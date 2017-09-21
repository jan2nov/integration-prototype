# coding: utf-8
"""Script to write to a file.

This is intended to be used for testing file writing behaviour of docker
containers. See run options in the Dockerfile comments.
"""
import time
import sys
import os
import socket
import ntplib


def main():
    """."""
    file_name = sys.argv[1] if len(sys.argv) >= 2 else \
        'temp_{}.txt'.format(socket.gethostname())
    output_dir = 'output'
    if not os.path.isdir(output_dir):
        raise RuntimeError('Output directory missing, expecting directory: {}'
                           .format(output_dir))
    file_path = os.path.join(output_dir, file_name)
    file_name_root = os.path.splitext(file_path)[0]
    counter = 1
    while True:
        if os.path.exists(file_path):
            file_path = '{}.{:02d}.txt'.format(file_name_root, counter)
            print('-- Output file already exists ... Trying %s' % file_name)
            counter += 1
        else:
            break

    file_ = open(file_path, 'w')
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')

    print('Writing to file: %s' % file_path)
    local_time = time.localtime(response.tx_time)
    c_time = str(time.ctime(response.tx_time))
    file_.write('The time is %s (%s)\n' %
                (time.strftime('%m%d%H%M%Y.%S', local_time), c_time))
    counter = 0
    time_out = 100  # seconds
    elapsed = 0
    start_time = time.time()
    try:
        while True:
            file_.write('Hello from %s ... %-3i (%.2f s)\n' %
                        (socket.gethostname(),
                         counter,
                         elapsed))
            file_.flush()
            time.sleep(0.1)
            elapsed = (time.time() - start_time)
            counter += 1
            counter = counter % 1e3
            if elapsed > time_out:
                print('Time out reached!')
                break
    except KeyboardInterrupt:
        print('Interupdated! counter = %i' % counter)

    file_.close()


if __name__ == '__main__':
    main()
