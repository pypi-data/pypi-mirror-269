#!/bin/bash

# Inside the repo's root
temp=$( realpath "$0"  ) && dirname "$temp"|cd
pwd
cd ../
pwd

echo -e "\n ### Building and installing"
# Creating venv and activating the env
python3.11 -m venv tutorial_env 
source tutorial_env/bin/activate

# Upgrading pip
python -m pip  install --upgrade pip

# Installing build and run dependencies
python -m pip  install build jinja2 twine

# Building the package
python -m build

# Installing locally
pip install -e .

#--------- Testing cli
echo -e "\n ### Testing"

# Running cli
tutorial_env/bin/psql-script-generator -d test -r test_readwrite -u test_user -p 'qweasdzxc' -t readwrite-user-template.sql.j2 -o test_sql_script.sql
tutorial_env/bin/psql-script-generator -d test_ro -r test_readonly -u test_ro_user -p 'qweasdzxc' -t readonly-user-template.sql.j2 -o test_ro_sql_script.sql

# Starting postgres docker container
 docker run --name psql-validating -e POSTGRES_PASSWORD=mysecretpassword -p 5555:5432 -d postgres:13 ;sleep 5

# Running the SQL script inside the postgres database
export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d postgres -p 5555 -w -f test_sql_script.sql
export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d postgres -p 5555 -w -f test_ro_sql_script.sql

#Testing the user_test grants

echo -e "\n ### Validating rw user grants ### \n"
export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_user -d postgres -p 5555 -w -f validating.sql

echo -e "\n ### Validating ro user grants ### \n"
export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d test_ro -p 5555 -w -f validating_setup_for_ro_user.sql
export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_ro_user -d test_ro -p 5555 -w -f validating_ro.sql

echo -e "\n ### Cleaning the env"
# Stopping and deleting the postgres container
docker stop psql-validating; docker rm psql-validating

# Uninstall cli
pip uninstall -y psql-script-generator

# Deleting dist folder
rm -rf dist

# Deleting sql script
 rm test_sql_script.sql test_ro_sql_script.sql

# Deactivating venv
deactivate

# Deleting venv folder
rm -rf tutorial_env
