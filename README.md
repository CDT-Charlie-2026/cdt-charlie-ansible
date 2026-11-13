# cdt-charlie-ansible
This repo contains Team Charlie's Ansible and deployment information for Cyber Defense Techniques.

Service roles live under `roles/`; playbooks and `ansible.cfg` live at the repository root.

## Apache
Author: Dylan Weber (dmw7938@rit.edu)\
Code for deploying Docker and subsequently Apache is in the Apache role, located in roles/apache\
To deploy this service, run the linux.yaml playbook with the apache tag using the command:
```
ansible-playbook linux.yaml -i <PATH TO INVENTORY FILE> -t apache
```
Within the inventory file, ensure targets of the apache tag are under the apache group\
Variables for the role are defined in roles/apache/vars/main.yml\
Files deployed are located in roles/apache/files

## Samba
Author: Braeden Villano (bcv4079@rit.edu)
Code for deploying the Samba service is in the Samba role, located in roles/samba directory
To deploy, run the linux.yaml playbook for the tag samba, using the command:
```
ansible-playbook linux.yaml -i <PATH TO INVENTORY FILE> -t samba
```
In the inventory file, hosts Samba should be deployed to must be under the samba group
Variables for the role are defined in roles/samba/vars/main.yml
Samba passwords use the Linux regular-user and gray-team defaults from Ansible Vault.
The workgroup for the SMB server is SNOOPY and the share name is snoopy. The share can be connected to using the following command:
```
smbclient -W SNOOPY -U <USERNAME> //<IP_ADDRESS>/snoopy
```

## SSH / SSHD
Author: Aria Shepard (als5265@rit.edu)
Code for deploying SSH and SSHD, an SSH Peanuts themed banner, and creating a SSH alias. Located in the roles/ssh directory.
To deploy, run the linux.yaml playbook for the tag ssh, using the command:
```
ansible-playbook linux.yaml -i <PATH TO INVENTORY FILE> -t ssh
```

## PAM
Author: Willis Martin (wrm3207@rit.edu)
Enforces password complexity and aging policy via PAM, and manages a set of accounts includes create required ones and lock stale/unauthorized ones.

### Requirements
- Debian/Ubuntu target (need becuase of apt, package libpam-pwquality, and PAM config expected at
/etc/pam.d/common-password).

### Before running
Edit vars/main.yml:
- pam_min_length / pam_min_complexity_classes - password policy strictness
- pam_max_days / pam_warn_days - password aging
- pam_accounts_locked - optional account lock list; present accounts come from the shared packet roster.

### Usage
```
ansible-playbook linux.yaml -i <PATH TO INVENTORY FILE> -t pam
```

### Features demonstrated
1. Package install + PAM stack config
2. Password complexity policy via config templating
3. Account lifecycle management - create/lock accounts
4. Password aging policy

## Telnet
Author: Nathan Peck (nsp7941@rit.edu)\
Code for deploying the Telnet service is in the telnet role, located in roles/telnet directory\
To deploy, run the linux.yaml playbook for the tag telnet, using the command:
```
ansible-playbook linux.yaml -i <PATH TO INVENTORY FILE> -t telnet
```
In the inventory file, hosts telnet should be deployed to must be under the telnet group\
Variables for the role are defined in roles/telnet/vars/main.yml
