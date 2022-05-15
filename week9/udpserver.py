import os
import socket

FLAGS = _ = None
DEBUG = False


def get_filedict(rootpath):
    files = {}
    with os.scandir(rootpath) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                info = get_fileinfo(entry.path)
                info['path'] = entry.path
                files[entry.name] = info
    return files


def get_fileinfo(path):
    size = 0
    value = None
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(FLAGS.mtu)
            chunk_size = len(chunk)
            if chunk_size == 0: # if not data:
                break
            size = size + chunk_size
    return {'size': size}
def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    files = get_filedict(FLAGS.files)
    if DEBUG:
        print(f'Ready to file transfer')
        for key, value in files.items():
            print(f'{key}: {value}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))
    print(f'Listening on {sock}')
    while True:
        try:
            data, client = sock.recvfrom(FLAGS.mtu)
            data = data.decode('utf-8')
            data = data.split(' ')

            if len(data) < 2:
                response = 'Error'
                sock.sendto(response.encode('utf-8'), client)
                continue

            command = data[0].upper()
            target = ' '.join(data[1:])
            print(f'{command} {target} from {client}')


            if target not in files.keys():
                print(f'{target} was not found (requested by {client})')
                response = '404 Not Found'
                sock.sendto(response.encode('utf-8'), client)
                continue

            info = files[target]
            path = info['path']
            size = info['size']
            if command == 'INFO':
                upstream = str(size)
                sock.sendto(upstream.encode('utf-8'), client)
                print('File info sended')
            elif command == 'DOWNLOAD':
                remain = size
                with open(path, 'rb') as f:
                    while remain > 0:
                        chunk = f.read(FLAGS.mtu)
                        sock.sendto(chunk, client)
                        remain = remain - FLAGS.mtu
                print(f'File transfer complete {target}')
                break
        except KeyboardInterrupt:
            print(f'Shutting down... {sock}')
            break

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='localhost',
                        help='The address to serve service')
    parser.add_argument('--port', type=int, default=40806,
                        help='The port to serve service')
    parser.add_argument('--mtu', type=int, default=2**16,
                        help='The maximum transmission unit')
    parser.add_argument('--files', type=str, default='./files',
                        help='The file directory path')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    FLAGS.files = os.path.abspath(os.path.expanduser(FLAGS.files))

    main()

