import functools
import types
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from operator import getitem
from typing import Union, Any, Generic, Optional, get_origin, TypeVar, Type, TYPE_CHECKING, Mapping, KeysView, \
    ItemsView, ValuesView, cast, ClassVar

from frozendict import frozendict

from hgraph._types._schema_type import AbstractSchema
from hgraph._types._scalar_types import SCALAR, CompoundScalar
from hgraph._types._time_series_types import TimeSeriesInput, TimeSeriesOutput, DELTA_SCALAR, \
    TimeSeriesDeltaValue, TimeSeries
from hgraph._types._type_meta_data import ParseError
from hgraph._types._typing_utils import nth
from hgraph._wiring._wiring_errors import CustomMessageWiringError
from hgraph._wiring._wiring_node_instance import create_wiring_node_instance

if TYPE_CHECKING:
    from hgraph import Node, Graph, HgTimeSeriesTypeMetaData, HgTypeMetaData, WiringNodeSignature, WiringNodeType, \
    HgTSBTypeMetaData, HgTimeSeriesSchemaTypeMetaData, SourceCodeDetails, WiringNodeInstance, TS

__all__ = ("TimeSeriesSchema", "TSB", "TSB_OUT", "TS_SCHEMA", "is_bundle", "TimeSeriesBundle", "TimeSeriesBundleInput",
           "TimeSeriesBundleOutput", "UnNamedTimeSeriesSchema", "ts_schema")


class TimeSeriesSchema(AbstractSchema):
    """
    Describes a time series schema, this is similar to a data class, and produces a data class to represent
    it's point-in-time value.
    """
    __scalar_type__: ClassVar[Type[SCALAR] | None] = None

    @classmethod
    def scalar_type(cls) -> Type[SCALAR]:
        return cls.__dict__.get("__scalar_type__")

    def __init_subclass__(cls, **kwargs):
        scalar_type = kwargs.pop("scalar_type", False)
        super().__init_subclass__(**kwargs)

        if scalar_type is True:
            cls.__scalar_type__ = cls.to_scalar_schema()
        elif type(scalar_type) is type:
            cls.__scalar_type__ = scalar_type

    def __class_getitem__(cls, item):
        out = super(TimeSeriesSchema, cls).__class_getitem__(item)
        if cls.scalar_type() and item is not TS_SCHEMA:
            out.__scalar_type__ = out.to_scalar_schema()
        return out

    @staticmethod
    def from_scalar_schema(schema: Type[AbstractSchema]) -> Type["TimeSeriesSchema"]:
        """
        Creates a new schema from the scalar schema provided.
        """
        if schema is CompoundScalar:
            return TimeSeriesSchema

        assert issubclass(schema, CompoundScalar), f'Can only create bundle schema from scalar schemas, not {schema}'

        if tsc_schema := schema.__dict__.get("__bundle_type__", None):
            return tsc_schema

        if (root := schema._root_cls()) and root is not schema:
            root_bundle = TimeSeriesSchema.from_scalar_schema(root)
            return root_bundle[schema.__args__]

        from hgraph._types._ts_type import TS
        annotations = {k: TS[v.py_type] for k, v in schema.__meta_data_schema__.items()}

        bases = []
        for b in schema.__bases__:
            if issubclass(b, CompoundScalar):
                bases.append(TimeSeriesSchema.from_scalar_schema(b))
            elif b is Generic:
                bases.append(Generic[schema.__parameters__])
            else:
                bases.append(b)

        tsc_schema = types.new_class(f"{schema.__name__}Bundle",
                                     tuple(bases),
                                     None,
                                     lambda ns: ns.update({"__annotations__": annotations, "__module__": schema.__module__}))

        tsc_schema.__scalar_type__ = schema
        schema.__bundle_type__ = tsc_schema
        return tsc_schema

    @classmethod
    @functools.lru_cache(maxsize=None)
    def to_scalar_schema(cls: Type["TimeSeriesSchema"]) -> Type[CompoundScalar]:
        """
        Converts a time series schema to a scalar schema.
        """
        if cls is TimeSeriesSchema:
            return CompoundScalar

        assert issubclass(cls, TimeSeriesSchema), f'Can only convert bundle schemas to scalar schemas, not {cls}'

        if scalar_schema := cls.__dict__.get("__scalar_type__", None):
            return scalar_schema

        if (root := cls._root_cls()) and root is not cls:
            root_scalar = root.to_scalar_schema()
            return root_scalar[cls.__args__]

        bases = tuple(b.to_scalar_schema() if issubclass(b, TimeSeriesSchema) else b
                      for b in cls.__bases__)

        from hgraph._types._tsb_meta_data import HgTimeSeriesSchemaTypeMetaData
        annotations = {k: v.scalar_type().py_type
                          if not type(v) is HgTimeSeriesSchemaTypeMetaData
                          else v.py_type.to_scalar_schema()
                       for k, v in cls.__meta_data_schema__.items()}

        scalar_schema = type(f"{cls.__name__}Struct",
                             bases,
                             {"__annotations__": annotations, "__module__": cls.__module__})

        scalar_schema = dataclass(scalar_schema, frozen=True)  #should this be kw_only too?

        scalar_schema.__bundle_type__ = cls
        return scalar_schema


TS_SCHEMA = TypeVar("TS_SCHEMA", bound=TimeSeriesSchema)


class UnNamedTimeSeriesSchema(TimeSeriesSchema):
    """Use this class to create un-named bundle schemas"""

    @classmethod
    def create(cls, **kwargs) -> Type["UnNamedTimeSeriesSchema"]:
        """Creates a type instance with root class UnNamedTimeSeriesSchema using the kwargs provided"""
        from hgraph._types._time_series_meta_data import HgTimeSeriesTypeMetaData
        schema = {k: HgTimeSeriesTypeMetaData.parse_type(v) for k, v in kwargs.items()}
        if any(v is None for v in schema.values()):
            bad_inputs = {k: v for k, v in kwargs.items() if schema[k] is None}
            raise CustomMessageWiringError(f"The following inputs are not valid time-series types: {bad_inputs}")
        return cls.create_resolved_schema(schema)

    @classmethod
    def create_resolved_schema(cls, schema: Mapping[str, "HgTimeSeriesTypeMetaData"]) \
            -> Type["UnNamedTimeSeriesSchema"]:
        """Creates a type instance with root class UnNamedTimeSeriesSchema using the schema provided"""
        return cls._create_resolved_class(schema)


def ts_schema(**kwargs) -> Type["TimeSeriesSchema"]:
    """
    Creates an un-named time-series schema using the kwargs provided.
    """
    return UnNamedTimeSeriesSchema.create(**kwargs)


class TimeSeriesBundle(TimeSeriesDeltaValue[Union[TS_SCHEMA, dict[str, Any]], Union[TS_SCHEMA, dict[str, Any]]], ABC,
                       Generic[TS_SCHEMA]):
    """
    Represents a non-homogenous collection of time-series values.
    We call this a time-series bundle.
    """

    def __init__(self, __schema__: TS_SCHEMA, **kwargs):
        self.__schema__: TS_SCHEMA = __schema__
        self._ts_values: Mapping[str, TimeSeriesInput] = {
            k: kwargs.get(k, None) for k in self.__schema__.__meta_data_schema__.keys()
        }  # Initialise the values to None or kwargs provided

    def __class_getitem__(cls, item) -> Any:
        # For now limit to validation of item
        if item is not TS_SCHEMA:
            from hgraph._types._type_meta_data import HgTypeMetaData
            if HgTypeMetaData.parse_type(item).is_scalar:
                if isinstance(item, type) and issubclass(item, CompoundScalar):
                    item = TimeSeriesSchema.from_scalar_schema(item)
                else:
                    raise ParseError(
                        f"Type '{item}' must be a TimeSeriesSchema or a valid TypeVar (bound to to TimeSeriesSchema)")

            out = super(TimeSeriesBundle, cls).__class_getitem__(item)
            if hasattr(out, "from_ts"):
                fn = out.from_ts
                code = fn.__code__
                out.from_ts = functools.partial(fn, __schema__=item)
                out.from_ts.__code__ = code
        else:
            out = super(TimeSeriesBundle, cls).__class_getitem__(item)

        return out

    @property
    def as_schema(self) -> TS_SCHEMA:
        """
        Exposes the TSB as the schema type. This is useful for type completion in tools such as PyCharm / VSCode.
        It is a convenience method, it is possible to access the properties of the schema directly from the TSB
        instances as well.
        """
        return self

    def __getattr__(self, item) -> TimeSeries:
        """
        The time-series value for the property associated to item in the schema
        :param item:
        :return:
        """
        ts_values = self.__dict__.get("_ts_values")
        if item == "_ts_values":
            if ts_values is None:
                raise AttributeError(item)
            return ts_values
        if ts_values and item in ts_values:
            return ts_values[item]
        else:
            return super().__getattribute__(item)

    def __getitem__(self, item: Union[int, str]) -> "TimeSeries":
        """
        If item is of type int, will return the item defined by the sequence of the schema. If it is a str, then
        the item as named.
        """
        if type(item) is int:
            return self._ts_values[nth(iter(self.__schema__.__meta_data_schema__), item)]
        else:
            return self._ts_values[item]

    def keys(self) -> KeysView[str]:
        """The keys of the schema defining the bundle"""
        return self._ts_values.keys()

    @abstractmethod
    def items(self) -> ItemsView[str, TimeSeries]:
        """The items of the bundle"""
        return self._ts_values.items()

    @abstractmethod
    def values(self) -> ValuesView[TimeSeries]:
        """The values of the bundle"""
        return self._ts_values.values()


class TimeSeriesBundleInput(TimeSeriesInput, TimeSeriesBundle[TS_SCHEMA], Generic[TS_SCHEMA]):
    """
    The input form of the bundle. This serves two purposes, one to describe the shape of the code.
    The other is to use as a Marker class for typing system. To make this work we need to implement
    the abstract methods.
    """

    @staticmethod
    def _validate_kwargs(schema: TS_SCHEMA, **kwargs):
        from hgraph._wiring._wiring_port import WiringPort
        meta_data_schema: dict[str, "HgTypeMetaData"] = schema.__meta_data_schema__
        if any(k not in meta_data_schema for k in kwargs.keys()):
            from hgraph._wiring._wiring_errors import InvalidArgumentsProvided
            raise InvalidArgumentsProvided(tuple(k for k in kwargs.keys() if k not in meta_data_schema))

        for k, v in kwargs.items():
            # If v is a wiring port then we perform a validation of the output type to the expected input type.
            if isinstance(v, WiringPort):
                if not meta_data_schema[k].matches(cast(WiringPort, v).output_type.dereference()):
                    from hgraph import IncorrectTypeBinding
                    from hgraph import WiringContext
                    from hgraph import STATE
                    with WiringContext(current_arg=k, current_signature=STATE(
                            signature=f"TSB[{schema.__name__}].from_ts({', '.join(kwargs.keys())})")):
                        raise IncorrectTypeBinding(expected_type=meta_data_schema[k], actual_type=v.output_type)

    @staticmethod
    def from_ts(**kwargs) -> "TimeSeriesBundleInput[TS_SCHEMA]":
        """
        Create an instance of the TSB[SCHEMA] from the kwargs provided.
        This should be used in a graph instance only. It produces an instance of an un-bound time-series bundle with
        the time-series values set to the values provided.
        This does not require all values be present, but before wiring the bundle into an input, this will be a
        requirement.
        """
        schema: TS_SCHEMA = kwargs.pop("__schema__")
        fn_details = TimeSeriesBundleInput.from_ts.__code__
        from hgraph import WiringNodeSignature, WiringNodeType, SourceCodeDetails, HgTSBTypeMetaData, \
            HgTimeSeriesSchemaTypeMetaData, WiringNodeInstance
        wiring_node_signature = WiringNodeSignature(
            node_type=WiringNodeType.STUB,
            name=f"TSB[{schema.__name__}].from_ts",
            args=tuple(kwargs.keys()),
            defaults=frozendict(),
            input_types=frozendict(schema.__meta_data_schema__),
            output_type=HgTSBTypeMetaData(HgTimeSeriesSchemaTypeMetaData(schema)),
            src_location=SourceCodeDetails(fn_details.co_filename, fn_details.co_firstlineno),
            active_inputs=None,
            valid_inputs=None,
            all_valid_inputs=None,
            unresolved_args=frozenset(),
            time_series_args=frozenset(kwargs.keys()),
        )
        TimeSeriesBundleInput._validate_kwargs(schema, **kwargs)
        from hgraph._wiring._wiring_node_class._stub_wiring_node_class import NonPeeredWiringNodeClass
        from hgraph._wiring._wiring_port import TSBWiringPort, WiringPort
        wiring_node = NonPeeredWiringNodeClass(wiring_node_signature, lambda *args, **kwargs: None)
        wiring_node_instance = create_wiring_node_instance(
            node=wiring_node,
            resolved_signature=wiring_node_signature,
            inputs=frozendict(kwargs),
            rank=max((v.rank for k, v in kwargs.items() if isinstance(v, WiringPort)), default=1)
        )
        return TSBWiringPort(wiring_node_instance, tuple())

    def copy_with(self, __init_args__: dict = None, **kwargs):
        """
        Creates a new instance of a wiring time bundle using the values of this instance combined / overridden from
        the kwargs provided. Can be used to clone a runtime instance of a bundle as well.
        # TODO: support k: REMOVE semantics to remove a value from the bundle?
        """
        self._validate_kwargs(self.__schema__, **kwargs)
        value = self.__class__[self.__schema__](self.__schema__) if __init_args__ is None else \
            self.__class__[self.__schema__](self.__schema__, **__init_args__)
        value._ts_values = self._ts_values | kwargs
        return value

    @property
    def parent_input(self) -> Optional["TimeSeriesInput"]:
        raise NotImplementedError()

    @property
    def has_parent_input(self) -> bool:
        raise NotImplementedError()

    @property
    def bound(self) -> bool:
        raise NotImplementedError()

    @property
    def output(self) -> Optional[TimeSeriesOutput]:
        raise NotImplementedError()

    def do_bind_output(self, value: TimeSeriesOutput):
        raise NotImplementedError()

    @property
    def active(self) -> bool:
        raise NotImplementedError()

    def make_active(self):
        raise NotImplementedError()

    def make_passive(self):
        raise NotImplementedError()

    @property
    def value(self) -> Optional[SCALAR]:
        raise NotImplementedError()

    @property
    def delta_value(self) -> Optional[DELTA_SCALAR]:
        raise NotImplementedError()

    @property
    def owning_node(self) -> "Node":
        raise NotImplementedError()

    @property
    def owning_graph(self) -> "Graph":
        raise NotImplementedError()

    @property
    def modified(self) -> bool:
        raise NotImplementedError()

    @property
    def valid(self) -> bool:
        raise NotImplementedError()

    @property
    def all_valid(self) -> bool:
        raise NotImplementedError()

    @property
    def last_modified_time(self) -> datetime:
        raise NotImplementedError()

    def items(self) -> ItemsView[str, TimeSeriesInput]:
        return super().items()

    def values(self) -> ValuesView[TimeSeriesInput]:
        return super().values()


class TimeSeriesBundleOutput(TimeSeriesOutput, TimeSeriesBundle[TS_SCHEMA], ABC, Generic[TS_SCHEMA]):
    """
    The output form of the bundle
    """

    def items(self) -> ItemsView[str, TimeSeriesOutput]:
        return super().items()

    def values(self) -> ValuesView[TimeSeriesOutput]:
        return super().values()


TSB = TimeSeriesBundleInput
TSB_OUT = TimeSeriesBundleOutput


def is_bundle(bundle: Union[type, TimeSeriesBundle]) -> bool:
    """Is the value a TimeSeriesBundle type, or an instance of a TimeSeriesBundle"""
    return (origin := get_origin(bundle)) and issubclass(origin, TimeSeriesBundle) or isinstance(bundle,
                                                                                                 TimeSeriesBundle)
