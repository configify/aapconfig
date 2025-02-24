hub_config
=========
This role creates objects in AAP Private Automation Hub

Requirements
------------
The role needs **infra.ah_configuration**  collection

Role Variables
--------------
For each object this role creates, it expects a variable with a list of dictionaries structured in a certain way for each item being created, as well as credentials for Hub. See collection documentation for more details.

Example Playbook
----------------
```
  ---
  - name: Configure AAP
    hosts: localhost
    gather_facts: false
  
    roles:
      - hub_config
```
