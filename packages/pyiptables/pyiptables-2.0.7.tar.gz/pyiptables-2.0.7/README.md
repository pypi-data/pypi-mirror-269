# iptables


### Introduction

Native iptables is not friendly enough for most users.
This module is trying to make Linux/Iptables working like security groups in cloud environments.

### Scenarios
 - Service must be public facing, but still wants to block random bad ipaddress easily.
 - Scripting interface talking to iptables, be convenient like same thing in cloud.

### Examples
##### To protect your personal web server
```python

from pyiptables import securitygroup as sg

# Create a security group based on tcp/port, naming associated to your to-be-protected service.
sg.create_security_group(security_group_name='httpd', dst_port='80')

# Create, append/insert, rules based on source address, with action accept/reject/drop.
sg.create_security_group_rule(security_group_name='httpd', 
                              src_addr='1.2.3.0/24',
                              rule_action='insert',
                              packet_action='DROP')
sg.create_security_group_rule(security_group_name='httpd',
                              src_addr='2.3.4.0/24',
                              rule_action='insert',
                              packet_action='DROP')

# List current rules for a given security group.
sg.list_security_group_rules(security_group_name='httpd')

# Delete a given rule for a security group.
sg.delete_security_group_rule(security_group_name='httpd', rule_id='HTTPD_kfnsznwvb0mzn3uh')

# Delete a given security group and its rules completely.
sg.delete_security_group(security_group_name='httpd')

```