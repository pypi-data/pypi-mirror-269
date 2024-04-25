import paramiko
import os
import getpass
from .remote_manager import RemoteDeviceManager
from typing import List
import stat

class SftpClient:
    def __init__(self, local_root: str, remote_paths: List[str], host, password=None, port=22, timeout=10,
                 exclude=None, IdentityFile=None):
        self.local_root = local_root
        self.remote_paths = remote_paths
        if '@' not in host:
            raise RuntimeError("correct host is user@ip")
        username, ip_address = host.split('@')
        if password == 'input':
            password = getpass.getpass("{}'s password: ".format(host))
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        look_for_keys = (password is None or len(password) == 0)
        self.ssh.connect(hostname=ip_address, port=port, username=username,
                         password=password, look_for_keys=look_for_keys, timeout=timeout, compress=True)
        self.sftp = self.ssh.open_sftp()

        # exclude hints
        self.exclude_paths = exclude or []
        info_str = "exclude:\n"
        for p in self.exclude_paths:
            info_str += f'  {p}\n'
        print(info_str)

    def check_exclude_file(self, local_file_path, file):
        """priority is file list > path > extension """
        if not self.exclude_paths:
            return 0
        for path_regex in self.exclude_paths:
            key, ext = path_regex, None
            if "*" in path_regex:
                key, ext = path_regex.split("*")
                # print(key, ext, local_file_path)
            if key in local_file_path:
                if ext:
                    _, extension = os.path.splitext(file)
                    if extension == ext:
                        return 1
                else:
                    return 1
        return 0

    def download(self):
        if not os.path.exists(self.local_root):
            print(f"[ERROR] local_path not exist: {self.local_root}")
            self.sftp.close()
            self.ssh.close()
            exit(1)

        for remote_path in self.remote_paths:
            remote_path = remote_path.rstrip('/')  # drop right slash of path
            if '/*' in remote_path:
                # download files by match pattern
                remote_path, matched_ext = remote_path.split('/*')
                if matched_ext:
                    # when remote_path=.../path/*.txt
                    self.download_dir(remote_path, self.local_root, recursive=False, include_ext_list=[matched_ext])
                else:
                    # when remote_path=.../*
                    self.download_dir(remote_path, self.local_root)
                continue
            # download file and folder
            type_p = self.check_path_type(remote_path)
            if type_p == 'file':
                local_file = os.path.join(self.local_root, os.path.basename(remote_path))
                self.download_sync(remote_path, local_file)
            elif type_p == 'folder':
                local_path = os.path.join(self.local_root, os.path.basename(remote_path))
                self.download_dir(remote_path, local_path)
        # 关闭连接
        self.sftp.close()
        self.ssh.close()

    def download_dir(self, remote_dir, local_dir, recursive=True, include_ext_list=None):
        """download directory
        Args:
            include_ext_list: only files ends witch extensions in include_ext can be downloaded
            recursive: walk through all subdirectories
        """
        for item in self.sftp.listdir_attr(remote_dir):
            remote_path = f'{remote_dir}/{item.filename}'
            local_path = os.path.join(local_dir, item.filename)
            if stat.S_ISDIR(item.st_mode):
                if recursive:
                    self.download_dir(remote_path, local_path)
            else:
                if include_ext_list and (os.path.splitext(item.filename)[-1] not in include_ext_list):
                    continue
                if self.check_exclude_file(local_path, item.filename):
                    continue
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                self.download_sync(remote_path, local_path)

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

    def download_sync(self, remote_file, local_file):
        # compare remote and local file state
        try:
            local_stat = os.stat(local_file)
            remote_stat = self.sftp.stat(remote_file)
            if remote_stat.st_size == local_stat.st_size and remote_stat.st_mtime <= local_stat.st_mtime:
                return
        except Exception as err:
            pass  # new file to sync
        print(f"download: {remote_file} -> {local_file}")
        self.sftp.get(remote_file, local_file)

def config_parser(sub_parsers):
    p = sub_parsers.add_parser("get", help="download files from remote with sftp")
    p.add_argument('remote', type=str, help='remote_name, usrname@ip_address')
    p.add_argument('paths', nargs='+', help='path1 path2 ..., the last is local_path when length>=2')
    p.add_argument('--password', type=str, help='specify or input')
    p.add_argument('-p', '--port', type=int, help='remote port', default=22)
    p.add_argument('--exclude', nargs='+', help='paths, files or extensions to filter')
    p.set_defaults(func=execute)

def execute(args):
    # print(args)
    """api for download files by sftp transformer"""
    assert len(args.paths) >= 2, 'the last path is local_root'
    remote_manager = RemoteDeviceManager()
    device = remote_manager.get_device(args.remote)
    host, password, port, IdentityFile = args.remote, args.password, args.port, None
    if device is not None:
        host, password, port, IdentityFile = device.host, device.password, device.port, device.IdentityFile
        
    client = SftpClient(
        local_root=args.paths[-1],
        remote_paths=args.paths[:-1],
        host=host,
        password=password,
        port=port,
        exclude=args.exclude,
        IdentityFile=IdentityFile
    )
    client.download()
