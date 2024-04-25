import subprocess
import os
from .remote_manager import RemoteDeviceManager
import magic
import yaml
import argparse

_custom_help = '''
usage: 
  magic ssh host                           # connect remote host (username@ip)
  magic ssh -p 2222 root@10.203.254.178    # specify port
  magic ssh config                         # register device
  ...
                 
positional arguments:
  list                  list all registered devices 
  info                  find and display details about host/name
  config                register device
  
optional arguments:
  -h, --help            show this help message and exit
  --password            password
  -p, --port            port
  --config              load conf from file, eg. rsync.yaml
  -L                    map local port
'''


class CustomHelpFormatter(argparse.HelpFormatter):
    def format_help(self):
        custom_help = _custom_help
        return custom_help


def config_parser(sub_parsers):
    p = sub_parsers.add_parser("ssh", help="ssh helper, check remote devices",
                               formatter_class=CustomHelpFormatter)
    p.add_argument('argv', nargs="*", help='command args')
    p.add_argument('--password', default=None, help='password')
    p.add_argument('-p', '--port', type=int, default=22, help='port')
    p.add_argument('--config', help='rsync.yaml')
    p.add_argument('-L', '--map-local', default=None, help='map local port')
    p.set_defaults(func=execute)


def execute(args):
    argv = args.argv
    default_args = dict(
        password=args.password,
        port=args.port,
        map_local=args.map_local
    )

    remote_manager = RemoteDeviceManager()
    # 参数解析
    if len(argv) == 0:
        # 解析配置文件的参数，不使用命令行参数
        config_file = args.config or os.path.join(os.getcwd(), '.vscode/rsync.yaml')
        if not os.path.exists(config_file):
            raise FileNotFoundError("Not found config '{}'".format(config_file))
        with open(config_file, 'r') as f:
            conf = yaml.safe_load(f)
        default_args['host'] = conf['host']
        default_args['password'] = conf.get('password')
        default_args['port'] = conf.get('port', 22)
        default_args['IdentityFile'] = conf.get('IdentityFile', None)
        ssh_connect(**default_args)
    elif argv[0] == 'list':
        remote_manager.list_all_devices()
    elif argv[0] == 'info':
        device = remote_manager.get_device(argv[1])
        print(device)
    elif argv[0] == 'config':
        remote_config_file = os.path.join(magic.config_root, 'remote_device.pt')
        subprocess.run(f'gedit {remote_config_file}', shell=True)
    else:
        default_args['host'] = argv[0]
        device = remote_manager.get_device(argv[0])
        if device is not None:
            default_args['host'] = device.host
            default_args['password'] = device.password
            default_args['port'] = device.port
            default_args['IdentityFile'] = device.IdentityFile
        ssh_connect(**default_args)

def ssh_connect(host, password=None, port=22, IdentityFile=None, map_local=None):
    if password:
        assert isinstance(password, str)
        sshpass_cmd = 'sshpass -p {} ssh -p {} -o StrictHostKeyChecking=no {}'.format(password, port, host)
        if map_local:
            sshpass_cmd += ' -L {}'.format(map_local)
        subprocess.run(sshpass_cmd, shell=True)
    else:
        ssh_cmd = f'ssh -p {port} {host}'
        if IdentityFile:
            ssh_cmd += ' -i {}'.format(IdentityFile)
        if map_local:
            ssh_cmd += ' -L {}'.format(map_local)
        print(ssh_cmd)
        subprocess.run(ssh_cmd, shell=True)
