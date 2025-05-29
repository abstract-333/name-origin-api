from datetime import datetime
from pydantic import BaseModel, Field

from domain.entities.name import NameEntity


class CountryOutSchema(BaseModel):
    country: str = Field(
        ...,
        description="Comma-separated list of country code and names (e.g., 'CA,Canada,Canada')",
    )
    region: str = Field(..., description='Region where the country is located')
    sub_region: str = Field(..., description='Sub-region where the country is located')
    independent: bool | None = Field(
        ..., description='Whether the country is independent'
    )
    capital: str | None = Field(..., description='Capital city name')
    capital_lat: float | None = Field(..., description='Latitude of the capital')
    capital_long: float | None = Field(..., description='Longitude of the capital')
    flag_png: str = Field(..., description='URL to PNG flag image')
    flag_svg: str = Field(..., description='URL to SVG flag image')
    flag_alt: str | None = Field(..., description='Alt text for the flag')
    coat_of_arms_png: str | None = Field(
        ..., description='URL to PNG coat of arms image'
    )
    coat_of_arms_svg: str | None = Field(
        ..., description='URL to SVG coat of arms image'
    )
    borders: str = Field(
        ...,
        description="Comma-separated list of bordering country codes, or 'island' if no borders",
    )


class NameOriginsOutSchema(BaseModel):
    name: str = Field(..., description='The name being queried')
    count_of_requests: int = Field(..., description='Number of requests for this name')
    last_accessed: datetime | None = Field(
        None, description='Last time the name was accessed'
    )
    probability: float = Field(
        ..., description='Probability of the name being from this country'
    )
    # Country fields
    country: str = Field(
        ...,
        description="Comma-separated list of country code and names (e.g., 'CA,Canada,Canada')",
    )
    region: str = Field(
        ..., description='Region and sub-region in format "Region,Sub-region"'
    )
    independent: bool | None = Field(
        ..., description='Whether the country is independent'
    )
    capital: str | None = Field(..., description='Capital city name')
    capital_coordinates: str = Field(
        ..., description='Capital coordinates in format "lat,long"'
    )
    flag_png: str = Field(..., description='URL to PNG flag image')
    flag_svg: str = Field(..., description='URL to SVG flag image')
    flag_alt: str | None = Field(..., description='Alt text for the flag')
    coat_of_arms_png: str | None = Field(
        ..., description='URL to PNG coat of arms image'
    )
    coat_of_arms_svg: str | None = Field(
        ..., description='URL to SVG coat of arms image'
    )
    borders: str = Field(
        ...,
        description="Comma-separated list of bordering country codes, or 'island' if no borders",
    )

    @classmethod
    def from_entity(cls, name_origin: NameEntity) -> 'NameOriginsOutSchema':
        return cls(
            name=name_origin.name.as_generic_type(),
            count_of_requests=name_origin.count_of_requests.as_generic_type(),
            last_accessed=name_origin.last_accessed_at
            if hasattr(name_origin, 'last_accessed_at')
            else None,
            probability=name_origin.probability.as_generic_type(),
            country=name_origin.country.country_name,
            region=name_origin.country.region_full,
            independent=name_origin.country.independent,
            capital=name_origin.country.capital_name,
            capital_coordinates=name_origin.country.capital_coordinates,
            flag_png=name_origin.country.flag_png,
            flag_svg=name_origin.country.flag_svg,
            flag_alt=name_origin.country.flag_alt,
            coat_of_arms_png=name_origin.country.coat_of_arms_png,
            coat_of_arms_svg=name_origin.country.coat_of_arms_svg,
            borders=name_origin.country.borders_str,
        )
