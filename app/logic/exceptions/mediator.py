from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self) -> str:
        return f'Command not found: {self.command_type}'
