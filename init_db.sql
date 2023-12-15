-- init_db.sql

-- Connect to the default PostgreSQL database (usually 'postgres')
\c postgres postgres

-- Create a new database with a specific name
CREATE DATABASE travel_agency;

-- Set the owner of the database
ALTER DATABASE travel_agency OWNER TO postgres;

--Run sudo docker exec -i travel_agency psql -U postgres < init_db.sql

