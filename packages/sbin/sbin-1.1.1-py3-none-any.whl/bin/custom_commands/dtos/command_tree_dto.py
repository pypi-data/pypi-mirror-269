from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import root_validator, validator

from bin.commands.command import Command
from bin.commands.errors import CommandParseError
from bin.commands.internal.factory import InternalCommandFactory
from bin.commands.internal.log_title_command import LogTitleCommand
from bin.custom_commands.basic_command import BasicCommand
from bin.custom_commands.command_tree import CommandTree
from bin.custom_commands.dtos.base_custom_command_dto import BaseCustomCommandDto
from bin.custom_commands.dtos.str_custom_command_dto import StrCustomCommandDto
from bin.env.env import Env
from bin.models.bin_base_model import BinBaseModel
from bin.models.str_command import StrCommand
from bin.up.dtos import UpSubcommandDto
from bin.up.dtos.up_command_mapper import UpCommandMapper


class CommandTreeDto(BinBaseModel, BaseCustomCommandDto):
    env: Env = Env({})
    up: List[UpSubcommandDto] = []
    run: Optional[StrCommand]
    alias: Optional[str]
    aliases: List[str] = []
    subcommands: Dict[str, Union[CommandTreeDto, StrCustomCommandDto]] = {}

    @root_validator(pre=True)
    def must_contain_at_least_a_command(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        run = values.get("run")
        subcommands = values.get("subcommands", {})
        up = values.get("up", [])
        if run is None and len(subcommands) == 0 and len(up) == 0:
            raise ValueError("Command tree must have at least a runnable command")

        return values

    @validator("alias")
    def alias_must_not_use_up_down(cls, value: str) -> str:
        if value in ("up", "down"):
            raise ValueError("up/down are reserved commands")

        return value

    @validator("subcommands")
    def subcommands_must_not_use_up_or_down(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        if "up" in value or "down" in value:
            raise ValueError("up/down are reserved commands")

        return value

    @validator("aliases")
    def aliases_must_be_unique(cls, values: List[str]) -> List[str]:
        if len(values) != len(set(values)):
            raise ValueError("command aliases are clashing")

        return values

    @validator("aliases", each_item=True)
    def aliases_item_must_not_clash_with_subcommands(cls, value: str, values: Dict[str, Any]) -> str:
        subcommands = values.get("subcommands", {})
        if value in subcommands:
            raise ValueError("command aliases are clashing")

        if value in ("up", "down"):
            raise ValueError("up/down are reserved commands")

        if value == values.get("alias"):
            raise ValueError("command aliases are clashing")

        return value

    def to_command(self, self_name: str) -> Dict[str, Command]:
        if self.run is not None and len(self.subcommands) == 0 and len(self.up) == 0:
            return self.__to_command_dict(self_name, BasicCommand.no_help(self.run))

        self_cmd = None
        if self.run is not None:
            self_cmd = BasicCommand.no_help(self.run)

        cmd = CommandTree(self_cmd=self_cmd, subcommands_tree=self.__to_subcommands_dict(self_name))
        return self.__to_command_dict(self_name, cmd)

    def __to_command_dict(self, self_name: str, cmd: Command) -> Dict[str, Command]:
        aliases = self.__aliases()
        if self_name in aliases:
            raise CommandParseError(f"conflicting subcommand names or aliases in '{self_name}'")

        wrapped = InternalCommandFactory.wrap_with_env(self.env, cmd)
        result = {self_name: wrapped}
        for alias in aliases:
            result[alias] = wrapped

        return result

    def __to_subcommands_dict(self, self_name: str) -> Dict[str, Command]:
        result: Dict[str, Command] = {}
        if len(self.up) > 0:
            result["up"] = InternalCommandFactory.with_setup(
                [LogTitleCommand.up()], UpCommandMapper.to_up_command(self.up)
            )
            result["down"] = InternalCommandFactory.with_setup(
                [LogTitleCommand.down()], UpCommandMapper.to_down_command(self.up)
            )

        for name, cmd_dto in self.subcommands.items():
            cmd_dict = cmd_dto.to_command(name)
            result_candidate = {**result, **cmd_dict}
            if len(result_candidate) != len(result) + len(cmd_dict):
                raise CommandParseError(f"conflicting subcommand names or aliases in '{self_name}'")

            result = result_candidate

        return result

    def __aliases(self) -> List[str]:
        if self.alias is None:
            return self.aliases

        return self.aliases + [self.alias]
