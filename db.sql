CREATE DATABASE sawaaldb;
CREATE USER sawaaluser WITH ENCRYPTED PASSWORD 'sawaalpassword';
ALTER ROLE sawaaluser SET client_encoding TO 'utf8';
ALTER ROLE sawaaluser SET default_transaction_isolation TO 'read committed';
ALTER ROLE sawaaluser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sawaaldb TO sawaaluser;

ALTER ROLE  sawaaluser CREATEDB ; -- Required only for running Unit tests locally.
\q
