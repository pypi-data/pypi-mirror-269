import paramiko
import os
import getpass

class SftpClient:
    def __init__(self, local_path, remote_path, host, password=None, port=22, timeout=10,
                 exclude=None, include=None, IdentityFile=None):
        assert os.path.exists(local_path), "local_path error: %s" % local_path
        self.local_path = os.path.abspath(local_path)
        self.remote_path = remote_path.rstrip('/')
        if '@' not in host:
            raise RuntimeError("host error: %s" % host)
        username, ip_address = host.split('@')
        if password == 'input':
            password = getpass.getpass("{}'s password: ".format(host))
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip_address, port=port, username=username,
                         password=password, look_for_keys=(not password), timeout=timeout, compress=True)
        self.sftp = self.ssh.open_sftp()

        # include hints
        self.enable_include_hint = True if include else False
        self.include_file_list = []  # 绝对路径
        self.include_paths = []
        if self.enable_include_hint:
            for hint in include:
                assert len(hint) >= 2, 'too short hint'
                if os.path.isfile(hint):
                    self.include_file_list.append(os.path.abspath(hint))
                else:
                    self.include_paths.append(hint)
            # info_str = "include:"
            # for p in self.include_file_list:
            #     info_str += "\n  " + p
            # for p in self.include_paths:
            #     info_str += "\n  " + p
            # print(info_str)
        # exclude hints
        self.enable_exclude_hint = True if exclude else False
        self.exclude_file_list = []  # 绝对路径
        self.exclude_paths = []
        if self.enable_exclude_hint:
            for hint in exclude:
                assert len(hint) >= 2, 'too short hint'
                if os.path.isfile(hint):
                    self.exclude_file_list.append(os.path.abspath(hint))
                else:
                    self.exclude_paths.append(hint)
            info_str = "exclude:"
            for p in self.exclude_file_list:
                info_str += "\n  " + p
            for p in self.exclude_paths:
                info_str += "\n  " + p
            print(info_str)

    def exclude_file(self, local_file_path, file):
        """priority is file list > path > extension """
        if not self.enable_exclude_hint:
            return 0
        if local_file_path in self.exclude_file_list:
            return 1
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

    def include_file(self, local_file_path, file):
        """priority is file > path > extension, must provide path when specify extension
        Return:
            0 - not subject to exclude filtering rules
            1 - include by regex. subject to exclude filtering rules
            2 - not included
        """
        if not self.enable_include_hint:
            return 1
        if local_file_path in self.include_file_list:
            return 2
        for path_regex in self.include_paths:
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

    def put(self):
        self.create_remote_directory(self.remote_path)
        # 根据过滤条件进行文件传输
        for root, dirs, files in os.walk(self.local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                include_state = self.include_file(local_file_path, file)
                # print(include_state)
                if include_state == 0:
                    continue
                if include_state == 1 and self.exclude_file(local_file_path, file):
                    continue
                remote_file_path = os.path.join(self.remote_path, os.path.relpath(local_file_path, self.local_path))
                self.create_remote_directory(os.path.dirname(remote_file_path))
                self.upload(local_file_path, remote_file_path)
        # 关闭连接
        self.sftp.close()
        self.ssh.close()

    def create_remote_directory(self, remote_dir):
        try:
            self.sftp.stat(remote_dir)
        except Exception as err:
            path, folder = os.path.split(remote_dir)
            self.create_remote_directory(path)
            self.sftp.mkdir(remote_dir)

    def upload(self, local_file, remote_file):
        # compare remote and local file state
        local_stat = os.stat(local_file)
        try:
            remote_stat = self.sftp.stat(remote_file)
            if local_stat.st_size == remote_stat.st_size and abs(local_stat.st_mtime - remote_stat.st_mtime) < 1.0:
                return
        except Exception as err:
            pass
        print(f"upload: {local_file} -> {remote_file}")
        self.sftp.put(local_file, remote_file)
        self.sftp.utime(remote_file, (local_stat.st_atime, local_stat.st_mtime))

def deploy(
        host, local_path, remote_path, password=None,
        port=22, include=None, exclude=None, IdentityFile=None):
    """api for python scripts"""
    client = SftpClient(
        host=host,
        local_path=local_path,
        remote_path=remote_path,
        password=password,
        port=port,
        exclude=exclude,
        include=include,
        IdentityFile=IdentityFile,
    )
    client.put()
