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

## Competition accounts

The shared roster is `inventory/group_vars/all/users.yaml`. Linux hosts
use local accounts only; no Linux domain join is performed. The `admin` flag
grants sudo on Linux and Domain Admins membership for Windows domain accounts.
The `gray_team` flag adds the account to `grayteam_users`.

| Accounts | Linux | Windows |
| --- | --- | --- |
| First five competition admins | Local sudo users | Domain Admins |
| Five normal competition users | Local users without managed sudo-group membership | Domain users without Domain Admins membership |
| grayteam, violetgray | Local sudo users, grayteam_users | Domain Admins, domain grayteam_users |
| othergrayteam | Local sudo user, grayteam_users | Local Administrators and local grayteam_users on member servers only |

Domain controllers do not have ordinary local accounts, so `othergrayteam` is
excluded from them. Domain gray team membership contains `grayteam` and
`violetgray`; the member-server local group contains `othergrayteam`.
Team-specific domain names are set in `group_vars/team1.yaml` and `team2.yaml`.
Samba consumes the shared roster and uses the same Linux Vault passwords.

Run full deployment from the repository root with your normal Vault arguments:

```sh
ansible-playbook deploy.yaml --ask-vault-pass
```

The root `ansible.cfg` selects `inventory/inventory.yaml` and `roles/`.
Inventory-adjacent `group_vars/` and `host_vars/` load automatically.

Linux users are provisioned before Linux services. Windows domain users are
provisioned after AD setup. For existing domains, run only account tasks:

```sh
ansible-playbook deploy.yaml --tags users --ask-vault-pass
```

For initial domain creation, run the full Windows playbook or full deployment
without the users tag. Linux account provisioning lives in
`roles/linux_users/`. To manage Linux accounts alone from the repository root:

```sh
ansible-playbook linux.yaml --tags users --ask-vault-pass
```

All roles source account passwords from these keys in
`inventory/group_vars/all/vault.yaml`:

| Vault key | Used for |
| --- | --- |
| `vault_linux_user_password` | Regular Linux accounts, FTP, MySQL, regular Samba accounts |
| `vault_linux_gray_team_password` | Linux gray team accounts, SSH/sudo as grayteam, gray team Samba accounts |
| `vault_windows_user_password` | Regular AD accounts and Windows connection as Administrator |
| `vault_windows_gray_team_password` | Gray team AD/local accounts and domain joins as grayteam |

The AD recovery password remains the separate `ad_safe_mode_password` Vault key.
See `inventory/secrets.yaml.example` for the required keys. Edit the
existing encrypted Vault yourself; no plaintext fallback passwords are provided.
Team-specific Vault files may override these defaults if passwords differ.
Domain joins require the grayteam domain account to have been provisioned first.

Linux retains `update_password: always`; AD and Windows local accounts retain
`on_create`, so changing their Vault defaults does not reset existing Windows
account passwords. Samba resets passwords on each run and reports changed.

No accounts outside
the managed roster are removed. Removing an account from the roster does not
delete it. Normal-user privilege enforcement removes only the managed Linux
sudo/wheel membership or AD Domain Admins membership, not other privilege paths.

Before rollout, syntax-check and inspect inventory targeting, then run against
one Linux host and one domain controller. Verify accounts, gray team groups,
sudo/Domain Admins membership, and password behavior on a second run. Windows
local accounts should also be verified on one member server.

MySQL provisions every packet account from the shared roster, including gray
team accounts. Admins receive database-scoped SELECT/INSERT/UPDATE/DELETE;
normal users receive SELECT. FTP uses the same local accounts, limits logins to
the roster, and grants the FTP group access to the shared upload directory.
PAM applies password aging to the roster. FTP, PAM, Samba, and mail roles depend
on `linux_users` so local packet accounts are initialized when run separately.
Legacy MySQL `low_user`/`high_user` and Linux `ftpuser` accounts are not deleted
automatically; FTP's allowlist excludes accounts outside the packet roster.

Windows domain joins use `domain_name` and `domain_controller_host` from the
host's team group variables. The controller's DNS address comes from its
`ansible_host` in inventory. The domain join play in `windows.yaml` targets all Windows member servers
and excludes `ad_dns`. Join credentials default to `grayteam@<domain_name>` and
`vault_windows_gray_team_password`; optional inventory overrides are defined in
`roles/windows_domain_join/defaults/main.yml`.

Full Windows deployment now creates AD/DNS and packet domain users, provisions
local gray team accounts on member servers, joins those servers to their team
domains, and deploys IIS. ICMP and WinRM roles remain available but are not called
by the main playbook. To rerun joins after AD provisioning, use
`ansible-playbook windows.yaml --tags domain_join --ask-vault-pass`
from the repository root.

Each team's `ad_reverse_lookup_zones` lists its LAN and cloud /24 reverse DNS
zones. Zone creation does not itself create PTR records. MySQL now listens for
remote TCP connections and provisions both localhost and remote (`%`) packet
accounts. Host and network firewalls must permit TCP 3306 from the scorer.
