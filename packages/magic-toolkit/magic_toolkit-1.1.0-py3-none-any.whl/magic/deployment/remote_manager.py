import os
import magic
from typing import List
from magic.proto.remote_config_pb2 import RemoteDeviceConfig, RemoteDevice
from google.protobuf import text_format

class Device:
    def __init__(self, name, ip, username, password, port, IdentityFile, description):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.IdentityFile = IdentityFile
        self.description = description

    @property
    def host(self):
        return self.username + '@' + self.ip

    def __repr__(self):
        string = str(self.host) + '\n'
        string += '  name: {}\n'.format(self.name)
        string += '  ip: {}\n'.format(self.ip)
        string += '  username: {}\n'.format(self.username)
        if self.password:
            string += '  password: {}\n'.format(self.password)
        if self.port:
            string += '  port: {}\n'.format(self.port)
        if self.IdentityFile:
            string += '  IdentityFile: {}\n'.format(self.IdentityFile)
        if self.description:
            string += '  description: {}\n'.format(self.description)
        return string

class RemoteDeviceManager:
    def __init__(self, default_port=22):
        self.remote_devices: List[Device] = []
        self.default_port = default_port
        self.remote_config_file = os.path.join(magic.config_root, 'remote_device.pt')

        if not os.path.exists(self.remote_config_file):
            # create a template of config file
            os.makedirs(magic.config_root, exist_ok=True)
            device = Device('name', '0.0.0.0', 'username', 'password', self.default_port, '', 'description')
            self.remote_devices.append(device)
            self.dump_device_conf()

        # parse device config file
        remote_conf = RemoteDeviceConfig()
        with open(self.remote_config_file, 'r') as f:
            text_format.Parse(f.read(), remote_conf)

        for device_conf in remote_conf.device:
            device = Device(
                name=device_conf.name,
                ip=device_conf.ip,
                username=device_conf.username,
                password=device_conf.password,
                port=device_conf.port,
                IdentityFile=device_conf.IdentityFile,
                description=device_conf.description
            )
            assert len(device.name), 'device name is empty'
            assert len(device.ip), 'device ip is empty'
            assert len(device.username), 'device username is empty'
            device.port = device.port or self.default_port
            for device_registered in self.remote_devices:
                if device.name == device_registered.name:
                    raise RuntimeError("device already exists, name: ".format(device.name))
                if device.host == device_registered.host:
                    raise RuntimeError("device already exists, host: ".format(device.host))
            self.remote_devices.append(device)

        if not self.remote_devices:
            print('[WARN] remote_device.pt is empty')

    def list_all_devices(self):
        msg_fmt = '{:<25} {} \t {}'
        print(msg_fmt.format('name', 'ssh-connection', ''))
        device_list = sorted(self.remote_devices, key=lambda x: x.name, reverse=False)
        for device in device_list:
            ssh_connection = f"ssh -p {device.port} {device.username}@{device.ip}"
            msg = msg_fmt.format(device.name[:25], ssh_connection, device.description)
            print(msg)

    def get_device(self, key):
        """ get device by name, host """
        for device in self.remote_devices:
            if key in [device.name, device.host]:
                return device
        return None

    def dump_device_conf(self):
        # dump device config to remote_device.pt
        remote_conf = RemoteDeviceConfig()
        for device in self.remote_devices:
            device_conf = RemoteDevice()
            device_conf.name = device.name
            device_conf.ip = device.ip
            device_conf.username = device.username
            device_conf.password = device.password
            device_conf.port = device.port
            device_conf.IdentityFile = device.IdentityFile
            device_conf.description = device.description
            remote_conf.device.append(device_conf)
            with open(self.remote_config_file, 'w') as f:
                text_format.PrintMessage(remote_conf, f)
