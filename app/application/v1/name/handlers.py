from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.routing import APIRouter

from punq import Container
from logic.init import init_container
from logic.mediator import Mediator
from logic.commands.name import GetNameOriginsCommand
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
