-- ================================================================================
-- rbac_educational_app Setup Script
-- 
-- This script sets up the complete environment for the educational
-- Streamlit application including database, permissions, git integration,
-- and the Streamlit app itself.
--
-- Requirements:
-- - ACCOUNTADMIN role to create roles, databases, and integrations
-- - Git repository: https://github.com/mpkeet9/sf_account_basics_educational_app.git
-- ================================================================================

USE ROLE ACCOUNTADMIN;

-- ================================================================================
-- 1. CREATE DATABASES AND SCHEMAS
-- ================================================================================

-- Create main demo database
CREATE DATABASE IF NOT EXISTS ACCOUNT_BASICS_APP_DB
    COMMENT = 'Database for sf_account_basics_educational_app objects';

-- Create schema for the application
CREATE SCHEMA IF NOT EXISTS ACCOUNT_BASICS_APP_DB.APPLICATIONS
    COMMENT = 'Schema for Streamlit applications and notebooks';

-- ================================================================================
-- 2. CREATE COMPUTE RESOURCES
-- ================================================================================

-- Create warehouse for the application
CREATE WAREHOUSE IF NOT EXISTS ACCOUNT_BASICS_WH
    WITH 
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    COMMENT = 'Warehouse for sf_account_basics_educational_app application';

-- ================================================================================
-- 4. CREATE GIT INTEGRATION
-- ================================================================================

-- Create API integration for GitHub (requires ACCOUNTADMIN)
CREATE OR REPLACE API INTEGRATION ACCOUNT_BASICS_GIT_INTEGRATION
    API_PROVIDER = GIT_HTTPS_API
    API_ALLOWED_PREFIXES = ('https://github.com/mpkeet9/sf_account_basics_educational_app.git')
    ENABLED = TRUE
    COMMENT = 'API integration for sf_account_basics_educational_app GitHub repository';

-- Grant usage on integration to ACCOUNTADMIN
GRANT USAGE ON INTEGRATION ACCOUNT_BASICS_GIT_INTEGRATION TO ROLE ACCOUNTADMIN;

-- Create git repository object
USE ROLE ACCOUNTADMIN;
USE SCHEMA ACCOUNT_BASICS_APP_DB.APPLICATIONS;

CREATE OR REPLACE GIT REPOSITORY ACCOUNT_BASICS_REPO
    API_INTEGRATION = ACCOUNT_BASICS_GIT_INTEGRATION
    GIT_CREDENTIALS = NULL  -- For public repositories
    ORIGIN = 'https://github.com/mpkeet9/sf_account_basics_educational_app.git'
    COMMENT = 'sf_account_basics_educational_app repository containing Streamlit application';


-- ================================================================================
-- 5. CREATE STREAMLIT APPLICATION
-- ================================================================================

-- Switch to the application schema
USE SCHEMA ACCOUNT_BASICS_APP_DB.APPLICATIONS;
USE WAREHOUSE ACCOUNT_BASICS_WH;

-- Create the Streamlit application
CREATE OR REPLACE STREAMLIT ACCOUNT_BASICS_APP
    ROOT_LOCATION = '@ACCOUNT_BASICS_APP_DB.APPLICATIONS.ACCOUNT_BASICS_REPO/branches/main'
    MAIN_FILE = '/streamlit_app.py'
    QUERY_WAREHOUSE = SI_DEMO_WH
    COMMENT = 'Account Basics Streamlit Application'
    TITLE = 'Snowflake Account Basics Streamlit Application';

-- Grant usage on the Streamlit app to ACCOUNTADMIN
GRANT USAGE ON STREAMLIT ACCOUNT_BASICS_APP TO ROLE ACCOUNTADMIN;
