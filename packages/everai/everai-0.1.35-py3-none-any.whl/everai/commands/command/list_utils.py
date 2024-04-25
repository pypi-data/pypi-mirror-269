import argparse
import json
import sys
import typing
from datetime import datetime

import yaml
from tabulate import tabulate


class HasRequiredMethod(typing.Protocol):
    @classmethod
    def table_title(cls, wide: bool = False) -> typing.List[str]:
        ...

    def table_row(self, wide: bool = False) -> typing.List:
        ...

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        ...


T = typing.TypeVar("T", bound=HasRequiredMethod)


def yaml_output(items: typing.List[T]):
    yaml.dump([item.to_dict() for item in items],
              sys.stdout,
              default_flow_style=False)


def json_output(items: typing.List[T]):
    def datatime_default(o: typing.Any):
        if isinstance(o, datetime):
            return o.isoformat()

    data = json.dumps([item.to_dict() for item in items],
                      default=datatime_default,
                      indent=2,
                      )
    print(data)


class ListDisplayer(typing.Generic[T]):
    def __init__(self, items: typing.Union[T, typing.List[T]]):
        if isinstance(items, typing.List):
            self.items = items
        else:
            self.items = [items]

    def table_title(self, wide: bool = False):
        assert hasattr(self, '__orig_class__')
        cls = getattr(self, '__orig_class__').__args__[0]
        return cls.table_title(wide=wide)

    def show_list(self, output: str = 'table'):
        match output:
            case 'wide':
                titles = self.table_title(wide=True)
                wide = True
            case 'yaml':
                return yaml_output(self.items)
            case 'json':
                return json_output(self.items)
            case _:
                titles = self.table_title()
                wide = False

        print(
            tabulate(
                [item.table_row(wide=wide) for item in self.items],
                headers=titles,
            ),
        )

    @staticmethod
    def add_output_to_parser(parser: argparse.ArgumentParser):
        parser.add_argument("--output", "-o",
                            help="Output format, One of: (json, yaml, table, wide)",
                            nargs="?", default="table")
