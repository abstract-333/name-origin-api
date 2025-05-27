from datetime import UTC, datetime
from typing import Protocol, TypeVar

ModelT = TypeVar('ModelT')
EntityT = TypeVar('EntityT')


class BaseConverter(Protocol[ModelT, EntityT]):
    """Protocol for model to entity converters.

    This protocol defines the contract for all converters that transform between database models
    and domain entities.

    Type Parameters:
        ModelT: The type of the database model to convert from/to
        EntityT: The type of the domain entity to convert to/from
    """

    @classmethod
    def to_entity(cls, model: ModelT) -> EntityT:
        """Convert a database model to a domain entity.

        Args:
            model (ModelT): The database model to convert.

        Returns:
            EntityT: The converted domain entity.
        """
        ...

    @classmethod
    def to_model(cls, entity: EntityT) -> ModelT:
        """Convert a domain entity to a database model.

        Args:
            entity (EntityT): The domain entity to convert.

        Returns:
            ModelT: The converted database model.
        """
        ...


def to_db_datetime(dt: datetime) -> datetime:
    """Convert timezone-aware datetime to timezone-naive datetime for database storage.

    Args:
        dt: Timezone-aware datetime object

    Returns:
        Timezone-naive datetime object
    """
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


def from_db_datetime(dt: datetime) -> datetime:
    """Convert timezone-naive datetime from database to timezone-aware datetime.

    Args:
        dt: Timezone-naive datetime object from database

    Returns:
        Timezone-aware datetime object with UTC timezone
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt
