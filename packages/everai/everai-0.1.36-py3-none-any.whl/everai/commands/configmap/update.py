from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction

from everai.configmap import ConfigMapManager
from everai.secret.secret_manager import SecretManager


class UpdateCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        create_parser = parser.add_parser('update', help='Update ConfigMap from file or literal string')
        create_parser.add_argument('name', help='The configmap name')
        create_parser.add_argument(
            '-l',
            '--from-literal',
            action='append',
            type=str,
            help='Update configmap from literal, for example: --from-literal name=user'
        )

        create_parser.add_argument(
            '-f',
            '--from-file',
            action='append',
            type=str,
            help='Update configmap from file, for example: --from-file filename'
        )

        create_parser.set_defaults(func=UpdateCommand)

    @command_error
    def run(self):
        if self.args.from_literal is None and self.args.from_file is None:
            raise ValueError('Please specify either --from-literal, or --from-file arguments')

        if self.args.from_literal is not None and self.args.from_file is not None:
            raise ValueError('Cannot support both --from-literal and --from-file')

        if self.args.from_literal is not None and len(self.args.from_literal) > 0:
            configmap = ConfigMapManager().update_from_literal(name=self.args.name, literals=self.args.from_literal)
        elif self.args.from_file is not None and len(self.args.from_file) > 0:
            configmap = ConfigMapManager().update_from_file(name=self.args.name, file=self.args.from_file)
        else:
            raise RuntimeError('Never been here')

        print(f"Configmap `{configmap.name}` updated successfully")

