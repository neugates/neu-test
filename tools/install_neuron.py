import argparse

import remote


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=str, help="version")
    parser.add_argument("-a", "--arch", type=str, help="arch")
    return parser.parse_args()


default_directory = '/tmp'
ip = '192.168.10.111'
port = 22
user = 'root'
password = '3onedata'

args = parse_args()

remote = remote.Remote(ip, port, user, password)
remote.connect()
remote.exe_command('rm -rf /etc/config_partition/app/neuron/')
remote.exe_command(
    'tar xvf /tmp/neuron-%s-linux-%s.tar  -C /etc/config_partition/app' % (args.version, args.arch))
