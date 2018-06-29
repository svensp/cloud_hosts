# hosts
Ansible roles and config used to provision my low profile hetzner-cloud machines.
They are currently running a high available kubernetes cluster using 2 cx21 and
1 cx11.

It started out as a 2 host cluster but the cx11 was added to have an etcd quorum
on a single host failing. The cx11 is also a kubernetes worker because otherwise
it would just be sitting there.

The commit history from before changing server to github was deleted because at
some points the roles contained passwords

## Roles
I usually have 2 playbooks per host config.

- hostname_provision.yml  
  This file includes the `provision`, `base-tools` and `users` roles and is executed as `root`
- hostname.yml  
  This file includes all other roles and is executed via `become` - sudo to root

I would prefer not to use passwordless root access at all but provisioning and adding users requires it.

### Provision
This role provisions a host that is currently in hetzner rescue mode.
Most notably it causes the installation of Debian 9? with /boot on ext4 and the
rest of the filesystem on lvm.  
It also provides a `startup script` to the installation which installs python on
the new machine. This is necessary for ansible connect to it.
It then restarts the machine and waits for it to come bcak online.

Note that it does not do anything if the hostname of the machine is not `rescue`
so it is safe to run this role on provisioned hosts.  
It usually
### Parameters
- volumes: Required `[ { name: lvm-name, mountpoint: /path/to/mountpoint, fs: filesystemname, size: size } ]`
  - Size needs to be understood by hetzners `installimage` Kommand. Notable examples are:
    - `all` The rest of the volume group at the time. So writing more volumes after one using `all` will fail
    - `10G` Use 10 Gibibyte

### Examples
```yaml
    - role: provision
      volumes:
        - name: root
          mountpoint: /
          fs: ext4
          size: all
```

### base-tools
This role installs the bare minimum packages necessary to use the host
- zsh
- sudo
- rsync
- git
- lvm

### Parameters
This role does not take any parameters

### users
This role creates users from files.
The expected files are:
- playbook_root/users/{username}/password: sha512 hashed password
- playbook_root/users/{username}/id_rsa.pub: public ssh key which will allow the user to log in
- playbook_root/users/{username}/copy/*: Files to be copied into the users home directory

### Parameters
This role does not take any parameters

### tools
Installs a set of tools to work comfortably on the server
Installed tools:

- screen
- vim
- git
- unattended-upgrades
- apt-listchanges

### Parameters
This role does not take any parameters

### cluster
This role installs corosync, pacemaker and pcs. It then attempts to detect if the cluster already exists. If it does not
then all hosts in the ansible group `clustergroup` will have the `hacluster` user created with the password set in `cluster.ini`
section `pacemaker` key `password`.

### Parameters
Required:
- clustername: An arbitrary string. DO NOT CHANGE THIS. Changing it will cause the cluster to be recreated
- clustergroup: All hosts in this group will be added to the cluster
Optional:
- ini_file: Override the ini file in which to look for the password
- ini_section: Override the section of the ini file in which to look for the password
- stickyness: Set a different default stickyness for resources
- disable_stonith: Set the `disable_stonith` property for the cluster to work without stonith devices.  
  This setting should never be used for production systems. See the `hetzner_cloud_stonith` role for hetzner cloud stonith
  or inspiration on how to implement your own role providing stonith
  
### TODO: Describe more roles

# Credits
Ondrej Faměra - Ansible Peacemaker modules - https://github.com/OndrejHome/ansible.pcs-modules-2
