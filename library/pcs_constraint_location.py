#!/usr/bin/python

DOCUMENTATION = '''
---
author: "Ondrej Famera <ondrej-xa2iel8u@famera.cz>"
module: pcs_constraint_location
short_description: "wrapper module for 'pcs constraint location'"
description:
  - "module for creating and deleting clusters location constraints using 'pcs' utility"
version_added: "2.0"
options:
  state:
    description:
      - "'present' - ensure that cluster constraint exists"
      - "'absent' - ensure cluster constraints doesn't exist"
    required: false
    default: present
    choices: ['present', 'absent']
  resource:
    description:
      - resource for constraint
    required: true
  node_name:
    description:
      - node name for constraints
    required: true
  score:
    description:
      - constraint score in range -INFINITY..0..INFINITY
    required: false
    default: 'INFINITY'
notes:
   - tested on CentOS 7.3
'''

EXAMPLES = '''
- name: resource resA prefers to run on node1
  pcs_constraint_location: resource='resA' node_name='node1'

- name: resource resB avoids running on node2
  pcs_constraint_location: resource='resB' node_name='node2' score='-INFINITY'
'''

import os.path
import xml.etree.ElementTree as ET
from distutils.spawn import find_executable

def main():
        module = AnsibleModule(
                argument_spec = dict(
                        state=dict(default="present", choices=['present', 'absent']),
                        resource=dict(required=True),
                        node_name=dict(required=True),
                        score=dict(required=False, default="INFINITY"),
                ),
                supports_check_mode=True
        )

        state = module.params['state']
        resource = module.params['resource']
        node_name = module.params['node_name']
        score = module.params['score']

        result = {}

        if find_executable('pcs') is None:
            module.fail_json(msg="'pcs' executable not found. Install 'pcs'.")

        ## get running cluster configuration
        rc, out, err = module.run_command('pcs cluster cib')
        if rc == 0:
            current_cib_root = ET.fromstring(out)
        else:
            module.fail_json(msg='Failed to load current cluster configuration')
        
        ## try to find the constraint we have defined
        constraint = None
        constraints = current_cib_root.findall("./configuration/constraints/rsc_location")
        for constr in constraints:
            # constraint is considered found if we see resource and node as got through attributes
            if constr.attrib.get('rsc') == resource and constr.attrib.get('node') == node_name:
                constraint = constr
                break

        # location constraint creation command
        cmd_create='pcs constraint location %(resource)s prefers %(node_name)s=%(score)s' % module.params

        if state == 'present' and constraint is None:
            # constraint should be present, but we don't see it in configuration - lets create it
            result['changed'] = True
            if not module.check_mode:
                rc, out, err = module.run_command(cmd_create)
                if rc == 0:
                    module.exit_json(**result)
                else:
                    module.fail_json(msg="Failed to create constraint with cmd: '" + cmd_create + "'", output=out, error=err)

        elif state == 'present' and constraint is not None:
            # constraint should be present and we see similar constraint so lets check if it is same
            if score != constraint.attrib.get('score'):
                result['changed'] = True
                if not module.check_mode:
                    rc, out, err = module.run_command('pcs constraint delete '+ constraint.attrib.get('id'))
                    if rc != 0:
                        module.fail_json(msg="Failed to delete constraint for replacement with cmd: '" + cmd + "'", output=out, error=err)
                    else:
                        rc, out, err = module.run_command(cmd_create)
                        if rc == 0:
                            module.exit_json(**result)
                        else:
                            module.fail_json(msg="Failed to create constraint replacement with cmd: '" + cmd_create + "'", output=out, error=err)
                   
        elif state == 'absent' and constraint is not None:
            # constraint should not be present but we have found something - lets remove that
            result['changed'] = True
            if not module.check_mode:
                rc, out, err = module.run_command('pcs constraint delete '+ constraint.attrib.get('id'))
                if rc == 0:
                    module.exit_json(**result)
                else:
                    module.fail_json(msg="Failed to delete constraint with cmd: '" + cmd + "'", output=out, error=err)
        else:
            # constraint should not be present and is not there, nothing to do
            result['changed'] = False

        ## END of module
        module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
