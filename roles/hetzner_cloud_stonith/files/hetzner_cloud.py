#!/bin/python
#
#   Resource Agent for managing hetzner cloud ips
#
#   License:      MIT
#   (c) 2018Sven Speckmaier

import os
import sys
from lxml import etree as Et
import hetznercloud

class OCfReturnCodes:
    success = 0
    genericError = 1
    invalidArguments = 2
    isNotImplemented = 3
    hasInsufficientPermissions = 4
    isMissingRequiredComponent = 5
    isMissconfigured = 6
    isNotRunning = 7
    isRunningMaster = 8
    isFailedMaster = 9

class OcfApi:
    def action(self):
        return sys.argv[1]
    def variable(self, name):
        os.environ.get('OCF_RESKEY_'+name)
    def meta(self, name):
        converted_name = name.replace('-','_')
        os.environ.get('OCF_RESKEY_CRM_meta_'+converted_name)

class OcfPopulater:
    def init(self):
        self.api = OcfApi()
    def populate(self, resource):
        for parameter in resource.getParameters():
            value = self.api.getVariable( parameter.getName() )
            if resource.isRequired():
                assert value != ''
            if not value:
                value = parameter.getDefault()
                
            parameter.set(value)

class OcfAgent:
    def init(self, name, version):
        self.name = name
        self.version  = version
        self.parameters = []
        self.languages = []

class OcfParameter:
    def init(self, name, shortDescription='', description='', default='', unique=False, required=False):
        self.name = name
        self.default = default
        self.shortDescription = shortDescription
        self.description = description
        self.unique = unique
        self.required = required

    def name(self):
        return self.name
    def default(self):
        return self.default
    def isRequired(self):
        return self.required
    def isUnique(self):
        return self.unique
    def getShortDescription():
        return self.shortDescription
    def getDescription():
        return self.getDescription

class ResourceAgent:
    def init(self):
        self.populater = OcfPopulater()

    def notImplemented(self):
        return OCfErrors.notImplemented

    def metaData(self, resource):
        root = ET.Element('resource-agent')
        root.set('name', resource.name)
        root.set('version', resource.version)
        version = ET.SubElement(root, 'version')
        version.text = resource.version
        shortdesc = ET.SubElement(root, 'shortdesc')
        shortdesc.text = resource.shortDescription
        longdesc = ET.SubElement(root, 'longdesc')
        longdesc.text = resource.longDescription
            
        parametersNode = ET.SubElement(root, 'parameters')
        for parameter in resource.getParameters():
            parameterNode = ET.SubElement(parametersNode, 'parameter')
            parameterNode.set('name', parameter.getName())
            content = ET.SubElement(parameterNode, 'content')
            content.set('type', parameter.getType())

            longDesc = ET.SubElement(parameterNode, 'longdesc')
            longDesc.text = resource.getLongDescription()
            ShortDesc = ET.SubElement(parameterNode, 'shortdesc')
            ShortDesc = resource.getShortDescription()

            parameterNode.set('unique', '0')
            try:
                if parameter.isUnique():
                    parameterNode.set('unique', '1')
            except AttributeError:
                pass

            parameterNode.set('required', '0')
            try:
                if parameterNode.isRequired():
                    parameterNode.set('required', '1')
            except AttributeError:
                pass

        actions = ['start', 'stop', 'monitor', 'meta-data', 'validate-all'
                'reload', 'migrate_to', 'migrate_from', 'promote', 'demote']
        for action in actions:
            try:
                resource.action
            except AttributeError:
                pass

        tree = Et.ElementTree(root)
        print ET.tostring(tree, encoding="UTF-8",
                     xml_declaration=True,
                     pretty_print=True,
                     doctype='<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">')

    def validate(self, resource):

        self.populater.populate(resource)

        for item in resource.getParameters():
            item.validate()
            
        try:
            resource.validate()
        except AttributeError:
            pass

        return 0 

    def run(self, resource, action):
        self.populater.populate(resource)

        actions = {}
        try:
            actions.update({"start": resource.start})
        except AttributeError:
            pass

        try:
            actions.update({"stop": resource.stop})
        except AttributeError:
            pass

        try:
            actions.update({"monitor": resource.monitor})
            actions.update({"status": resource.monitor})
        except AttributeError:
            pass

        actions.update({
            "promote": getattr(resource, 'promote', self.notImplemented),
            "demote": getattr(resource, 'demote', self.notImplemented),
            "migrate_to": getattr(resource, 'migrateTo', self.notImplemented),
            "migrate_from": getattr(resource, 'migrateFrom', self.notImplemented),
            "meta-data": lambda : self.metaData(resource),
            "validate-all": lambda : self.validate(resource),
        })

        try:
            actionMethod = actions[action]
            return actionMethod()
        except KeyError:
            return OCfReturnCodes.isNotImplemented

class HCloudFloatingIp:
    def init(self):
        self.parameters = [
            OcfParameter('floating_ip', overview='Hetner Cloud Ip-Address x.x.x.x' ,
                descrpition='''
                The Hetzner Cloud Floating Ip Address which this resource should manage.
                Note that this does not mean the Id of the Ip-Address but the Address
                itself.
                ''',
                required=True, unique=True),
            OcfParameter('htoken', overview='Hetner Cloud api token' ,
                descrpition='''
                The Hetzner Cloud api token with which the ip address can be managed.

                You can create this in the Hetner Cloud Console. Select the project
                which contains your Ip-Address, then select `Access` on the leftside menu
                Activate the second tab `Api Tokens` and create a new token.
                ''',
                required=True, unique=False)
        ]
    def getParameters(self):
        return self.parameters

    def start(self):
        print 'Start!'

    def stop(self):
        print 'Stop!'

    def monitor(self):
        print 'Monitor!'

application = ResourceAgent()
resource = HCloudFloatingIp()
api = OcfApi()

try:
    code = application.run(resource, api.action()) 
except AssertionError:
    code = OCfReturnCodes.isMissconfigured
sys.exit( code )
