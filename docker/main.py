#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.docker import Container, Image, DockerProvider

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here
        DockerProvider(self, "default")

        dockerImage = Image(self, "nginxImage", name = "nginx:latest", keep_locally = False)

        Container(self, "nginxContainer", image =  dockerImage.latest, name = "tutorial",
        ports = [
            {
            'internal' : 80,
            'external' :8000,
            }
            ]
        )

app = App()
MyStack(app, "docker")

app.synth()
