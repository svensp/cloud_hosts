#!/bin/python

import os
import sys

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

def OcfParameter
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

def StonithAgent
    def init(self):
        self.api = OcfApi()

    def metaData(self):

    def notImplemented(self):
        return OCfErrors.notImplemented

    def validate(self):
        # TODO: implement

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

def HCloudStonith

application = HCloudStonith()
return application.run();
