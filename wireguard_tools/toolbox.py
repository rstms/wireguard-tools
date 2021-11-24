#!/usr/bin/env python3

import io
import subprocess
from pprint import pprint

class Toolbox():

    DOCKERFILE = """
        FROM alpine:3.14
        RUN apk update && apk add wireguard-tools
    """

    IMAGE = 'wireguard-toolbox'

    def __init__(self, output_hook=pprint):
        self.output_hook = output_hook
        self.image = f'{self.IMAGE}:latest'
        docker_build = ['docker', 'build', '-q', '-t', self.IMAGE, '-' ]
        self.log(self.exec(docker_build, input_stream=self.DOCKERFILE))

    def exec(self, cmd, input_stream=None):
        self.log(f"{self}: {cmd}")
        ret = subprocess.run(cmd, input=input_stream, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True, text=True)
        self.log(f"{self}: {ret.stdout.strip()}")
        return ret.stdout.strip()

    def log(self, msg):
        self.output_hook(msg)

    def docker_run(self, cmd):
        docker_command = ['docker', 'run', '--rm', self.image] 
        docker_command.extend(cmd)
        return self.exec(docker_command)

    def make_private_key(self):
        return self.docker_run(['wg', 'genkey'])

    def make_public_key(self, private_key):
        return self.docker_run(['sh', '-c', f"echo '{private_key}' | wg pubkey"])

    def make_preshared_key(self):
        return self.docker_run(['wg', 'genkey'])

    def make_keys(self):
        private = self.make_private_key()
        public = self.make_public_key(private)
        psk = self.make_preshared_key()
        return private, public, psk
