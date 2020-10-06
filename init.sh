#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER contact1;
    CREATE DATABASE contact;
    GRANT ALL PRIVILEGES ON DATABASE contact TO contact1;
EOSQL
