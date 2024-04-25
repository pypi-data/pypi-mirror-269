"""
Data Model.
"""

from __future__ import annotations

from datetime import datetime, timezone
from functools import wraps
from inspect import signature
from types import FunctionType, MethodType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import structlog
from pydantic import Extra, ValidationError, validator
from pydantic.fields import ModelField

from .base_model import BaseModel, BaseModelMeta
from .deeplist import deeplist
from .utils import snake_name

logger = structlog.get_logger(__name__)

T = TypeVar("T")


class DataModelMeta(BaseModelMeta):
    """DataModel metaclass."""

    def __new__(
        metacls: Type[DataModelMeta], name: str, bases: Tuple[Type, ...], __dict__: Dict[str, Any]
    ) -> DataModelMeta:
        cls = cast(DataModelMeta, super().__new__(metacls, name, bases, __dict__))

        # kill unused fields so that they can be used by models
        cls.fields = cls.schema = None  # type: ignore

        return cls

    def __repr__(self) -> str:
        """Pretty representation."""

        methods = "\n".join(
            f"  - {name}: " + x.__doc__.lstrip().split("\n")[0]
            for name, x in ((name, getattr(self, name)) for name in sorted(vars(self)) if not name.startswith("_"))
            if x.__doc__ is not None and isinstance(x, (FunctionType, MethodType))
        )

        return f"{self.__name__}:\n{methods}"

    def __str__(self) -> str:
        """Return str(self)."""

        return f"<class {self.__name__!r}>"


class DataModel(BaseModel, metaclass=DataModelMeta):
    """Model base-class."""

    if TYPE_CHECKING:
        fields: Any
        schema: Any

    class Config(BaseModel.Config):
        """Model config."""

        extra = Extra.allow

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

    def __getattribute__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            result = super().__getattribute__(name)
        except AttributeError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        return getattr(head, tail)
                    except AttributeError:
                        pass
            raise

        return deeplist(result) if isinstance(result, list) else result

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute."""

        if name.startswith("_"):
            super().__setattr__(name, value)

        try:
            super().__setattr__(name, value)
        except ValueError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        setattr(head, tail, value)
                    except ValueError:
                        pass
                    else:
                        return
            raise

    @staticmethod
    def translate(names: Optional[Mapping[str, str]] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """Translate names and obtain data from object."""

        def outer(f: Callable[..., T]) -> Callable[..., T]:
            positional_args = [
                name
                for name, x in signature(f).parameters.items()
                if name not in {"_client", "_dry_run"} and x.default is x.empty
            ][1:]

            @wraps(f)
            def inner(obj: Any, *args: Any, **kwargs: Any) -> T:
                if isinstance(obj, DataModel):
                    owner_prefix = snake_name(type(obj._owner).__name__) + "_" if obj._owner is not None else None
                    for arg_name in positional_args[len(args) :]:
                        if names is not None and arg_name in names:
                            source = names[arg_name]
                            kwargs[arg_name] = obj[source]
                        elif arg_name in obj:
                            kwargs[arg_name] = obj[arg_name]
                        elif owner_prefix is not None and arg_name.startswith(owner_prefix):
                            try:
                                kwargs[arg_name] = obj._owner[arg_name.replace(owner_prefix, "")]
                            except KeyError:
                                pass

                return f(obj, *args, **kwargs)

            return inner

        return outer

    @validator("*", pre=True)
    def convert_datetime(cls, value: Any, field: ModelField) -> Any:
        """Correct data-type for datetime values."""

        if not isinstance(value, datetime):
            return value

        field_type = field.type_

        if not isinstance(field_type, type):
            return value

        if issubclass(field_type, str):
            suffix = "Z" if value.microsecond else ".000000Z"
            return value.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + suffix
        elif issubclass(field_type, float):
            return value.timestamp()
        elif issubclass(field_type, int):
            return int(value.timestamp() * 1e9)
        else:
            return value


P = TypeVar("P", bound=DataModel)


class PaginatorDataModel(DataModel, Generic[P]):
    """Paginator data-model."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

    @validator("data", pre=True, check_fields=False)
    def validate_data(cls, v: Sequence[Mapping[str, Any]], field: ModelField) -> List[P]:
        """Validate data field."""

        T = field.type_
        results = []

        for item in v:
            try:
                results += [T(**item)]
            except ValidationError as e:
                logger.warning("Skipped invalid item", name=T.__name__, item=item, error=e)

        return results

    def __getitem__(self, item: Union[str, int]) -> Any:
        """Get item."""

        if isinstance(item, int):
            return self.data[item]

        return super().__getitem__(item)


DataModelBase = DataModel
