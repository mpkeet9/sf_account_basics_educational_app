-- ================================================================================
-- rbac_educational_app Setup Script
-- 
-- This script sets up the complete environment for the educational
-- Streamlit application including database, permissions, git integration,
-- and the Streamlit app itself.
--
-- Requirements:
-- - ACCOUNTADMIN role to create roles, databases, and integrations
-- - Git repository: https://github.com/kfir-liron-snowflake/SI_Data_Generator
-- ================================================================================

USE ROLE ACCOUNTADMIN;
