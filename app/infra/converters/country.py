from domain.entities.country import CountryEntity
from infra.converters.base import BaseConverter
from infra.models.country import CountryModel


class CountryConverter(BaseConverter[CountryModel, CountryEntity]):
    """Converter for transforming between CountryModel and CountryEntity."""

    @classmethod
    def to_entity(cls, model: CountryModel) -> CountryEntity:
        """Convert CountryModel to CountryEntity.

        Args:
            model (CountryModel): The SQLAlchemy model instance to convert.

        Returns:
            CountryEntity: The converted domain entity.
        """
        return CountryEntity(
            iso_alpha2_code=model.iso_alpha2_code,
            common_name=model.common_name,
            official_name=model.official_name,
            region=model.region,
            sub_region=model.sub_region,
            independent=model.independent,
            capital=set(model.capital.split(',')) if model.capital else set(),
            capital_lat=model.capital_lat,
            capital_long=model.capital_long,
            flag_png=model.flag_png,
            flag_svg=model.flag_svg,
            flag_alt=model.flag_alt,
            coat_of_arms_png=model.coat_of_arms_png,
            coat_of_arms_svg=model.coat_of_arms_svg,
            borders=set(model.borders.split(',')) if model.borders else set(),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_model(cls, entity: CountryEntity) -> CountryModel:
        """Convert CountryEntity to CountryModel.

        Args:
            entity (CountryEntity): The domain entity to convert.

        Returns:
            CountryModel: The converted SQLAlchemy model.
        """
        return CountryModel(
            iso_alpha2_code=entity.iso_alpha2_code,
            common_name=entity.common_name,
            official_name=entity.official_name,
            region=entity.region,
            sub_region=entity.sub_region,
            independent=entity.independent,
            capital=','.join(sorted(entity.capital)) if entity.capital else None,
            capital_lat=entity.capital_lat,
            capital_long=entity.capital_long,
            flag_png=entity.flag_png,
            flag_svg=entity.flag_svg,
            flag_alt=entity.flag_alt,
            coat_of_arms_png=entity.coat_of_arms_png,
            coat_of_arms_svg=entity.coat_of_arms_svg,
            borders=','.join(sorted(entity.borders)) if entity.borders else None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
