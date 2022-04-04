#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.docker import Container, Image, DockerProvider

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here


app = App()
MyStack(app, "docker")

app.synth()