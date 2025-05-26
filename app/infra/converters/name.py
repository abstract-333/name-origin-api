from domain.entities.name import NameEntity
from domain.values.name import CountOfRequests, Name, Probability
from infra.converters.base import BaseConverter
from infra.converters.country import CountryConverter
from infra.models.name import NameOriginModel


class NameConverter(BaseConverter[NameOriginModel, NameEntity]):
    """Converter for transforming between NameOriginModel and NameEntity."""

    @classmethod
    def to_entity(cls, model: NameOriginModel) -> NameEntity:
        """Convert NameOriginModel to NameEntity.

        Args:
            model (NameOriginModel): The SQLAlchemy model instance to convert.

        Returns:
            NameEntity: The converted domain entity.
        """
        return NameEntity(
            name=Name(value=model.name),
            count_of_requests=CountOfRequests(value=model.count_of_requests),
            probability=Probability(value=model.probability),
            country=CountryConverter.to_entity(model.country),
        )

    @classmethod
    def to_model(cls, entity: NameEntity) -> NameOriginModel:
        """Convert NameEntity to NameOriginModel.

        Args:
            entity (NameEntity): The domain entity to convert.

        Returns:
            NameOriginModel: The converted SQLAlchemy model.
        """
        return NameOriginModel(
            name=entity.name.as_generic_type(),
            probability=entity.probability.as_generic_type(),
            count_of_requests=entity.count_of_requests.as_generic_type(),
            country_code=entity.country.iso_alpha2_code,
        ) 