#!/bin/python
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

from hetznercloud import HetznerCloudClientConfiguration, HetznerCloudClient
import ocf

class FloatingIp(ocf.ResourceAgent):
    def __init__(self):
        ocf.ResourceAgent.__init__(self, 'floating_ip', '0.1.0', 'Manage Hetzner Cloud Floating Ips',
                '''
                This resource agent uses the hetzner cloud api and to manage a floating ip address.

                IMPORTANT: This resource agent assumes that the hostname of the target cluster member
                is the same as its name in the cloud api.

                It does NOT manage adding the ip address to the network interface. You should either
                add it permanently to your network adapter by setting it in /etc/network/interfaces,
                /etc/netplan/* or in NetworkManager OR you could use a second resource of type IPAddr2
                with the address and set at least two constraints:
                colocation ip address with floating ip
                order start ip address after floating ip
                ''')

        self.floatingIp = ocf.Parameter('floating_ip', shortDescription='Hetner Cloud Ip-Address x.x.x.x' ,
                description='''
                The Hetzner Cloud Floating Ip Address which this resource should manage.
                Note that this does not mean the Id of the Ip-Address but the Address
                itself.
                ''',
                required=True, unique=True)
        self.apiToken = ocf.Parameter('htoken', shortDescription='Hetner Cloud api token' ,
                description='''
                The Hetzner Cloud api token with which the ip address can be managed.

                You can create this in the Hetner Cloud Console. Select the project
                which contains your Ip-Address, then select `Access` on the leftside menu
                Activate the second tab `Api Tokens` and create a new token.
                ''',
                required=True, unique=False)
        self.parameters = [
                self.floatingIp,
                self.apiToken
        ]

    def getParameters(self):
        return self.parameters

    def makeClient(self):
        configuration = HetznerCloudClientConfiguration().with_api_key( self.apiToken.get() ).with_api_version(1)
        client = HetznerCloudClient(configuration)
        return client


    def start(self):
        print 'Start!'

    def stop(self):
        print 'Stop!'

    def monitor(self):
        print 'Monitor!'
