# psql-script-generator

It generates a SQL script based on a Jinja2 template, allowing you to automate the creation of a database, roles, and permissions.
It is particularly useful for setting up a PostgreSQL database with predefined roles and permissions.

## Installation:

```bash
# You can create a virtual env to install the cli

# Creating the venv
$ python -m venv tutorial_env

# Activating
$ source tutorial_env/bin/activate

# Installing the cli
pip install psql-script-generator

```

## Usage

```bash
$ psql-script-generator -d <database_name> -w <readwrite_role> -u <user_role> -p <password> -t <template_file> -o <output_file>
-d, --database: Name of the database.
-w, --readwrite_role: Name of the readwrite role.
-u, --user_role: Name of the users role.
-p, --password: Password for the user roles.
-t, --template: Path to the Jinja2 template file.
-o, --output_file: Output file for the generated SQL script.
```

Let's validate our generated sql script!!!

Start a PostgreSQL container:
```bash
$ docker run --name psql-validating -e POSTGRES_PASSWORD=mysecretpassword -p 5555:5432 -d postgres:13
```

Run generate_sql_script cli:
```bash
$ psql-script-generator -d test -w test_readwrite -u test_user -p 'qweasdzxc' -t readwrite-user-template.sql.j2 -o test_sql_script.sql
```

Run the generated SQL script:
```bash
$ export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d postgres -p 5555 -w -f test_sql_script.sql

# The output should be something like that:

CREATE DATABASE
CREATE ROLE
GRANT
GRANT
GRANT
GRANT
GRANT
GRANT
GRANT
ALTER DEFAULT PRIVILEGES
ALTER DEFAULT PRIVILEGES
ALTER DEFAULT PRIVILEGES
CREATE ROLE
GRANT ROLE
ALTER DATABASE

```

Now, let's test the grants that provided to test_user
```bash

# Download the validating.sql file
$ curl -o validating.sql https://raw.githubusercontent.com/pledo/psql-script-generator/main/validating.sql

# Run the sql script with write, read and delete permissions
export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_user -d postgres -p 5555 -w -f validating.sql

# The output should be something like:

CREATE TABLE
INSERT 0 1
 id |         title
----+------------------------
  1 | Learn basic SQL syntax
(1 row)

ALTER TABLE
UPDATE 1
 id |         title          | completed
----+------------------------+-----------
  1 | Learn basic SQL syntax | t
(1 row)

INSERT 0 1
DELETE 1
 id |         title          | completed
----+------------------------+-----------
  1 | Learn basic SQL syntax | t
(1 row)

DROP TABLE

```

Uninstall cli
```bash
$ pip uninstall psql-script-generator

and deactive the venv

$ deactivate
```

### For a full automated tests

Enter tests folder
```bash
$ cd tests
```

Run the bash script
```bash
bash full_test.sh
```
