# Database Service

Sets up a MySQL database service on Linux.

## Features
- Creates a default database
- Creates a low privilege user
- Creates a high privilege user

## Deployment
The controller needs the `community.mysql` collection installed:

`ansible-galaxy collection install community.mysql`

Then the database role can be added to the Linux playbook and run on the target.
