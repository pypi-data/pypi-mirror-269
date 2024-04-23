from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
from bigtree import Node, find_path, add_path_to_tree
from tqdm import tqdm

from raspberry_config_sdk.utils import is_running_bookworm


@dataclass
class Option:
    """
    :var path: Path is the key for the setting but since we can have sub settings we call it path
                Nested key example:
                    In File: dtparam=audio=on
                    Path: ["dtparam", "audio"]
                    Value: on
    """

    path: str | List[str]
    value: Optional[str] = None
    comments: List[str] = dataclasses.field(default_factory=list)


class BootConfig:
    SEPERATOR = "="
    ROOT_NODE_NAME = "root"

    _is_running_bookworm: bool = is_running_bookworm()
    _config_path: Path
    _config: Node

    def __init__(self, config_path: Optional[Path] = None):
        self._config_path = config_path
        if not config_path:
            self._config_path = (
                Path("/boot/firmware/config.txt") if self._is_running_bookworm else Path("/boot/config.txt")
            )

        self._config = Node(BootConfig.ROOT_NODE_NAME, sep=BootConfig.SEPERATOR)
        self._parse_config_file()

    def _parse_config_file(self):
        with self._config_path.open() as file:
            comments = []
            for line in tqdm(file.readlines(), desc="Parsing Config"):
                if line.startswith("\n"):
                    continue

                # Pre Process Line
                line = line.replace("\n", "")

                if line.startswith("#"):
                    comments.append(line.lstrip("#").strip())
                    continue

                components = line.split(BootConfig.SEPERATOR)
                option_keys = components[:-1]

                option_keys.insert(0, BootConfig.ROOT_NODE_NAME)  # Add root node

                add_path_to_tree(
                    self._config,
                    BootConfig.SEPERATOR.join(option_keys),
                    sep=BootConfig.SEPERATOR,
                    duplicate_name_allowed=False,
                    node_attrs={"value": components[-1], "comments": comments},
                )
                comments = []

    def reload_config_file(self):
        self._config = Node(BootConfig.ROOT_NODE_NAME, sep=BootConfig.SEPERATOR)
        self._parse_config_file()

    def get_config(self, path: str | List[str]) -> Optional[Option]:
        """

        :param path: Path is the key for the setting but since we can have sub settings we call it path
                    Nested key example:
                        In File: dtparam=audio=on
                        Path: ["dtparam", "audio"]
                        Value: on
        :return:
        """
        tree_path = path.copy() if isinstance(path, list) else [path]
        tree_path.insert(0, BootConfig.ROOT_NODE_NAME)

        option = find_path(self._config, BootConfig.SEPERATOR.join(tree_path))
        if not option:
            return None

        return Option(path=path, value=option.get_attr("value"), comments=option.get_attr("comments", []))

    def add_or_update_config(self, option: Option) -> BootConfig:
        tree_path = option.path.copy() if isinstance(option.path, list) else [option.path]
        tree_path.insert(0, BootConfig.ROOT_NODE_NAME)

        add_path_to_tree(
            self._config,
            BootConfig.SEPERATOR.join(tree_path),
            sep=BootConfig.SEPERATOR,
            duplicate_name_allowed=False,
            node_attrs={"value": option.value, "comments": option.comments},
        )
        return self

    def _save(self, node: Node):
        """
        Recurse over the nodes to recreate config file with correct format

        :param node:
        :return:
        """
        text = ""

        for comment in node.get_attr("comments", []):
            text += f"# {comment}\n"

        if value := node.get_attr("value"):
            text += f"{node.path_name.lstrip(f'{BootConfig.ROOT_NODE_NAME}=')}{BootConfig.SEPERATOR}{value}\n"

        for child in node.children:
            text += self._save(child)

        return text

    def save(self):
        config = self._save(self._config)
        self._config_path.write_text(config)
