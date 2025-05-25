from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime, UTC


@dataclass(kw_only=True)
class CountryEntity:
    """Country entity for country-related data.
    Attributes:
        iso_alpha2_code: ISO 3166-1 alpha-2 country code (e.g., 'US' for United States)
        common_name: Common name of the country (e.g., 'United States')
        official_name: Official name of the country (e.g., 'United States of America')
        region: Geographic region of the country (e.g., 'Americas')
        sub_region: Sub-region of the country (e.g., 'Northern America')
        independent: Whether the country is independent (e.g., True), it could be None
        capital: Set of capital cities (some countries have multiple capitals), it could be None
        capital_lat: Capital city latitude (e.g., 37.774929), it could be None
        capital_long: Capital city longitude (e.g., -122.419416), it could be None
        flag_png: URL to the country's flag in PNG format
        flag_svg: URL to the country's flag in SVG format
        flag_alt: Alternative text description of the flag (optional)
        coat_of_arms_png: URL to the country's coat of arms in PNG format (optional)
        coat_of_arms_svg: URL to the country's coat of arms in SVG format (optional)
        borders: Set of ISO alpha-2 codes representing bordering countries (e.g., {'US', 'CA'}), it could be island
        created_at: Timestamp of entity creation
    """

    iso_alpha2_code: str
    common_name: str
    official_name: str
    region: str
    sub_region: str
    independent: bool | None
    capital: set[str] = field(
        default_factory=set,
    )
    capital_lat: float | None
    capital_long: float | None
    flag_png: str
    flag_svg: str
    flag_alt: str | None
    coat_of_arms_png: str | None
    coat_of_arms_svg: str | None
    borders: set[str] = field(
        default_factory=set,
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    def __hash__(self) -> int:
        return hash(self.iso_alpha2_code)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, CountryEntity):
            raise NotImplementedError

        return self.iso_alpha2_code == __value.iso_alpha2_code

    @property
    def capital_name(self) -> str:
        """Returns all capital(s) combined into a single string.

        Returns:
            str: Comma-separated list of capital(s), or empty string if no capital(s)
        """
        return ', '.join(sorted(self.capital)) if self.capital else ''
