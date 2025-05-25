from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from logic.commands.base import (
    CommandHandler,
    CR,
    CT,
)
from logic.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
)


@dataclass(eq=False)
class Mediator:
    commands_map: defaultdict[CT, list[CommandHandler[CT, CR]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_command(
        self,
        command: CT,
        command_handlers: Iterable[CommandHandler[CT, CR]],
    ) -> None:
        self.commands_map[command].extend(command_handlers)

    async def handle_command(self, command: CT) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type=command_type)

        return [await handler.handle(command) for handler in handlers]
