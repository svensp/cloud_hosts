resource {{ item.name }} {
	disk        {{ item.disk_device }};
	device      {{ item.drbd_device }} minor {{ item.minor }};
	meta-disk   internal;

	{% if drbd_group is defined %}
		{% set drbd_hosts=groups[drbd_group] %}
	{% endif %}

	{% for host in drbd_hosts %}

	on {{ hostvars[host].ansible_hostname }} {
		address {{ hostvars[host].ansible_default_ipv4.address }}:{{ item.port }};

	}

	{% endfor %}

	startup {
		wfc-timeout  15;
		degr-wfc-timeout 60;
	}

	disk {
		resync-rate 24M;
		on-io-error             detach;
		c-plan-ahead 0;
		c-fill-target 24M;
		c-min-rate 80M;
		c-max-rate 720M;
	} 
	handlers {
	{% if resource_level_fencing is defined %}
		fence-peer "/usr/lib/drbd/crm-fence-peer.sh";
		after-resync-target "/usr/lib/drbd/crm-unfence-peer.sh";
		unfence-peer "/usr/lib/drbd/crm-unfence-peer.sh";
	{% endif %}
	}
	net {
	{% if resource_level_fencing is defined %}
		fencing resource-only;
	{% endif %}
		protocol B;
# max-epoch-size          20000;
		max-buffers             36k;
		sndbuf-size            1024k ;
		rcvbuf-size            2048k;
		after-sb-0pri discard-least-changes;
		after-sb-1pri consensus;
		after-sb-2pri disconnect;
	}
}
