# Database Service

Creates the competition database and a MySQL account for every entry in
`inventory/group_vars/all/users.yaml`, including gray team users.

Packet admins receive SELECT, INSERT, UPDATE, and DELETE permissions on the
competition database; normal users receive SELECT only. These permissions are
configured by `mysql_admin_privileges` and `mysql_user_privileges`.
Passwords use `vault_linux_gray_team_password` for gray team accounts and
`vault_linux_user_password` for all other packet accounts.

Requires the `community.mysql` collection. Run through `linux.yaml`.
Existing legacy `low_user` and `high_user` accounts are not automatically removed.

MySQL listens on `mysql_bind_address` (default `0.0.0.0`) for remote scoring.
Each packet account is created for `localhost` and `%` via `mysql_user_hosts`.
Override the latter with scorer host addresses if needed. TCP port 3306 must
also be reachable through any host or network firewall; this role does not
manage firewall policy. Listener configuration changes restart MySQL.
