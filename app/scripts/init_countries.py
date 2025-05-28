import asyncio

from logic.init import init_container
from logic.mediator import Mediator
from logic.commands.country import FetchAndSaveCountriesCommand
from punq import Container


async def main() -> None:
    """Initialize countries by fetching them from API and saving to database."""
    container: Container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(FetchAndSaveCountriesCommand())
        print('Countries fetched and saved successfully')
    except Exception as e:
        print(f'Error occurred: {e}')
        raise


if __name__ == '__main__':
    asyncio.run(main())
