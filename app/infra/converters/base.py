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