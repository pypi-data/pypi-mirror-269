import paramiko
import os
import stat
import yaml
import subprocess

def shell(cmd):
    ret = subprocess.run(cmd, shell=True, capture_output=False)
    assert ret.returncode == 0, "assert shell returncode == 0"

class SftpClient:
    def __init__(self, host, port, password=None, timeout=10):
        if '@' not in host:
            raise RuntimeError("correct host is user@ip")
        username, ip_address = host.split('@')
        # create sftp connection
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        look_for_keys = (password is None or len(password) == 0)
        self.ssh.connect(hostname=ip_address, port=port, username=username,
                         password=password, look_for_keys=look_for_keys, timeout=timeout)
        self.sftp = self.ssh.open_sftp()

    def check_path_type(self, path):
        try:
            attr = self.sftp.stat(path)
            if stat.S_ISDIR(attr.st_mode):
                return 'folder'
            elif stat.S_ISREG(attr.st_mode):
                return 'file'
            else:
                print(f"[ERROR] remote path is not directory or file: {path}")
                return None
        except Exception as err:
            print(f"[ERROR] remote not exits: {path}")
            return None

    def create_remote_directory(self, remote_dir):
        try:
            self.sftp.stat(remote_dir)
        except Exception as err:
            path, folder = os.path.split(remote_dir)
            self.create_remote_directory(path)
            self.sftp.mkdir(remote_dir)

class RsyncHelper:
    def __init__(self, host, port, local_root, remote_root, excludes=None, **kwargs):
        self.host = host
        self.port = port
        self.local_root = local_root.rstrip('/')
        self.remote_root = remote_root.rstrip('/')
        self.excludes = excludes or []
        self.password = kwargs.get('password')
        self.sftp = SftpClient(host, port, self.password)

        self.__delete = kwargs.get('delete', False)
        self.__progress = kwargs.get('progress', False)

    def pull(self, paths):
        """pull remote files to local"""
        if not paths:
            self.pull_every_path(self.remote_root + '/', self.local_root + '/')
        for path in paths:
            assert not path.startswith('/'), 'need relative path'
            path = path.rstrip('/')
            remote_path = os.path.abspath(os.path.join(self.remote_root, path))
            local_path = os.path.abspath(os.path.join(self.local_root, path))
            path_type = self.sftp.check_path_type(remote_path)
            if path_type == 'folder':
                os.makedirs(local_path, exist_ok=True)
                self.pull_every_path(remote_path + '/', local_path + '/')
            elif path_type == "file":
                dirname = os.path.dirname(local_path)
                os.makedirs(dirname, exist_ok=True)
                self.pull_every_path(remote_path, local_path)

    def pull_every_path(self, remote_path, local_path):
        print('rsync:', remote_path, '->', local_path)
        cmd = f'''rsync -rlptzve "ssh -p {self.port}" {self.host}:{remote_path} {local_path}'''
        for exclude in self.excludes:
            cmd += " --exclude {}".format(exclude)
        if self.__delete:
            cmd += " --delete"
        if self.__progress:
            cmd += " --progress"
        if self.password:
            cmd = f"sshpass -p {self.password} " + cmd
        shell(cmd)

    def push(self, paths):
        """push local files to remote"""
        if not paths:
            self.push_every_path(self.local_root + '/', self.remote_root + '/')
        for path in paths:
            assert not path.startswith('/'), 'need relative path'
            path = path.rstrip('/')
            local_path = os.path.abspath(os.path.join(self.local_root, path))
            remote_path = os.path.abspath(os.path.join(self.remote_root, path))
            if os.path.isdir(local_path):
                self.sftp.create_remote_directory(remote_path)
                self.push_every_path(local_path + '/', remote_path + '/')
            elif os.path.isfile(local_path):
                remote_dirname = os.path.dirname(remote_path)
                self.sftp.create_remote_directory(remote_dirname)
                self.push_every_path(local_path, remote_path)
            else:
                print('[ERROR] local_path not exits:', local_path)

    def push_every_path(self, local_path, remote_path):
        print('rsync:', local_path, '->', remote_path)
        cmd = f'''rsync -rlptzve "ssh -p {self.port}" {local_path} {self.host}:{remote_path}'''
        for exclude in self.excludes:
            cmd += " --exclude {}".format(exclude)
        if self.__delete:
            cmd += " --delete"
        if self.__progress:
            cmd += " --progress"
        if self.password:
            cmd = f"sshpass -p {self.password} " + cmd
        shell(cmd)

def config_parser(sub_parsers):
    p = sub_parsers.add_parser("rsync", help="rsync helper")
    p.add_argument('rsync_cmd', choices=["pull", "push"])
    p.add_argument('relative_paths', nargs='*', help='path1 path2 ...')
    p.add_argument('--host', default=None, help="username@ip")
    p.add_argument('--port', default=22, help="port")
    p.add_argument('--local', default=None, help="local root")
    p.add_argument('--remote', default=None, help="remote root")
    p.add_argument('--exclude', action='append', help='exclude pattern')
    p.add_argument('--config', default='', help='config file, rsync.yaml')
    p.add_argument('--delete', default=False, action='store_true', help='delete extraneous files from destination dirs')
    p.add_argument('--progress', default=False, action='store_true', help='show progress during transfer')
    p.set_defaults(func=execute)

def execute(args):
    conf = dict()
    if args.local and args.remote and args.host:
        # load config from argparse
        conf['local_root'] = args.local
        conf['remote_root'] = args.remote
        conf['host'] = args.host
        conf['port'] = args.port
        conf['exclude'] = args.exclude
    else:
        # check and load yaml config file
        if args.config:
            config_file = args.config
            if not os.path.exists(config_file):
                raise FileNotFoundError("Not found config '{}'".format(config_file))
            with open(config_file, 'r') as f:
                conf = yaml.safe_load(f)
        else:
            # check and load config file from local project
            workspaceFolder = os.getcwd()
            config_file = os.path.join(workspaceFolder, '.vscode/rsync.yaml')
            if not os.path.exists(config_file):
                raise FileNotFoundError("Not found config '{}'".format(config_file))
            with open(config_file, 'r') as f:
                yaml_conf = yaml.safe_load(f)
                if yaml_conf.get('local_root') is None:
                    raise KeyError("missed key 'local_root'")
                if yaml_conf['local_root'] != workspaceFolder:
                    raise KeyError("key 'local_root' in json_conf unmatched with workspaceFolder")
                conf.update(yaml_conf)

    rsync_helper = RsyncHelper(host=conf['host'],
                               port=conf['port'],
                               local_root=conf['local_root'],
                               remote_root=conf['remote_root'],
                               excludes=conf.get('exclude', None),
                               delete=args.delete,
                               progress=args.progress,
                               password=conf.get('password', None)
                               )
    if args.rsync_cmd == "pull":
        rsync_helper.pull(args.relative_paths)
    else:
        rsync_helper.push(args.relative_paths)
