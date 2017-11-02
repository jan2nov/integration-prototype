# coding: utf-8
""" Script using multiprocessing to start multiple mock log publishers.
"""
from multiprocessing import Pool
from subprocess import call


def run_publisher(name):
    call(['python3', '-m', 'sip.zmq_logging_aggregator.mock_log_publisher',
          'pub_{:02d}'.format(name)])


def main():
    pool = Pool(20)
    pool.map(run_publisher, range(20))


if __name__ == '__main__':
    main()
