import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Snowflake Security Setup - Perimeter",
    page_icon="🔒",
    layout="wide"
)

# Title and description
st.title("Snowflake Security Perimeter Setup")
st.markdown("### Network Rules, Network Policy, Session Policy, and Authentication Policy")
st.markdown("---")

# Input section
st.subheader("📝 Configuration")
col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input(
        "Company Name",
        placeholder="Enter your company name (e.g., acme)",
        help="Used to prefix network rules and policies"
    )

with col2:
    allowed_ips = st.text_input(
        "Allowed IP Range",
        value="192.0.0.1/24",
        help="CIDR notation for allowed IPs (e.g., 192.0.0.1/24)"
    )

col3, col4 = st.columns(2)

with col3:
    blocked_ip = st.text_input(
        "Blocked IP",
        value="184.0.23.212",
        help="Single IP address to block"
    )

with col4:
    session_timeout = st.number_input(
        "Session Idle Timeout (minutes)",
        min_value=5,
        max_value=480,
        value=30,
        help="Idle timeout for user sessions"
    )

# Only show content if company name is provided
if company_name:
    st.markdown("---")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Policy Overview", "📜 Generated SQL", "📚 Documentation"])
    
    with tab1:
        st.subheader("Security Policy Configuration")
        
        # Network Policy Section
        st.markdown("### 🌐 Network Policy")
        st.markdown("""
        Network policies control access based on IP addresses. This configuration includes:
        - **Allowed Network Rule**: Permits access from specified IP ranges (e.g., VPN, office networks)
        - **Blocked Network Rule**: Denies access from specific IPs
        - **Network Policy**: Combines both rules to enforce access control
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✅ **Allowed IPs:** {allowed_ips}")
        with col2:
            st.error(f"🚫 **Blocked IP:** {blocked_ip}")
        
        st.markdown("---")
        
        # Session Policy Section
        st.markdown("### ⏱️ Session Policy")
        st.markdown("""
        Session policies control user session behavior and timeouts:
        - **Idle Timeout**: Automatically logs out inactive users
        - **UI Timeout**: Separate timeout for web UI sessions
        - Can be applied at account or user level
        """)
        
        st.info(f"🕐 **Session Timeout:** {session_timeout} minutes")
        
        st.markdown("---")
        
        # Authentication Policy Section
        st.markdown("### 🔐 Authentication Policy")
        st.markdown("""
        Authentication policies define authentication requirements:
        - **MFA Enrollment**: Requires multi-factor authentication
        - **Client Types**: Specifies which clients can authenticate (UI, CLI, etc.)
        - Enhances security by enforcing stricter authentication
        """)
        
        auth_col1, auth_col2 = st.columns(2)
        with auth_col1:
            st.success("✅ **MFA:** Required")
        with auth_col2:
            st.success("✅ **Allowed Clients:** Snowflake UI, Snowflake CLI")
    
    with tab2:
        st.subheader("Generated SQL Script")
        st.markdown("This script sets up the complete security perimeter for your Snowflake account.")
        
        # Generate the SQL with replacements
        sql_script = f"""-- ============================================================================
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

CREATE NETWORK RULE SECURITY_SCHEMA.{company_name}_allowed_ips
    TYPE = IPV4
    VALUE_LIST = ('{allowed_ips}')
    MODE = INGRESS
    COMMENT = 'Allow access from specified IPs and subnets (VPN for instance)';

CREATE NETWORK RULE SECURITY_SCHEMA.{company_name}_blocked_ips
    TYPE = IPV4
    VALUE_LIST = ('{blocked_ip}')
    MODE = INGRESS
    COMMENT = 'Block access from specified IPs';

CREATE OR REPLACE NETWORK POLICY {company_name}_network_policy
    ALLOWED_NETWORK_RULE_LIST = ({company_name}_allowed_ips)
    BLOCKED_NETWORK_RULE_LIST = ({company_name}_blocked_ips)
    COMMENT = 'Network policy for {company_name}';

    

-- ============================================================================
-- 3. SESSION POLICY
-- ============================================================================
-- Session policies control user session behavior and timeouts
-- Idle timeout set to {session_timeout} minutes as specified
-- Ref: https://docs.snowflake.com/en/sql-reference/sql/create-session-policy
-- Can be applied to account or user

CREATE OR REPLACE SESSION POLICY SECURITY_DB.SECURITY_SCHEMA.standard_session_policy
    SESSION_IDLE_TIMEOUT_MINS = {session_timeout}
    SESSION_UI_IDLE_TIMEOUT_MINS = {session_timeout}
    COMMENT = 'Standard session policy with {session_timeout}-minute idle timeout';


-- ============================================================================
-- 4. AUTHENTICATION POLICY
-- ============================================================================
-- Authentication policies define authentication requirements for users
-- This policy allows Snowflake UI access and CLI access
-- Ref: https://docs.snowflake.com/en/sql-reference/sql/create-authentication-policy

CREATE OR REPLACE AUTHENTICATION POLICY SECURITY_DB.SECURITY_SCHEMA.ui_cli_auth_policy
  MFA_ENROLLMENT = REQUIRED
  CLIENT_TYPES = ('SNOWFLAKE_UI', 'SNOWFLAKE_CLI');


-- ============================================================================
-- 5. APPLY POLICIES (OPTIONAL)
-- ============================================================================
-- Apply network policy to account
-- ALTER ACCOUNT SET NETWORK_POLICY = {company_name}_network_policy;

-- Apply session policy to account
-- ALTER ACCOUNT SET SESSION_POLICY = SECURITY_DB.SECURITY_SCHEMA.standard_session_policy;

-- Apply authentication policy to account
-- ALTER ACCOUNT SET AUTHENTICATION POLICY = SECURITY_DB.SECURITY_SCHEMA.ui_cli_auth_policy;

-- Or apply to specific users:
-- ALTER USER <username> SET NETWORK_POLICY = {company_name}_network_policy;
-- ALTER USER <username> SET SESSION POLICY = SECURITY_DB.SECURITY_SCHEMA.standard_session_policy;
-- ALTER USER <username> SET AUTHENTICATION POLICY = SECURITY_DB.SECURITY_SCHEMA.ui_cli_auth_policy;
"""
        
        st.code(sql_script, language='sql')
        
        # Download button
        st.download_button(
            label="📥 Download SQL Script",
            data=sql_script,
            file_name=f"security_perimeter_setup_{company_name}.sql",
            mime="text/plain"
        )
    
    with tab3:
        st.subheader("📚 Documentation & Best Practices")
        
        st.markdown("### Network Rules and Policies")
        st.markdown("""
        **Network Rules** define IP-based access controls:
        - Use CIDR notation for IP ranges (e.g., `192.168.1.0/24`)
        - Can specify `INGRESS` (incoming) or `EGRESS` (outgoing) mode
        - Support both IPv4 and IPv6 addresses
        
        **Network Policies** combine multiple network rules:
        - `ALLOWED_NETWORK_RULE_LIST`: IPs that can access
        - `BLOCKED_NETWORK_RULE_LIST`: IPs that are denied (takes precedence)
        - Can be applied at account or user level
        
        📖 [Network Rules Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-network-rule)
        📖 [Network Policy Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-network-policy)
        """)
        
        st.markdown("---")
        
        st.markdown("### Session Policies")
        st.markdown("""
        **Session Policies** control user session behavior:
        - `SESSION_IDLE_TIMEOUT_MINS`: Timeout for idle sessions (CLI, drivers)
        - `SESSION_UI_IDLE_TIMEOUT_MINS`: Timeout for web UI sessions
        - Range: 5-480 minutes
        - Applied at account or user level
        
        📖 [Session Policy Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-session-policy)
        """)
        
        st.markdown("---")
        
        st.markdown("### Authentication Policies")
        st.markdown("""
        **Authentication Policies** enforce authentication requirements:
        - `MFA_ENROLLMENT`: Require multi-factor authentication (`REQUIRED` or `OPTIONAL`)
        - `CLIENT_TYPES`: Restrict which clients can authenticate
          - `SNOWFLAKE_UI`: Web interface
          - `SNOWFLAKE_CLI`: Command-line interface
          - `DRIVERS`: JDBC, ODBC, Python, etc.
        
        📖 [Authentication Policy Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-authentication-policy)
        """)
        
        st.markdown("---")
        
        st.markdown("### Best Practices")
        st.markdown("""
        1. **Start Restrictive**: Begin with strict policies and relax as needed
        2. **Test First**: Apply policies to test users before account-wide deployment
        3. **Document IPs**: Maintain a record of all allowed IP ranges and their purpose
        4. **Regular Review**: Periodically review and update network rules
        5. **MFA Always**: Require MFA for all production accounts
        6. **Reasonable Timeouts**: Balance security with user experience (30-60 min typical)
        7. **Monitor Access**: Use query history to track policy effectiveness
        """)

else:
    st.info("👆 Please enter your Company Name to see the configuration and generated SQL.")

# Footer
st.markdown("---")
st.markdown("*This page helps you set up the security perimeter for your Snowflake account including network policies, session policies, and authentication policies.*")
st.markdown("**Next Step:** Check out the RBAC Setup page to configure role-based access control.")

