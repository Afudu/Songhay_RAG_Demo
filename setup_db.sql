-- =============================================================
-- Songhay Glossary RAG App — PostgreSQL setup
-- Run once as the postgres superuser:
--   psql -U postgres -f setup_db.sql
-- =============================================================

-- 1. Create the database and dedicated user
CREATE DATABASE songhay_glossary_db;
CREATE USER songhay_glossary_user WITH PASSWORD '123456';
GRANT ALL PRIVILEGES ON DATABASE songhay_glossary_db TO songhay_glossary_user;

-- 2. Switch into the new database
--  Everything below runs inside songhay_glossary_db
\c songhay_glossary_db

-- 3. Grant schema access (required in PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO songhay_glossary_db_user;

-- 4. Enable pgvector extension (must be done as superuser)
CREATE EXTENSION IF NOT EXISTS vector;

-- 5. Verify pgvector is installed
SELECT * FROM pg_extension WHERE extname = 'vector';