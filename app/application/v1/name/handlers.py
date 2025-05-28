from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from punq import Container
from logic.init import init_container
from logic.mediator import Mediator
from logic.commands.name import GetNameOriginsCommand, GetFrequentNamesCountryCommand
from logic.exceptions.name import NameNotFoundException
from logic.exceptions.country import CountryNotFoundException
from application.v1.name.schemas import NameOriginsOutSchema
from application.v1.exceptions.schemas import (
    ErrorResponseSchema,
)


router = APIRouter(tags=['Name'], prefix='/names')


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=list[NameOriginsOutSchema],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorResponseSchema,
            'description': 'Invalid request parameters',
            'content': {
                'application/json': {
                    'example': {
                        'detail': {
                            'error': 'Name parameter is required',
                        },
                    },
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorResponseSchema,
            'description': 'Name or country not found',
            'content': {
                'application/json': {
                    'example': {
                        'detail': {
                            'error': [
                                'Country information not found for /name/',
                                'Name /name/ not found',
                            ],
                        },
                    },
                },
            },
        },
    },
)
async def get_name_origins_handler(
    name: str,
    container: Container = Depends(dependency=init_container),
) -> list[NameOriginsOutSchema]:
    """Get name origins with country information.

    Args:
        name: The name to get origins for

    Returns:
        List of name origins with country information, sorted by probability in descending order

    Raises:
        HTTPException: If the name parameter is missing or if the name/country is not found
    """
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'error': 'Name parameter is required',
            },
        )

    mediator: Mediator = container.resolve(Mediator)
    try:
        name_origins, *_ = await mediator.handle_command(
            command=GetNameOriginsCommand(name=name),
        )
        # Convert to list of schemas and sort by probability in descending order
        results = [
            NameOriginsOutSchema.from_entity(name_origin_entity)
            for name_origin_entity in name_origins
        ]
        return results

    except NameNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'error': f"Name '{name}' not found",
            },
        ) from exception

    except CountryNotFoundException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'error': f"Country information not found for name '{name}'",
            },
        ) from exception

    except Exception as exception:
        raise exception

@router.get(
    path='/popular-names/',
    status_code=status.HTTP_200_OK,
    response_model=list[NameOriginsOutSchema],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': ErrorResponseSchema,
            'description': 'Invalid request parameters',
            'content': {
                'application/json': {
                    'example': {
                        'detail': {
                            'error': 'Country parameter is required',
                        },
                    },
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorResponseSchema,
            'description': 'No names found for country',
            'content': {
                'application/json': {
                    'example': {
                        'detail': {
                            'error': 'No names found for country US',
                        },
                    },
                },
            },
        },
    },
)
async def get_popular_names_by_country_handler(
    country: str,
    container: Container = Depends(dependency=init_container),
) -> list[NameOriginsOutSchema]:
    """Get top 5 most frequent names for a specific country.

    Args:
        country: The country code to get popular names for (e.g. "US", "UA")

    Returns:
        List of top 5 most frequent names with country information

    Raises:
        HTTPException: If the country parameter is missing or if no names are found
    """
    if not country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'error': 'Country parameter is required',
            },
        )

    mediator: Mediator = container.resolve(Mediator)
    try:
        top_frequent_names, *_ = await mediator.handle_command(
            command=GetFrequentNamesCountryCommand(country_name=country.upper()),
        )
        if not top_frequent_names:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'error': f'No names found for country {country}',
            },
        ) 
        results = [
            NameOriginsOutSchema.from_entity(name_origin_entity)
            for name_origin_entity in top_frequent_names
        ]
        return results

    except Exception as exception:
        raise exception
