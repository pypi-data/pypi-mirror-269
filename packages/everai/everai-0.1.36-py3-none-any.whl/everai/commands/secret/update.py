from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction
from everai.secret.secret_manager import SecretManager


class UpdateCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        create_parser = parser.add_parser('update', help='Update the Secret from file or literal string')
        create_parser.add_argument('name', help='The secret name')
        create_parser.add_argument(
            '-l',
            '--from-literal',
            action='append',
            type=str,
            help='Create secret from literal, for example: --from-literal name=user'
        )

        create_parser.add_argument(
            '-f',
            '--from-file',
            action='append',
            type=str,
            help='Create secret from file, for example: --from-file filename, '
                 'file is yaml for simply key value, all value should be string'
        )

        create_parser.set_defaults(func=UpdateCommand)

    @command_error
    def run(self):
        if self.args.from_literal is None and self.args.from_file is None:
            raise ValueError('Please specify either --from-literal, or --from-file arguments')

        if self.args.from_literal is not None and self.args.from_file is not None:
            raise ValueError('Cannot support both --from-literal and --from-file')

        if self.args.from_literal is not None and len(self.args.from_literal) > 0:
            secret = SecretManager().update_from_literal(name=self.args.name, literals=self.args.from_literal)

        if self.args.from_file is not None and len(self.args.from_file) > 0:
            secret = SecretManager().create_from_file(name=self.args.name, file=self.args.from_file)

        print("Secret updated successfully")

