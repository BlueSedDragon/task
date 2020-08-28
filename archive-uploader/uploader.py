#!/usr/bin/env python3

import os
import time
import json

try:
    from internetarchive import get_session
except ImportError as err:
    print(os.system('pip3 install internetarchive'))
    raise err

ROOT = os.path.abspath('/tmp/code/')

PACKAGES = tuple({
    'apt', 'make', 'cmake', 'vim', 'nano', 'systemd', 'busybox',
    'coreutils', 'vlc', 'gimp', 'firefox', 'firefox-esr', 'chromium',
    'binutils', 'git', 'zip', 'unzip', 'gzip', 'tar', 'i2p', 'tor',
    'iptables', 'ufw', 'curl', 'wget', 'htop', 'bash', 'fish', 'zsh',
    'dash', 'python', 'python3.7', 'python2.7', 'lua5.3', 'perl', 'iperf', 'iperf3',
    'openjdk-11-jdk', 'yum', 'p7zip', 'adb', 'rustc', 'gcc', 'gcc-8', 'g++', 'g++-8',
    'llvm', 'llvm-7', 'gawk', 'mawk', 'openssl', 'openssh', 'dropbear',
    'bc', 'cron', 'systemd-cron', 'golang', 'golang-1.14', 'cpp', 'cpp-8', 'dpkg', 'emacs',
    'less', 'tree', 'gpg', 'grep', 'grub', 'grub2', 'dnsutils', 'knot-dnsutils', 'sudo',
    'net-tools', 'hexedit', 'jq', 'netcat', 'socat', 'nmap', 'wireshark', 'tcpdump',
    'nodejs', 'gdb', 'xz-utils', 'ca-certificates', 'dnsmasq', 'php', 'php7.3', 'php-fpm',
    'php-cgi', 'mtr', 'traceroute', 'ruby', 'ruby2.7', 'bzip2', 'lzip', 'lz4', 'nginx',
    'apache2', 'libreoffice',

    'inetutils', 'parted', 'gparted', 'mailman', 'hello', 'autoconf', 'autogen', 'automake',
})
CONFIG = json.load(open('./config.json', 'r'))

SESSION = None


def new_session():
    global SESSION

    if SESSION is not None:
        raise Exception('have another session!')

    SESSION = get_session(config=CONFIG)


def get_directory(name):
    return f'{ROOT}/{name}'


def get_files(walk):
    files = {}

    dirname = walk[0]
    in_files = walk[2]
    for fn in in_files:
        abs_fn = f'{dirname}/{fn}'

        fn = valid_name(fn)
        files[fn] = abs_fn

    return files


def valid_name(name):
    for it in ['+', '~']:
        name = name.replace(it, '-')
    return name


def get_source():
    for name in PACKAGES:
        command = f'bash ./get_source.sh {name}'
        try:
            status = os.system(command)
            if status != 0:
                raise Exception(f'command {command}: Error {status}')
        except BaseException as err:
            print(repr(err))
            continue

        ls = f'{ROOT}/{name}/'
        walk = next(os.walk(ls))
        files = get_files(walk)

        version = None
        for it in walk[2]:
            if not it.endswith('.dsc'):
                continue

            it = it.split('.dsc')[0]
            it = it.split('_')[1]
            version = it
            break

        while True:
            print('files:', files)

            title = f'source code of {name} (version: {version})'
            print('title:', title)

            if input('is version right? ').lower() == 'yes':
                break
            version = input('please input version: ')

        f_version = valid_name(version)
        f_name = valid_name(name)

        timestamp = int(time.time())
        info = {
            'idname': f'{f_name}-{f_version}',
            'metadata': {
                'title': title,
                'time': time.ctime(timestamp),
                'timestamp': str(timestamp),
                'name': name,
                'version': version,
                'command': f'apt source {name}'
            },
            'files': files
        }
        yield info


def upload(idname, files, metadata):
    if SESSION is None:
        raise Exception('no session!')

    item = SESSION.get_item(idname)

    if item.exists:
        raise Exception('item exists!')

    result = item.upload(files, metadata=metadata,
                         verify=True, verbose=True)
    return result


results = {}


def main():
    new_session()
    for info in get_source():
        print('UPLOAD:', info)

        try:
            result = upload(**info)
        except BaseException as err:
            print(repr(err))
            continue

        print(result)

        name = info['metadata']['name']
        results[name] = result


main()
