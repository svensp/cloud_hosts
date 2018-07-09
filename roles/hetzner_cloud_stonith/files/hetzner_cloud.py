#!/bin/python

import os
import sys
from lxml import etree as Et

def OCfErrors:
    notImplemented = 1

def OcfApi:
    def action():
        return sys.argv[1]
    def variable(self, name)
        os.environ.get('OCF_RESKEY_'+name)
    def meta(self, name):
        converted_name = name.replace('-','_')
        os.environ.get('OCF_RESKEY_CRM_meta_'+converted_name)

def OcfPopulater
    def init(self):
        self.api = OcfApi()
    def populate(self, resource)
        for resource in resource.getParameters():
            value = self.api.variable( resource.getName() )
            if not value:
                value = resouce.getDefault()
            resource.set(value)

def OcfAgent:
    def init(self, name, version):
        self.name = name
        self.version  = version
        self.parameters = []

def OcfParameter:
    def init(self, name, default=''):
        self.name = name
        self.default = default
        self.description = ''
        self.unique = false
        self.required = false

    def name(self):
        return self.name
    def default(self):
        return self.default

def StonithAgent:
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
        shortdesc.text = resource.description.short
        longdesc = ET.SubElement(root, 'longdesc')
        longdesc.text = resource.description.long

        tree = Et.ElementTree(root)
        print ET.tostring(tree, encoding="UTF-8",
                     xml_declaration=True,
                     pretty_print=True,
                     doctype='<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">'))

    def validate(self, resource):

        self.populater.populate(resource)

        for item in resource.getParameters():
            item.validate()
            
        try:
            resource.validate()
        except AttributeError:

        return 0 

    def run(self, resource, action):
        actions = {}
        try:
            actions.update({"start": resource.start})
        except AttributeError:
            # ERROR: start must be implemented
        try:
            actions.update({"stop": resource.stop})
        except AttributeError:
            # ERROR: stop must be implemented
        try:
            actions.update({"monitor": resource.monitor})
            actions.update({"status": resource.monitor})
        except AttributeError:
            # ERROR: monitor must be implemented

        actions.update({
            "promote": getattr(resource, 'promote', self.notImplemented,
            "demote": getattr(resource, 'demote', self.notImplemented,
            "migrate_to": getattr(resource, 'migrateTo', self.notImplemented,
            "migrate_from": getattr(resource, 'migrateFrom', self.notImplemented,
            "meta-data": lambda: return self.metaData(resource),
            "validate-all": lambda: return self.validate(resource),
        })

        return actions[action]()

application = StonithAgent()
return application.run();
