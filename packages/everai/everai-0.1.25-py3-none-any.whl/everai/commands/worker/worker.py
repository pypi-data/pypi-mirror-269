from argparse import _SubParsersAction

from everai.commands.command import ClientCommand, setup_subcommands
from .list import ListCommand


class WorkerCommand(ClientCommand):
    parser: _SubParsersAction = None

    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        worker_parser = parser.add_parser('worker', help='Manage the worker of app')
        worker_subparser = worker_parser.add_subparsers(help='Worker command help')

        setup_subcommands(worker_subparser, [
            ListCommand,
        ])

        worker_parser.set_defaults(func=WorkerCommand)
        WorkerCommand.parser = worker_parser

    def run(self):
        WorkerCommand.parser.print_help()
