from argparse import ArgumentParser
from pathlib import Path

from dockercontroller import DockerController


def main(args):
    docker = DockerController(Path('D:/Projects').resolve())

    if args['command'] == 'build':
        docker.prepare(image='mrvertigo/archlinux-dev:latest',
                       command='make -s -j')
        docker.run()

    elif args['command'] == 'clean':
        docker.prepare(image='mrvertigo/archlinux-dev:latest',
                       command='make -s clean')
        docker.run()

    elif args['command'] == 'flash':
        docker.prepare(image='mrvertigo/archlinux-dev:latest',
                       command='ip link')
        docker.run()


def getArguments():
    parser = ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    return vars(args)

if __name__ == '__main__':
    args = getArguments()
    main(args)
