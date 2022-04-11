#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, Fn
from imports.google import GoogleProvider, DataGoogleComputeImage, ComputeInstance, ComputeInstanceBootDisk,ComputeInstanceBootDiskInitializeParams,ComputeInstanceNetworkInterface

class GcpBasicVmStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        #variables


        #set project name
        GCP_PROJECT_NAME = "PROJECT-NAME"

        #Set Credentials for Provider
        creds = open("<FILE-NAME>", "r").read()
        GoogleProvider(self,id=GCP_PROJECT_NAME, region="us-east1", project=GCP_PROJECT_NAME, credentials = creds)

        #Query a GCP Image filtered by Family        
        gcp_image = DataGoogleComputeImage(self, id = "windows_image", family = "windows-2019", project="windows-cloud" )

        #Get the network interface
        net_int = ComputeInstanceNetworkInterface(subnetwork ="<SUBNETWORK>",subnetwork_project = "<SHARED-VPC-PROJECT>")

        #Create a new vm
        instance = ComputeInstance(self,id = "windows_vm", machine_type="e2-standard-4", name="cdktf-instance-1", 
                        boot_disk= ComputeInstanceBootDisk(initialize_params=ComputeInstanceBootDiskInitializeParams(image=gcp_image.name)),
                        network_interface=[net_int], zone= "us-east4-a"
        )

        #Output 
        TerraformOutput(self, "image-name",value=gcp_image.name)
        #TerraformOutput(self, "instance_ip", instance.network_interface[0].network_ip)
        TerraformOutput(self, "instance_ip", value=Fn.lookup(Fn.element(instance.network_interface, 0), "network_ip","default"))

app = App()
GcpBasicVmStack(app, "gcp")

app.synth()
