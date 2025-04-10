**configify.aapconfig** collection is used to configure Ansible Automation Platform (AAP).

## Table of contents
- [Advantages](#Advantages)
- [Where to start](#Where-to-start)
- [Setting things up](#Setting-things-up)
  - [Dependencies](#Dependencies)
  - [Connection variables](#Connection-variables)
- [Available playbooks](#Available-playbooks)
  - [aap_create_hub_token.yml](#aap_create_hub_token)
  - [aap_audit_unused_objects.yml](#aap_audit_unused_objects)
  - [aap_audit_...yml](#aap_audit_...)
  - [aap_configure.yml](#aap_configure)
  - [aap_create_rrule.yml](#aap_create_rrule)
  - [convert_smart_inventories.yml](#convert_smart_inventories)
  - [compare_inventory_hosts.yml](#compare_inventory_hosts)
- [Available Tags](#Available-Tags)
- [Variable structure](#Variable-structure)
  - [Hub collections](#Hub-collections)
  - [Hub repositories](#Hub-repositories)
  - [Execution environments](#Execution-environments)
  - [Notification profiles](#Notification-profiles)
  - [Settings](#Settings)
  - [Authentication and mappings](#Authentication-and-mappings)
  - [Users](#Users)
  - [Teams](#Teams)
  - [Roles](#Roles)
  - [Instance groups](#Instance-groups)
  - [Credential types](#Credential-types)
  - [Credentials](#Credentials)
  - [Organizations](#Organizations)
  - [Inventories](#Inventories)
  - [Projects](#Projects)
  - [Templates](#Templates)
  - [Schedules](#Schedules)
  - [Workflows](#Workflows)
- [Limitations](#Limitations)
- [Known issues](#Known-issues)



## Advantages

1. Ability to report on configuration drift and optionally delete objects
1. Ability to export existing AAP configurations and use them for automation after minor adjustments
1. Ability to export configurations from AWX 24
1. Ability to export configurations from AAP 2.4 in the format suitable for AAP 2.5
1. Ability to limit changes to a subset of organizations
1. Support for AAP 2.5 and Gateway
1. Automation from start to finish including Hub namespaces and collections, and most of the Controller objects including settings, roles, execution environments and many more
1. Playbooks to assist in migration from Smart to Constructed inventories
1. AAP objects are created and deleted in the right sequence, so no need to worry about ordering variables

## Where to start

Most likely you already have an existing installation of AAP with some objects and configurations.
In this case you can use one of the audit playbooks to export configurations.
For example to export existing organizations use:

```
ansible-playbook configify.aapconfig.aap_audit_organizations.yml
```

The output will look like below:

```
ok: [localhost] => {
    "controller_objects_organizations": [
        "{'name': 'Default', 'descr': '', 'creds': []}",
        "{'name': 'Org A', 'descr': '', 'creds': ['Ansible Galaxy']}",
        "{'name': 'Org C', 'descr': '', 'creds': ['Ansible Galaxy']}"
    ]
}
```

After removing double-quotes you will get a variable **controller_objects_organizations** - a list describing existing organizations as a code:

```
controller_objects_organizations: [
  {'name': 'Default', 'descr': '', 'creds': []},
  {'name': 'Org A', 'descr': '', 'creds': ['Ansible Galaxy']},
  {'name': 'Org C', 'descr': '', 'creds': ['Ansible Galaxy']}
]
```

For objects with more parameters feel free to split each item into multiple lines:

```
controller_objects_organizations: [
  {'name': 'Default', 'descr': '',
   'creds': []},

  {'name': 'Org A', 'descr': '',
   'creds': ['Ansible Galaxy']},

  {'name': 'Org C', 'descr': '',
   'creds': ['Ansible Galaxy']}
]
```

Feed this variable to **configify.aapconfig.aap_configure.yml** playbook to start automating.
For example, if this variable is in objects.yml file: 

```
ansible-playbook configify.aapconfig.aap_configure.yml -e @objects.yml --tags controller_config_organizations
```

To see an example of full working configuration please check the repository we use for testing this collection - https://github.com/configify/aapconfig_testing


## Setting things up


### Dependencies

This collection uses **ansible.controller**, **infra.ah_configuration**, **ansible.hub** and **ansible.platform** collections (as well as **ansible.utils** for some filtering). It also needs **awxkit**. When using Hub and AAP these dependencies should be installed automatically.

When using from command line install required collections and dependencies with ansible-galaxy command:
```
ansible-galaxy collection install ansible.controller
ansible-galaxy collection install infra.ah_configuration
ansible-galaxy collection install ansible.platform
ansible-galaxy collection install ansible.utils
ansible-galaxy collection install ansible.hub
pip install awxkit
```


### Connection variables

Playbooks that interact with AAP Controller need the following parameters (as environment variables):

```
CONTROLLER_HOST
CONTROLLER_USERNAME
CONTROLLER_OAUTH_TOKEN
(CONTROLLER_VERIFY_SSL)
```

For AAP 2.4 Controller specify API endpoint:

```
CONTROLLER_OPTIONAL_API_URLPATTERN_PREFIX=/api/
```

Playbooks that interact with AAP Hub need:

```
AH_HOST
AH_USERNAME
AH_PASSWORD
(AH_VERIFY_SSL)
```

For AAP 2.5, Gateway credentials are also needed to create/change Organizations, Users, Teams and Settings:

```
GATEWAY_HOSTNAME
GATEWAY_USERNAME
GATEWAY_API_TOKEN
(GATEWAY_VERIFY_SSL)
```

When using from command line supply parameters as environment variables on localhost, for example:

```
export AH_HOST=aap-hub.int
export CONTROLLER_OAUTH_TOKEN=OqJACPb8Bx7OBCAi311LvJRLyAJStw
export CONTROLLER_VERIFY_SSL=false
```

When used within AAP, Controller parameters will be picked up automatically from a credential of type **Red Hat Ansible Automation Platform** attached to the template.

To supply parameters needed for Hub:

1. Create custom credential type for Hub details with required fields and inject them as env vars:

    ```env:```

    ```  AH_HOST: '{{ ... }}'```

    ```  AH_USERNAME: '{{ ... }}'```

    ```  AH_PASSWORD: '{{ ... }}'```

    ```  AH_VERIFY_SSL: '{{ ... }}'```

    More details on how to create custom credentials and access values in a playbook/vars are available in Automation Controller User Guide.

1. Create a new credential of this type and put Hub details there
1. Assign this credential to the template

Parameters for Gateway will also need to be supplied in a custom credential.

Correct API endpoint for AAP 2.4 can be configured from **Settings | Job settings | Edit | Extra Environment Variables**:

```
{
    "CONTROLLER_OPTIONAL_API_URLPATTERN_PREFIX": "/api/"
}
```

## Available playbooks


### aap_create_hub_token

Use this playbook to create API token for Private Hub. Running this playbook will reset any existing Private Hub tokens for this user.


### aap_audit_problematic_objects

Use this playbook to report on potentially problematic objects:

- duplicated teams
- duplicated credentials
- duplicated inventories
- duplicated projects
- duplicated templates
- duplicated workflows
- duplicated notification profiles
- credentials not used in credentials, templates, workflows, orgs and projects
- custom credential types not used by credentials
- projects not used in templates, workflows and dynamic inventories
- notification profiles not used in templates, workflows and projects
- inventories not used in templates, workflows, workflow nodes and constructed inventories
- projects without an organization
- templates without inventory or project


### aap_audit_...

Use these playbooks to export existing configurations


### aap_configure

Use it to create objects and apply settings. The playbook expects variables that describe AAP objects and settings.

The following switches can also be specified as extra variables:

- **replace_passwords** to change passwords for users and credentials (note: this option makes tasks not idempotent)
- **replace_workflow_nodes** to force deletion of workflow nodes (note: this option makes workflow apply task not idempotent)
- **delete_objects** to delete rogue objects
- **wait_project_sync** to wait for projects to synchronise (note: automation will report but not fail if project fails to sync)
- **trigger_project_sync** to trigger project update (note: automation will not fail if project fails to sync)
- **format_for_25** to export certain objects in a structure ready for import into AAP 2.5
- **trigger_inventory_sync** to trigger dynamic and constructed inventories synchronization (note: automation will not fail if inventory fails to sync)
- **aap_platform** set to 'awx24' to export objects from AWX 25
- **limit_organizations** to limit creations and modifications to a subset of objects that belong to organizations from the specified list

When using from command line call the playbook specifying files with variables:

```
ansible-playbook configify.aapconfig.aap_configure.yml --extra-vars @credentials --extra-vars @projects
```

When used from AAP, create a wrapper playbook. For example:

```
---
- name: Include auth info
  hosts: localhost

  tasks:
    - name: Include credentials vars
      ansible.builtin.include_vars: credentials

    - name: Include project vars
      ansible.builtin.include_vars: projects

- name: Run playbook to configure AAP
  ansible.builtin.import_playbook: configify.aapconfig.aap_configure.yml
```


### aap_create_rrule

This playbook is for generating an rrule used to configure AAP schedules. When run without any additional parameters, it will generate a daily schedule that runs at the time of playbook run.

Use the following variables to adjust that default behaviour:

* **start_date** to change start date/time, specify in the following format: 2025-10-25 17:00:00.
* **end_after** to set an end date. specify either a number (as string) to limit the amount of schedule runs or a date/time as 2025-10-25 17:00:00.
* **tz** to set a timezone, default value is 'America/New_York'.
* **repetition** to skip some days, for example, daily schedule with repetition=2 will run only every other day.
* **frequency** to select one of minute, hour, day, week, month, year frequencies.

Weekly frequency can further be adjusted with **weekdays** variable that specifies days of the week when the schedule will run. Variable takes comma separated list with weekdays: monday, tuesday etc.

Monthly frequency can also be adjusted further in two ways:

* **x_day** specifying a day of the month, for example x_day=10 means run on 10th every month
* **every_x_weekday** containing one of 'first, second, third, fourth or last' followed by a weekday - monday, tuesday etc.


### convert_smart_inventories

The playbook exports existing Smart inventories in a format suitable for further import as Constructed inventories. During execution it:

* creates a list of inventories the hosts are part of and adds them to the input field
* converts parameters from host_filter field and adds them to the limit field
* adds “migrated” to inventory name
* adds or copies without changes other fields required for Constructed inventory

Please, review values in the limit fields for correctness. If there are any '=', you will need convert the filters manually.

### compare_inventory_hosts

The playbook is meant to be run after converted Constructed inventories have been imported into AAP. It compares the array of hosts from each Constructed inventory to the hosts from corresponding Smart inventory and reports on the difference if any.


## Available Tags

Tags are structured to specify broad tasks first and narrow them down further as required. For example, tag **controller_config_credentials** assumes both **controller_config_credentials_cleanup** and **controller_config_inventories_apply**.

If the requirement is to configure credentials including cleanup and add/change, then it's enough to specify only **controller_config_credentials**. But adding two tags **controller_config_credentials_cleanup** and **controller_config_inventories_apply** will essentially have the same effect.

If the requirement is to remove credentials and credential types that are not needed it's enough to specify **controller_config_credentials_cleanup** and **controller_config_credential_types_cleanup**.

Available configuration tags:

- hub_config
- hub_config_all_apply
- hub_config_all_cleanup
- hub_config_repositories
- hub_config_repositories_apply
- hub_config_repositories_cleanup
- hub_config_collections
- hub_config_collections_apply
- hub_config_collections_cleanup
- controller_config
- controller_config_all_apply
- controller_config_all_cleanup
- controller_config_ee
- controller_config_ee_apply
- controller_config_ee_cleanup
- controller_config_notifications
- controller_config_notifications_apply
- controller_config_notifications_cleanup
- controller_config_credential_types
- controller_config_credential_types_apply
- controller_config_credential_types_cleanup
- controller_config_credentials
- controller_config_credentials_apply
- controller_config_credentials_cleanup
- controller_config_instance_groups
- controller_config_instance_groups_apply
- controller_config_instance_groups_cleanup
- controller_config_inventories
- controller_config_inventories_apply
- controller_config_inventories_cleanup
- controller_config_organizations
- controller_config_organizations_apply
- controller_config_organizations_cleanup
- controller_config_projects
- controller_config_projects_apply
- controller_config_projects_cleanup
- controller_config_projects_sync
- controller_config_roles
- controller_config_roles_apply
- controller_config_roles_cleanup
- controller_config_settings
- controller_config_teams
- controller_config_teams_apply
- controller_config_teams_cleanup
- controller_config_templates
- controller_config_templates_apply
- controller_config_templates_cleanup
- controller_config_workflows
- controller_config_workflows_apply
- controller_config_workflows_cleanup
- controller_config_users
- controller_config_users_apply
- controller_config_users_cleanup
- controller_config_authentication
- controller_config_authentication_apply
- controller_config_authentication_cleanup
- controller_config_schedules
- controller_config_schedules_apply
- controller_config_schedules_cleanup

Available export tags:

- export_collections
- export_authenticators
- export_credential_types
- export_credentials
- export_execution_environments
- export_instance_groups
- export_inventories
- export_notifications
- export_organizations
- export_projects
- export_roles
- export_schedules
- export_settings
- export_teams
- export_templates
- export_users
- export_workflows

## Variable structure

Details below specify audit playbook and variable format for each AAP object supported by this collection.


### Hub collections

**Audit playbook**: aap_audit_collections.yml

**Variable structure**:
```
hub_objects_collections: [
  {'namespace': 'infra', 'name': 'ah_configuration', 'filename': 'infra-ah_configuration-2.1.0.tar.gz'},

  {'namespace': 'community', 'name': 'general', 'filename': 'community-general-8.2.0.tar.gz'}
]
```

When running in AAP, place tarball files in **/collections_tarballs** sub-folder.

When running from the command line the expected location is */runner/project/collections_tarballs* on localhost.

Hub namespaces will be pulled from collection names and created if required.


### Hub repositories

**Audit playbook**: aap_audit_repositories.yml

**Variable structure**:
```
hub_objects_remotes: [
  {'name': 'rh-certified', 'repo_url': 'https://console.redhat.com/api/automation-hub/content/published/',
   'repo_auth_url': 'https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token',
   'repo_auth_token': '',
   'requirements': {'collections': [{'name': 'ansible.platform'}, {'name': 'ansible.controller'}]}},

  {'name': 'community', 'repo_url': 'https://galaxy.ansible.com/api/',
   'repo_auth_url': '',
   'repo_auth_token': '',
   'requirements': ''}
]
```


### Execution environments

**Audit playbook**: aap_audit_execution_environments.yml

**Variable structure**:

```
controller_objects_execution_environments: [
  {'name': 'Automation Hub Default execution environment', 'descr': '', 'image': '{{ hub_host }}/ee-supported-rhel8:latest', 'pull': 'missing'},
  {'name': 'Automation Hub Minimal execution environment', 'descr': '', 'image': '{{ hub_host }}/ee-minimal-rhel8:latest', 'pull': 'missing'},
  {'name': 'Execution Environment A', 'descr': '', 'image': '{{ hub_host }}/ee-minimal-rhel8:latest', 'pull': 'missing'}
]
```

Note:

* currently there is no ability to remove description using automation

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.

### Notification profiles

**Audit playbook**: aap_audit_notification_profiles.yml

**Variable structure**:

```
controller_objects_notification_profiles: [
  {'name': 'Notification Email A', 'descr': '', 'notification_type': 'email',
   'notification_config': {'host': 'examplea.com', 'port': 25, 'sender': 'a@examplea.com', 'timeout': 30, 'use_ssl': False, 'use_tls': False, 'password': '', 'username': '', 'recipients': ['aaa@examplea.com']},
   'org': 'Org A',
   'messages': {'error': {'body': !unsafe ' #{{ job.id }} had status {{ job.status }}, view details at {{ url }}\n\n{{ job_metadata }}',
                          'message': !unsafe ' #{{ job.id }} "{{ job.name }}" {{ job.status }}: {{ url }}'},
                'started': {'body': !unsafe '#{{ job.id }} had status {{ job.status }}, view details at {{ url }}\n\n{{ job_metadata }}',
                            'message': !unsafe '"{{ job.name }}" {{ job.status }}: {{ url }}'},
                'success': {'body': !unsafe ' #{{ job.id }} had status {{ job.status }}, view details at {{ url }}\n\n{{ job_metadata }}',
                            'message': !unsafe '#{{ job.id }} "{{ job.name }}" {{ job.status }}: {{ url }}'}}}
]
```

Note:

* **!unsafe** keywords must be added manually before each string with curly brackets
* **None** values in message categories that may appear under certain circumstances in exports from AAP 2.4 need to be removed or replaced manually with correct values
* profiles with secrets always report "changed"

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.

### Settings

**Audit playbook**: aap_audit_settings.yml

**Variable structure**:

```
controller_settings_authentication: {
    'AUTHENTICATION_BACKENDS': [
      'awx.sso.backends.LDAPBackend',
      'awx.sso.backends.TACACSPlusBackend',
      'awx.main.backends.AWXModelBackend'
  ]
}

controller_settings_jobs: {
  "GALAXY_IGNORE_CERTS": true,
  "AWX_ISOLATION_SHOW_PATHS": []
} # type: ignore

controller_settings_ldap: {
        'AUTH_LDAP_BIND_DN': 'CN=user,CN=users,DC=examplec,DC=com',
        'AUTH_LDAP_BIND_PASSWORD': '$encrypted$',
        'AUTH_LDAP_GROUP_SEARCH': [
            'DC=examplec,DC=com',
            'SCOPE_SUBTREE',
            '(objectClass=group)'
        ],
        'AUTH_LDAP_1_SERVER_URI': 'ldap://examplec',
        'AUTH_LDAP_1_START_TLS': true,
        'AUTH_LDAP_ORGANIZATION_MAP': {
            'Org B': {
                'admins': [
                    'CN=orgbadm,OU=Users,DC=example,DC=com'
                ],
                'remove_admins': true,
                'remove_users': true,
                'users': [
                    'CN=orgb,OU=Users,DC=example,DC=com'
                ]
            },
            'Org C': {
                'admins': [],
                'users': [
                    'CN=orgc,OU=Users,DC=example,DC=com',
                    'CN=orgc2,OU=Users,DC=example,DC=com'
                ]
            }
        },
        'AUTH_LDAP_TEAM_MAP': {
            'Team B': {
                'organization': 'Org B',
                'remove': true,
                'users': [
                    'CN=teamb,OU=Users,DC=example,DC=com'
                ]
            },
            'Team C': {
                'organization': 'Org C',
                'users': [
                    'CN=teamb,OU=Users,DC=example,DC=com',
                    'CN=teamb2,OU=Users,DC=example,DC=com'
                ]
            }
        }
}
```

Note:

* **controller_settings_ldap** - LDAP configuration, which includes team and organization mappings, is a part of settings in AAP 2.4, while in AAP 2.5 these configurations are separate objects and are handled by separate playbooks/tasks


### Authentication and mappings

**Audit playbook**: aap_audit_authentication.yml

**Variable structure**:

```
controller_authentication: [
        {
            'configuration': {
                'CONNECTION_OPTIONS': {},
                'GROUP_TYPE': 'MemberDNGroupType',
                'GROUP_TYPE_PARAMS': {
                    'member_attr': 'member',
                    'name_attr': 'cn'
                },
                'SERVER_URI': [
                    'ldap://exampleb'
                ],
                'START_TLS': false,
                'USER_ATTR_MAP': {
                    'email': 'mail',
                    'first_name': 'givenName',
                    'last_name': 'sn'
                }
            },
            'enabled': true,
            'name': 'Auth_LDAP',
            'type': 'ansible_base.authentication.authenticator_plugins.ldap'
        }
]

controller_authenticator_maps: [
  {'name': 'Auth_LDAP_team_Team B_map', 'authenticator': 'Auth_LDAP', 'order': 0,
   'map_type': 'team', 'role': 'Team Member', 'organization': 'Org B', 'team': 'Team B', 'revoke': True,
   'triggers': {'groups': {'has_or': ['CN=teamb,OU=Users,DC=example,DC=com']}}},

  {'name': 'Auth_LDAP_org_Org C_user_map', 'authenticator': 'Auth_LDAP', 'order': 0,
   'map_type': 'organization', 'role': 'Organization Member', 'organization': 'Org C', 'team': '', 'revoke': False,
   'triggers': {'groups': {'has_or': ['CN=orgc,OU=Users,DC=example,DC=com', 'CN=orgc2,OU=Users,DC=example,DC=com']}}}
]
```

Note:

* these configurations are applicable to 2.5 and later
* **controller_authentication** objects will be created/changed even in check mode

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.


### Users

**Audit playbook**: aap_audit_users.yml

**Variable structure**:

```
controller_objects_users: [
  {'username': 'UserA', 'first_name': 'aaa', 'last_name': '', 'email': 'usera@example.com',
   'superuser': False, 'auditor': False, 'pass': ''},

  {'username': 'UserC', 'first_name': 'ccc', 'last_name': '', 'email': '',
   'superuser': True, 'auditor': False, 'pass': ''}
]
```

Note:

* currently there is no ability to modify users in AAP 2.5 using automation
* password values are updated only if **replace_passwords** is set to true which will make the task not idempotent (most likely passwords will be stored in Ansible vault or pulled from external sources therefore the values in the example are empty)

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.

### Teams

**Audit playbook**: aap_audit_teams.yml

**Variable structure**:

```
controller_objects_teams: [
  {'name': 'Team A', 'descr': '', 'org': 'Org A'},
  {'name': 'Team C', 'descr': '', 'org': 'Org C'}
]
```

### Roles

**Audit playbook**: aap_audit_roles.yml

**Variable structure**:

```
controller_objects_roles: [
  {'team': 'Team A', 'role': 'JobTemplate Execute', 'object_type': 'jobtemplate', 'object_name': 'Template A'},
  {'team': 'Team A', 'role': 'Project Update', 'object_type': 'project', 'object_name': 'Project A'},
  {'team': 'Team A', 'role': 'WorkflowJobTemplate Approve', 'object_type': 'workflowjobtemplate', 'object_name': 'Workflow A'},
  {'team': 'Team A', 'role': 'Credential Use', 'object_type': 'credential', 'object_name': 'Credential GitHub A'},
  {'team': 'Team A', 'role': 'Inventory Adhoc', 'object_type': 'inventory', 'object_name': 'Inventory Constructed A'},
  {'team': 'Team A', 'role': 'InstanceGroup Admin', 'object_type': 'instancegroup', 'object_name': 'Auto IG A'},

  {'team': 'Team C', 'role': 'Organization ExecutionEnvironment Admin', 'object_type': 'organization', 'object_name': 'Org C'},
  {'team': 'Team C', 'role': 'Organization Audit', 'object_type': 'organization', 'object_name': 'Org C'},
  {'team': 'Team C', 'role': 'Organization Approval', 'object_type': 'organization', 'object_name': 'Org C'},

  {'user': 'UserA', 'role': 'JobTemplate Execute', 'object_type': 'jobtemplate', 'object_name': 'Template A'},
  {'user': 'UserA', 'role': 'Project Use', 'object_type': 'project', 'object_name': 'Project A'},
  {'user': 'UserA', 'role': 'WorkflowJobTemplate Execute', 'object_type': 'workflowjobtemplate', 'object_name': 'Workflow A'},
  {'user': 'UserA', 'role': 'Credential Admin', 'object_type': 'credential', 'object_name': 'Credential GitHub A'},
  {'user': 'UserA', 'role': 'Inventory Update', 'object_type': 'inventory', 'object_name': 'Inventory Constructed A'},
  {'user': 'UserA', 'role': 'InstanceGroup Use', 'object_type': 'instancegroup', 'object_name': 'Auto IG A'},

  {'user': 'UserC', 'role': 'Organization Execute', 'object_type': 'organization', 'object_name': 'Org C'},
  {'user': 'UserC', 'role': 'Organization Project Admin', 'object_type': 'organization', 'object_name': 'Org C'},
  {'user': 'UserC', 'role': 'Organization Approval', 'object_type': 'organization', 'object_name': 'Org C'}
] # type: ignore
```

**Variable structure** (2.5 addition):

```
gateway_objects_roles: [
  {'user': 'UserA', 'role': 'Organization Member', 'object_type': 'organization', 'object_name': 'Org A'},
  {'user': 'UserC', 'role': 'Organization Admin', 'object_type': 'organization', 'object_name': 'Org C'}
]
```

Note:

* **gateway_objects_roles** settings will be created/changed even in check mode.

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.

### Instance groups

**Audit playbook**: aap_audit_instance_groups.yml

**Variable structure**:

```
controller_objects_instance_groups: [
  {'name': 'Static IG A', 'minimum': 1, 'percentage': 0, 'instances': ["{{ controller_host }}"]},

  {'name': 'Auto IG C', 'minimum': 1, 'percentage': 100, 'instances': []}
]
```

### Credential types

**Audit playbook**: aap_audit_credential_types.yml

**Variable structure**:

```
controller_objects_credential_types: [
  {'name': 'Credential Type C', 'descr': '',
   'inputs': {'fields': [{'id': 'usernameC', 'type': 'string', 'label': 'Username'},
                         {'id': 'passwordC', 'type': 'string', 'label': 'Password'}]},
   'injectors': {'extra_vars': {'configifyadpass': !unsafe '{{ passwordC }}', 'configifyaduser': !unsafe '{{ usernameC }}'}}}
]
```

Note:

* **!unsafe** keywords, they must be added manually before each string with curly brackets
* currently there is no ability to remove description using automation

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.

### Credentials

**Audit playbook**: aap_audit_credentials.yml

**Variable structure**:

```
controller_objects_credentials: [
  {'name': 'Credential Machine A', 'org': 'Org A', 'descr': '', 'type': 'Machine',
   'inputs': {'password': '', 'username': 'aaa', 'become_method': '', 'become_username': ''},
   'src_input_field_name': 'password', 'src_credential': '', 'src_metadata': ''},

  {'name': 'Credential C', 'org': '', 'descr': '', 'type': 'Ansible Galaxy/Automation Hub API Token',
   'inputs': {'url': 'https://examplec', 'token': '', 'auth_url': ''},
   'src_input_field_name': 'password', 'src_credential': '', 'src_metadata': ''}
]
```

Note:

* currently there is no ability to remove description using automation
* password/token values are updated only if **replace_passwords** is set to true which will make the task not idempotent (most likely passwords/tokens will be stored in Ansible vault or pulled from external sources therefore the values in the example above are empty)
* in some cases there is no ability to modify credentials with incorrect sources using automation

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.

### Organizations

**Audit playbook**: aap_audit_organizations.yml

**Variable structure**:

```
controller_objects_organizations: [
  {'name': 'Org A', 'descr': '', 'creds': ['Credential A']},
  {'name': 'Org C', 'descr': '', 'creds': ['Credential C']},
]
```

### Inventories

**Audit playbook**: aap_audit_inventories.yml

**Variable structure**:

```
controller_objects_inventories_dynamic: [
  {'name': 'Inventory Dynamic C', 'description': '', 'org': 'Org C', 'host_filter': '', 'prevent_fallback': False,
   'variables': {},
   'sources': [{'name': 'Inventory Source C', 'description': '', 'enabled_value': '', 'enabled_var': '',
                'host_filter': '', 'overwrite': False, 'overwrite_vars': False, 'source': 'scm',
                'source_path': '', 'project': 'Project with Creds C', 'timeout': 0, 'update_cache_timeout': 0,
                'update_on_launch': False, 'verbosity': 1}]}
]

controller_objects_inventories_static: [
  {'name': 'Inventory Static C', 'description': 'Static inventory C', 'org': 'Org C', 'host_filter': '', 'prevent_fallback': False,
   'variables': {},
   'hosts': [{'name': 'Host C2', 'description': '', 'variables': {}}],
   'groups': [{'name': 'Group C1', 'description': '', 'subgroups': ['Group C2'], 'hosts': [], 'variables': {}},
              {'name': 'Group C2', 'description': '', 'subgroups': [], 'hosts': [{'name': 'Host C', 'description': '', 'variables': {}}], 'variables': {}}]}
]

controller_objects_inventories_constructed: [
  {'name': 'Inventory Constructed C', 'description': '', 'org': 'Org C',
   'input': ['Inventory Static C'],
   'host_filter': '', 'source_vars': {'plugin': 'constructed', 'strict': True}, 'limit': 'Group C1',
   'variables': {},
   'source': ''}
]

controller_objects_inventories_smart: [
  {'name': 'Smart A', 'description': '', 'org': 'A', 'variables': {}, 'host_filter': 'name__icontains=B'}
]
```

Note:

* inventories and hosts always report "changed" in check mode
* inventories, inventory sources, groups and hosts report "changed" during the first run and each time after template "saved" in the GUI

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.


### Projects

**Audit playbook**: aap_audit_projects.yml

**Variable structure**:

```
controller_objects_projects: [
  {'name': 'Project with Creds B', 'type': 'git', 'branch': '', 'clean_on_update': False, 'delete_on_update': False, 'update_on_launch': False,
   'allow_override': False, 'org': 'Org B', 'cred': 'Credential GitHub B', 'url': 'https://github.com/configify/hi.git', 'ee': 'Execution Environment B',
   'notifications_on_start': [], 'notifications_on_success': [], 'notifications_on_failure': []}
]
```

Note:

* currently there is no ability to remove credential from a project
* currently there is no ability to remove execution environemnt from a project

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.

### Templates

**Audit playbook**: aap_audit_templates.yml

**Variable structure**:

```
controller_objects_templates: [
  {'name': 'Template A', 'description': '', 'playbook': 'hi.yml', 'execution_environment': '',
   'project': 'Project with Creds A', 'allow_simultaneous': False, 'ask_credential_on_launch': False, 'ask_diff_mode_on_launch': False,
   'ask_execution_environment_on_launch': False, 'ask_forks_on_launch': False, 'ask_instance_groups_on_launch': False,
   'ask_inventory_on_launch': False, 'ask_job_slice_count_on_launch': False, 'ask_job_type_on_launch': False,
   'ask_labels_on_launch': False, 'ask_limit_on_launch': False, 'ask_scm_branch_on_launch': False,
   'ask_skip_tags_on_launch': False, 'ask_tags_on_launch': False, 'ask_timeout_on_launch': False,
   'ask_variables_on_launch': False, 'ask_verbosity_on_launch': False, 'become_enabled': False, 'diff_mode': False,
   'force_handlers': False, 'forks': 0, 'host_config_key': '', 'inventory': 'Inventory Dynamic A', 'job_slice_count': 1,
   'job_tags': '', 'job_type': 'run', 'limit': '', 'prevent_instance_group_fallback': False, 'scm_branch': '',
   'skip_tags': '', 'start_at_task': '', 'survey_enabled': False, 'timeout': 0, 'use_fact_cache': False, 'verbosity': 0,
   'extra_vars': {},
   'survey': {},
   'webhook_service': '', 'webhook_credential': '',
   'creds': ['Credential Machine A'],
   'notifications_on_start': ['Notification Email A', 'Notification Slack A'], 'notifications_on_success': [], 'notifications_on_failure': ['Notification Slack A']}
]
```

Note:

* currently there is no ability to disable webhook or remove webhook credentials using automation
* currently there is no ability to remove execution environment using automation

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.


### Schedules

**Audit playbook**: aap_audit_schedules.yml

**Variable structure**:

```
controller_objects_schedules: [
  {'name': 'Cleanup Job Schedule', 'descr': 'Automatically Generated Schedule', 'template': 'Cleanup Job Details',
   'rules': 'DTSTART:20240608T043855Z RRULE:FREQ=WEEKLY;INTERVAL=1;BYDAY=SU'}
]
```

Use **aap_create_rrule.yml** playbook to generate value for "rules" field.

### Workflows

**Audit playbook**: aap_audit_workflows.yml

**Variable structure**:

```
controller_objects_workflows: [
  {'name': 'Workflow A', 'descr': '', 'org': 'Org A', 'inventory': 'Inventory Static A',
   'allow_simultaneous': False, 'ask_inventory_on_launch': False, 'ask_labels_on_launch': False, 'ask_limit_on_launch': False, 'ask_scm_branch_on_launch': False,
   'ask_skip_tags_on_launch': False, 'ask_tags_on_launch': False, 'ask_variables_on_launch': False,
   'extra_vars': {}, 'job_tags': '', 'limit': '', 'scm_branch': '', 'skip_tags': '', 'survey_enabled': False, 'webhook_credential': '', 'webhook_service': '',
   'notifications_on_start': [], 'notifications_on_success': [], 'notifications_on_failure': [], 'notifications_on_approval': [],
   'nodes': [{'extra_data': {}, 'scm_branch': '', 'job_type': '', 'job_tags': '', 'skip_tags': '', 'limit': '', 'diff_mode': '', 'verbosity': '',
              'forks': '', 'job_slice_count': '', 'timeout': '', 'all_parents_must_converge': False,
              'identifier': '1ca40111-f92b-435e-bff2-b33edd455941',
              'unified_job_template': {'organization': {'name': 'Org C', 'type': 'organization'}, 'name': 'Template C', 'type': 'job_template'},
              'related': {'credentials': [],
                          'success_nodes': [],
                          'failure_nodes': [],
                          'always_nodes': []}},
             {'extra_data': {}, 'scm_branch': '', 'job_type': '', 'job_tags': '', 'skip_tags': '', 'limit': '', 'diff_mode': '', 'verbosity': '',
              'forks': '', 'job_slice_count': '', 'timeout': '', 'all_parents_must_converge': False,
              'identifier': '86e11000-e8a2-4ca6-9637-18cd29846f59',
              'unified_job_template': {'organization': {'name': 'Org A', 'type': 'organization'}, 'name': 'Template A', 'type': 'job_template'},
              'related': {'credentials': [],
                          'success_nodes': [{'identifier': '1ca40111-f92b-435e-bff2-b33edd455941', 'type': 'workflow_job_template_node'}],
                          'failure_nodes': [{'identifier': '94638f3b-b22d-4faa-a306-393791ef0c89', 'type': 'workflow_job_template_node'}],
                          'always_nodes': []}},
             {'extra_data': {}, 'scm_branch': '', 'job_type': '', 'job_tags': '', 'skip_tags': '', 'limit': '', 'diff_mode': '', 'verbosity': '',
              'forks': '', 'job_slice_count': '', 'timeout': '', 'all_parents_must_converge': False,
              'identifier': '94638f3b-b22d-4faa-a306-393791ef0c89',
              'unified_job_template': {'organization': {'name': 'Org A', 'type': 'organization'}, 'name': 'Template A', 'type': 'job_template'},
              'related': {'credentials': [],
                          'success_nodes': [],
                          'failure_nodes': [],
                          'always_nodes': []}}]}
]
```

Note:

* workflows with approval nodes always report "changed"
* workflows with extra vars will report "changed" each time after the "Save" button is pressed in the GUI, even if nothing has changed
* currently there is no ability to remove all survey questions using automation
* currently there is no ability to disable webhook or remove webhook credentials using automation
* inventory and execution environment fields for workflow nodes are omitted from export when empty

See [Known issues](#Known-issues) for more details and upvote mentioned Red Hat PRs/tickets.


## Limitations

This collection doesn't support:

* container groups
* projects sourced from controller file system
* specifying instance groups in job templates

Some fields that from our experience are rarely used have been purposely omitted to avoid overloading object variables. These fields can be added in future if there is a demand:

* organizations: instance groups
* organizations: max_hosts
* inventories: instance groups
* inventory sources: credentials (see https://github.com/ansible/awx/issues/14919 and https://github.com/ansible/awx/pull/14976)
* inventory sources: execution_environment (see https://github.com/ansible/awx/issues/14920 and https://github.com/ansible/awx/pull/14974)
* projects: source control refspec
* projects: track submodules
* templates: labels


## Known issues

All the issues below are related to Red Hat certified collections. We opened tickets and submitted PRs with fixes. Please, take a minute and upvote them so that they get some attention.

- **Templates**: without extra vars automation reports "changed" during the first run, with extra vars it reports "changed" each time after template "saved" in the GUI
(see https://github.com/ansible/awx/issues/14842 and https://github.com/ansible/awx/pull/15232)

- **Templates**: no option to specify empty or null values for webhook_service and webhook_credential thus no way to remove them
(see https://github.com/ansible/awx/issues/14843 and https://github.com/ansible/awx/pull/14844)

- **Templates**: execution_environment field is ignored when empty, which makes it impossible to remove ee using automation
  (see https://github.com/ansible/awx/issues/14841 and https://github.com/ansible/awx/pull/14975)

- **Workflows**: when extra vars are not empty, automation reports "changed" each time after workflow "saved" in the GUI
(see https://github.com/ansible/awx/pull/15232)

- **Workflows**: no option to specify empty value for webhook_service, which would be required to disable a webhook
(see https://github.com/ansible/awx/issues/15845 and https://github.com/ansible/awx/pull/15848)

- **Workflows**: empty value for webhook_credential is ignored instead of removing credential
(see https://github.com/ansible/awx/issues/15844 and https://github.com/ansible/awx/pull/15848)

- **Workflows**: execution environment and inventory fields for Workflow nodes don't accept empty values
(see https://github.com/ansible/awx/issues/15846, https://github.com/ansible/awx/issues/15847 and https://github.com/ansible/awx/pull/15848)

- **Inventories**: incorrectly report "changed" in dry-run mode
(see https://github.com/ansible/awx/issues/14922 and https://github.com/ansible/awx/pull/14988)

- **Hosts**: incorrectly report "changed" in dry-run mode
(see https://github.com/ansible/awx/issues/14922 and https://github.com/ansible/awx/pull/14988)

- **Credentials**: empty value in description is ignored
(see https://github.com/ansible/awx/issues/15854 and https://github.com/ansible/awx/pull/15857)

- **Credentials**: error when trying to modify credentials with not working source
(see https://issues.redhat.com/browse/AAP-36552)

- **Credential types**: empty value in description is ignored
(see https://github.com/ansible/awx/issues/15855 and https://github.com/ansible/awx/pull/15858)

- **Execution environments**: empty value in description is ignored
(see https://github.com/ansible/awx/issues/15856 and https://github.com/ansible/awx/pull/15859)

- **Users**: no ability to modify users in AAP 2.5 (see https://issues.redhat.com/browse/AAP-40035)

- **Notifications**: custom messages that haven't been changed (i.e. still default) will show "None" during export. This is an issue with API
(see https://issues.redhat.com/browse/AAP-40066)

- **Notifications**: add update_secrets parameter
(see https://github.com/ansible/awx/issues/15825 and https://github.com/ansible/awx/pull/15826)

- **Authentication**: module ansible.platform.authenticator does not honor check mode
(see https://issues.redhat.com/browse/AAP-40037)

- **Roles**: module ansible.platform.role_user_assignment does not honor check mode
(see https://issues.redhat.com/browse/AAP-40037)

- **Inventories**: because of how variables are handled by ansible.controller collection, automation reports "changed" during the first run and each time after template "saved" in the GUI
(see https://github.com/ansible/awx/issues/14918 and https://github.com/ansible/awx/pull/15232)

- **Inventory sources**: because of how variables are handled by ansible.controller collection, automation reports "changed" during the first run and each time after template "saved" in the GUI
(see https://github.com/ansible/awx/issues/14918 and https://github.com/ansible/awx/pull/15232)

- **Inventory groups**: automation reports "changed" during the first run and each time after template "saved" in the GUI
(see https://github.com/ansible/awx/issues/14918 and https://github.com/ansible/awx/pull/15232)

- **Inventory hosts**: automation reports "changed" during the first run and each time after template "saved" in the GUI
(see https://github.com/ansible/awx/issues/14918 and https://github.com/ansible/awx/pull/15232)

- **Private Hub**: automation doesn't support oAuth tokens which is a limitation of infra.ah_configuration.ah_api plugin
(see https://github.com/ansible/galaxy_collection/issues/447)

- **Projects**: no ability to remove credential and execution environment
(see https://issues.redhat.com/browse/AAP-42637)
