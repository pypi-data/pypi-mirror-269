import json
import sys
import typing
from datetime import datetime

import yaml

from everai.app import App
from everai.commands.command import ClientCommand, command_error, ListDisplayer
from argparse import _SubParsersAction
from everai.app.app_manager import AppManager


class ListCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        list_parser = parser.add_parser('list', aliases=['ls'], help='List all apps')
        ListDisplayer.add_output_to_parser(list_parser)
        list_parser.set_defaults(func=ListCommand)

    @command_error
    def run(self):
        from tabulate import tabulate
        apps = AppManager().list()
        ListDisplayer[App](apps).show_list(self.args.output)
