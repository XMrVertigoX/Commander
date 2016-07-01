import sys

from docker import Client
from pathlib import Path


class DockerController():

    def __init__(self, root):
        self.workingDirectory = Path('/host')
        self.projectDirectory = Path(self.workingDirectory,
                                     Path().resolve().relative_to(root))

        self.client = Client(base_url='tcp://127.0.0.1:2375')

        binds = ['{0}:{1}'.format(root, self.workingDirectory.as_posix())]

        self.hostConfig = self.client.create_host_config(binds=binds)

    def prepare(self, image, command):
        self.container = self.client.create_container(
            image=image,
            command=command,
            volumes=self.workingDirectory.as_posix(),
            working_dir=self.projectDirectory.as_posix(),
            host_config=self.hostConfig)

    def run(self):
        self.client.start(self.container)

        logs = self.client.logs(self.container, stream=True)

        for line in logs:
            sys.stdout.write(str(line, encoding='UTF-8'))

        self.client.wait(self.container)
