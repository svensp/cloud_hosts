datacenter = "{{ data_center }}"
data_dir = "/var/lib/consul"
encrypt = "{{ key }}"
bind_addr = "{{ ansible_default_ipv4.address }}"
server = true
bootstrap_expect = {{ groups[consul_group]|length }}
retry_join = [ {% set first_skipped=false %}{% for host in groups[consul_group] %}{% if host != inventory_hostname %}{% if not loop.first and not first_skipped %}, {% endif %}"{{ hostvars[host].ansible_fqdn }}"{% set first_skipped=false %}{% else %}{% if loop.first %}{% set first_skipped=true %}{% endif %}{% endif %}{% endfor %} ]
verify_outgoing = true
verify_incoming = true
ca_file = /etc/consul/cacert.pem
cert_file = /etc/consul/cacert.pem
key_file = /etc/consul/key.pem
