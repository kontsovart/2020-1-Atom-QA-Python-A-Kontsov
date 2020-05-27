import requests
import argparse
import sys
from time import sleep


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url')
    parser.add_argument('-t', '--timeout')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    time = int(namespace.timeout)
    while time > 0:
        try:
            sleep(1)
            requests.get(namespace.url)
        except Exception as e:
            time -= 1
            continue
        break
