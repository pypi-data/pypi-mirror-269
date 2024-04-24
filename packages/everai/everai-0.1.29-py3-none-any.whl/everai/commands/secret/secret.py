from everai.commands.command import ClientCommand, setup_subcommands
from argparse import _SubParsersAction
from everai.commands.secret.create import SecretCreateCommand
from everai.commands.secret.delete import SecretDeleteCommand
from everai.commands.secret.list import SecretListCommand
from everai.commands.secret.get import SecretGetCommand


class SecretCommand(ClientCommand):
    parser: _SubParsersAction = None

    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        secret_parser = parser.add_parser('secret', help='Manage secrets')
        secret_subparser = secret_parser.add_subparsers(help="Secret command help")

        setup_subcommands(secret_subparser, [
            SecretCreateCommand,
            SecretDeleteCommand,
            SecretListCommand,
            SecretGetCommand,
        ])

        secret_parser.set_defaults(func=SecretCommand)
        SecretCommand.parser = secret_parser

    def run(self):
        SecretCommand.parser.print_help()
        return
