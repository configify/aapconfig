controller_config
=========
This role creates objects in AAP Controller and AAP Gateway (for AAP 2.5)

Requirements
------------
The role needs **ansible.controller**, **ansible.platform** (for AAP 2.5) and **ansible.utils** collections.

Role Variables
--------------
For each object this role creates (credentials, projects etc.), it expects a variable with a list of dictionaries structured in a certain way for each item being created, as well as credentials for Controller. See collection documentation for more details.

Example Playbook
----------------
```
  ---
  - name: Configure AAP
    hosts: localhost
    gather_facts: false
  
    roles:
      - controller_config
```
