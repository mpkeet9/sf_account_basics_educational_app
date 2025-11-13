-- ============================================================================
-- 1. PREPPING THE ROLE SECURITY CONFIGURATION
-- ============================================================================
USE ROLE SYSADMIN;

CREATE DATABASE IF NOT EXISTS SECURITY_DB;
CREATE SCHEMA IF NOT EXISTS SECURITY_DB.SECURITY_SCHEMA;
USE DATABASE SECURITY_DB;
USE SCHEMA SECURITY_SCHEMA;

GRANT USAGE ON DATABASE SECURITY_DB TO ROLE SECURITYADMIN;
GRANT USAGE ON SCHEMA SECURITY_DB.SECURITY_SCHEMA TO ROLE SECURITYADMIN;
GRANT SELECT ON ALL TABLES IN SCHEMA SECURITY_DB.SECURITY_SCHEMA TO ROLE SECURITYADMIN;
GRANT SELECT ON FUTURE TABLES IN SCHEMA SECURITY_DB.SECURITY_SCHEMA TO ROLE SECURITYADMIN;
GRANT CREATE SESSION POLICY ON SCHEMA SECURITY_DB.SECURITY_SCHEMA TO ROLE SECURITYADMIN;
GRANT CREATE NETWORK RULE ON SCHEMA SECURITY_DB.SECURITY_SCHEMA TO ROLE SECURITYADMIN;
GRANT CREATE SESSION POLICY ON SCHEMA SECURITY_DB.SECURITY_SCHEMA TO ROLE SECURITYADMIN;
GRANT CREATE AUTHENTICATION POLICY ON SCHEMA SECURITY_DB.SECURITY_SCHEMA TO ROLE SECURITYADMIN;

GRANT CREATE NETWORK POLICY ON ACCOUNT TO ROLE SECURITYADMIN;


USE ROLE SECURITYADMIN;

-- ============================================================================
-- 2. NETWORK RULES AND POLICY
-- ============================================================================
-- Network rules define access controls for external network locations
-- (used with external access integrations for data egress)
-- Ref: https://docs.snowflake.com/en/sql-reference/sql/create-network-rule

CREATE NETWORK RULE SECURITY_SCHEMA.yourcompanyname_allowed_ips
    TYPE = IPV4
    VALUE_LIST = ('192.0.0.1/24')
    MODE = INGRESS
    COMMENT = 'Allow access from specified IPs and subnets (VPN for instance)';

CREATE NETWORK RULE SECURITY_SCHEMA.yourcompanyname_blocked_ips
    TYPE = IPV4
    VALUE_LIST = (184.0.23.212)
    MODE = INGRESS
    COMMENT = 'Allow access from specified IPs and subnets (VPN for instance)';

CREATE OR REPLACE NETWORK POLICY yourcompanyname_network_policy
    ALLOWED_NETWORK_RULE_LIST = (yourcompanyname_allowed_ips)
    BLOCKED_NETWORK_RULE_LIST = (yourcompanyname_blocked_ips)
    COMMENT = 'Network policy for your company';

    

-- ============================================================================
-- 3. SESSION POLICY
-- ============================================================================
-- Session policies control user session behavior and timeouts
-- Idle timeout set to 30 minutes as specified
-- Ref: https://docs.snowflake.com/en/sql-reference/sql/create-session-policy
-- Can be applied to account or user

CREATE OR REPLACE SESSION POLICY SECURITY_DB.SECURITY_SCHEMA.standard_session_policy
    SESSION_IDLE_TIMEOUT_MINS = 30SECURITY_DB.SECURITY_SCHEMA
    SESSION_UI_IDLE_TIMEOUT_MINS = 30
    COMMENT = 'Standard session policy with 30-minute idle timeout';


-- ============================================================================
-- 4. AUTHENTICATION POLICY
-- ============================================================================
-- Authentication policies define authentication requirements for users
-- This policy allows Snowflake UI access and CLI access
-- Ref: https://docs.snowflake.com/en/sql-reference/sql/create-authentication-policy

CREATE OR ALTER AUTHENTICATION POLICY SECURITY_DB.SECURITY_SCHEMA.ui_cli_auth_policy
  MFA_ENROLLMENT = REQUIRED
  CLIENT_TYPES = ('SNOWFLAKE_UI', 'SNOWFLAKE_CLI');