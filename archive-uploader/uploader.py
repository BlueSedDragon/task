import os
import time

try:
    from internetarchive import get_session
except ImportError as err:
    print(os.system('pip3 install internetarchive'))
    raise err

ROOT = os.path.abspath('/tmp/code/')
PACKAGES = tuple({
        #'apt', 'bash', 'make', 'curl', 'wget', 'rustc',
        #'nano', 'cargo', 'gzip', 'tar',
        #'dpkg',
    })

S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''

CONFIG = {
        's3': {
            'access': S3_ACCESS_KEY,
            'secret': S3_SECRET_KEY
        }
}

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

        fn = fn.replace('+', '-')
        files[fn] = abs_fn

    return files

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

        version = version.replace('+', '-')

        info = {
                'idname': f'{name}-{version}',
                'metadata': {
                    'title': title,
                    'date': time.ctime()
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

    result = item.upload(files, metadata=metadata, checksum=True, verify=True, verbose=True)
    return result

results = []
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
        results.append(result)

main()

