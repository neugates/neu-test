import paramiko


class Remote:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.trans = paramiko.Transport((self.host, self.port))

    def connect(self):
        self.ssh.connect(hostname=self.host, port=self.port,
                         username=self.username, password=self.password)
        self.trans.connect(username=self.username, password=self.password)

    def close(self):
        self.trans.close()
        self.ssh.close()

    def exe_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.readlines()

    def upload(self, local_path, remote_path):
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        sftp.put(local_path, remote_path)

    def download(self, remote_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        sftp.get(remote_path, local_path)
