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

## Sandlot scorecard

The role provisions `competition_db.sandlot_scorecard` (or the configured
`mysql_database`) with five player rows. Each has singles, doubles, triples,
home_runs and a recorded total_bases. The STORED generated column
`scorecard_status` returns PASS only for nonnegative counts and a matching total:
`singles + 2*doubles + 3*triples + 4*home_runs`. Otherwise it returns FAIL.
MySQL recalculates the status when a source field changes. Existing database
privileges already permit SELECT; no additional accounts/passwords are created.

A rerun skips an existing table completely: it does not overwrite rows, reseed
an emptied table, or alter an existing schema. The initial INSERT is one
statement. MySQL DDL is not transactional with that INSERT: if provisioning
stops after CREATE but before INSERT, Gray must inspect and explicitly seed the
new table before competition. A missing table will be recreated by provisioning;
do not rerun provisioning against a live competition without intending that.
Check mode skips both scorecard SQL tasks and does not validate live SQL.

After correcting the outdated inventory, run the existing MySQL play only:

```sh
ansible-playbook -i inventory/inventory.yaml linux.yaml --limit mysql --become --ask-vault-pass
```

This uses the existing role, collection and Vault variables. `--limit mysql`
keeps unrelated service plays from targeting machines. To provision only the
scorecard on hosts whose database is already installed/configured, add
`--tags mysql_scorecard`.

On an isolated fixture/test database, verify five PASS rows; change Charlie's
`total_bases` from 8 to 9 and expect FAIL; change it back to 8 and expect PASS.
Rerun the role while the total is wrong and confirm it remains wrong. For
operator inspection use `SELECT player, total_bases, scorecard_status FROM
sandlot_scorecard`; the scorer will read only `scorecard_status`. Empty tables
must fail scoring; deletion of only some rows is not detected by this agreed
field-only contract. The scoring engine's existing SELECT 1 check still needs
to be updated separately.
