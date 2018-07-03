#!/usr/bin/python

DOCUMENTATION = '''
---
author: "Sven Speckmaier <sven@speckmaier.de>"
module: rancher_registration
short_description: Module to retrieve the registration code and image to add a host to a rancher enviornment
description:
  - This module interacts with the rancher api to retrieve the registrationUrl and current image
  - It tries to autodetect a viable rancher api url and key from your environment variables.
  - This will detect RANCHER_* api keys but also CATTLE_* keys which are set by rancher when running
  - with 'io.rancher.container.create_agent=true' and 'io.rancher.container.agent.role=environmentAdmin,agent'
version_added: "2.5"
options:
  rancher_environment:
    description:
      - Rancher environment to add the host to. Can be autodetected through rancher-metadata instead
    required: false
  rancher_url:
    description:
      - url to the rancher api. Can be given through RANCHER_URL or CATTLE_URL environment variables instead
    required: false
  rancher_access_key:
    description:
      - access key to the rancher api. Will be autodetected if omited.
    required: false
  rancher_secret_key:
    description:
      - secret key to the rancher api. Will be autodetected if omited.
    required: false
'''

EXAMPLES = '''
- name: Add host from within rancher infrastruture to the environment it we are running in
  rancher_client:

- name: Add host to the default environment through RANCHER_URL, RANCHER_ACCESS_KEY and RANCHER_SECRET_KEY,
  rancher_client: rancher_name=default

- name: Add a host to the default environment
  rancher_client:
    rancher_environment: default
    rancher_url: https://rancher.example.com/v1
    rancher_access_key: acbdefg12345678
    rancher_secret_key: qewrty019283745
    

'''

import os.path
import os
import requests
import json
import base64

def main():
        module = AnsibleModule(
                argument_spec = dict(
                        rancher_environment=dict(required=False),
                        rancher_url=dict(required=False),
                        rancher_access_key=dict(required=False),
                        rancher_secret_key=dict(required=False, no_log=True)
                ),
                supports_check_mode=True
        )

        #
        # Rancher url
        #
        if not module.params['rancher_url']:
            rancher_url = os.getenv('RANCHER_URL', os.environ.get("CATTLE_URL"))
            if not rancher_url:
                module.fail_json(msg="rancher_url not given and neither RANCHER_URL nor CATTLE_URL set in environment.")
        else:
            rancher_url = module.params['rancher_url']
                

        #
        # Rancher environment
        #
        rancher_environment = module.params['rancher_environment']
        if not rancher_environment:
            r = requests.get('http://rancher-metadata/2015-07-25/self/stack/environment_name')
            if r.status_code != 200:
                module.fail_json(msg="rancher_environment not set and retrieving the current environment from rancher-metadata failed with code: "+str(r.status_code))
                
            rancher_environment = r.text

        #
        # Cattle environment admin auth
        #
        cattle_auth = os.environ.get('CATTLE_AGENT_INSTANCE_ENVIRONMENT_ADMIN_AUTH');

        #
        # Rancher access key
        #
        rancher_access_key = module.params['rancher_access_key']
        if not rancher_access_key:
            rancher_access_key = os.environ.get('RANCHER_ACCESS_KEY')

        if not rancher_access_key and not cattle_auth:
            module.fail_json(msg="Neither rancher_access_key nor RANCHER_ACCESS_KEY nor CATTLE_AGENT_INSTANCE_ENVIRONMENT_ADMIN_AUTH found.")

        #
        # Rancher secret key
        #
        rancher_secret_key = module.params['rancher_secret_key']
        if not rancher_secret_key:
            rancher_secret_key = os.environ.get('RANCHER_SECRET_KEY')

        if not rancher_secret_key and not cattle_auth:
            module.fail_json(msg="Neither rancher_access_key nor RANCHER_ACCESS_KEY nor CATTLE_AGENT_INSTANCE_ENVIRONMENT_ADMIN_AUTH found.")

        rancher_auth_header={"Authorization": cattle_auth}
        if rancher_access_key and rancher_secret_key:
            rancher_auth_header = { "Authorization": 'Basic '+base64.b64encode(rancher_access_key+":"+rancher_secret_key) }
            

        result = {}
        r = requests.get(rancher_url+'/projects?limit=1&name='+rancher_environment, headers=rancher_auth_header)
        if r.status_code != 200:
            module.fail_json(msg="Request to find environment id failed with code "+str(r.status_code))
        content = r.json();

        if not content['data']:
            module.fail_json(msg="Rancher environment not found: "+rancher_environment)

        environment_id = content['data'][0]['id']

        r = requests.get(rancher_url+'/projects/'+environment_id+'/registrationtokens?state=active&limit=1', headers=rancher_auth_header)
        if r.status_code != 200:
            module.fail_json(msg="Request to find registration token and image failed with code "+str(r.status_code))
        tokenContent = r.json()
        if not tokenContent['data']:
            module.fail_json(msg="No active registration token found")

        result['changed'] = True
        result['rancher'] = {
                "registration_url": tokenContent['data'][0]['registrationUrl'],
                "image": tokenContent['data'][0]['image']
        }

        ## END of module
        module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
