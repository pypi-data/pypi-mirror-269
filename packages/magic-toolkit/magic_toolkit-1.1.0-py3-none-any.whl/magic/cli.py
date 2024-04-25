import argparse
import sys
from magic import __version__
from .scripts.shell_wrapper import config_parser as shell_config_parser
from .deployment.sftp_put import config_parser as deployment_sftp_put_config_parser
from .deployment.ssh_login import config_parser as deployment_ssh_config_parser
from .deployment.sftp_get import config_parser as deployment_sftp_get_config_parser
from .deployment.rsync import config_parser as deployment_rsync_config_parser

def show_help_on_empty_command():
    if len(sys.argv) == 1:
        sys.argv.append("--help")

def create_parser():
    p = argparse.ArgumentParser()
    p.add_argument('-v', '--version', action='version', version=__version__)
    sub_parsers = p.add_subparsers(
        metavar="command",
        dest="cmd",
        required=False,
    )

    shell_config_parser(sub_parsers)  # scripts
    deployment_sftp_put_config_parser(sub_parsers)
    deployment_sftp_get_config_parser(sub_parsers)
    deployment_ssh_config_parser(sub_parsers)
    deployment_rsync_config_parser(sub_parsers)

    show_help_on_empty_command()
    return p

def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)
