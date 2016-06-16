import sys

from argparse import ArgumentParser
from docker import Client
from pathlib import Path


class DockerCommander():
    image = 'mrvertigo/archlinux-dev:latest'
    root = Path('C:/Users/caspa/Projects').resolve()

    workingDirectory = Path('/projects')
    projectDirectory = Path(
        workingDirectory, Path().resolve().relative_to(root))

    def __init__(self):
        self.client = Client(base_url='tcp://127.0.0.1:2375')
        self.hostConfig = self.client.create_host_config(
            binds=['{0}:{1}'.format(self.root,
                                    self.workingDirectory.as_posix())])

    def run(self, command):
        container = self.client.create_container(
            image=self.image,
            command=command,
            volumes=self.workingDirectory.as_posix(),
            working_dir=self.projectDirectory.as_posix(),
            host_config=self.hostConfig)

        self.client.start(container)

        logs = self.client.logs(container, stream=True)

        for line in logs:
            sys.stdout.write(str(line, encoding='UTF-8'))

        self.client.wait(container)


def main(args):
    docker = DockerCommander()

    if args['command'] == 'build':
        docker.run('make -j')
    elif args['command'] == 'clean':
        docker.run('make clean')
    else:
        print("Unknown command")


def getArguments():
    parser = ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    return vars(args)

if __name__ == '__main__':
    main(getArguments())
