from everai.commands.command import ClientCommand, command_error
from argparse import _SubParsersAction
from everai.volume.volume_manager import VolumeManager


class VolumeListCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        list_parser = parser.add_parser('list', help='List volume')

        list_parser.set_defaults(func=VolumeListCommand)

    @command_error
    def run(self):
        list_volumes = VolumeManager().list_volumes()
        for volume in list_volumes:
            print(volume)



