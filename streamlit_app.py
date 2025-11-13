import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Snowflake Security Examples",
    page_icon="❄️",
    layout="wide"
)

# Title and description
st.title("❄️ Snowflake Security Configuration Examples")
st.markdown("### Interactive guides for Snowflake security best practices")
st.markdown("---")

# Introduction
st.markdown("""
Welcome to the Snowflake Security Configuration Examples! This application provides interactive guides 
for setting up security configurations in Snowflake.

### 📚 Available Guides

Use the sidebar to navigate between the different configuration guides:

#### 🔒 Perimeter Setup
Configure the security perimeter for your Snowflake account:
- **Network Policies**: Control IP-based access
- **Session Policies**: Manage session timeouts
- **Authentication Policies**: Enforce MFA and client restrictions

#### 🗄️ RBAC Setup
Set up Role-Based Access Control (RBAC) for your databases:
- **Database Roles**: Create read, create, and write roles
- **Schema Access**: Configure managed access schemas
- **Functional Roles**: Set up analyst, developer, and support roles

---

### 🚀 Getting Started

1. **Choose a guide** from the sidebar
2. **Fill in your configuration** details
3. **Review the generated SQL** and visualizations
4. **Download the script** and run it in Snowflake

---

### 💡 Best Practices

- Start with the **Perimeter Setup** to secure your account
- Then configure **RBAC Setup** for each database
- Test policies on individual users before applying account-wide
- Document all security configurations for your team

---

""")

# Quick links
st.markdown("### 📖 Useful Resources")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Network Security**
    - [Network Policies](https://docs.snowflake.com/en/user-guide/network-policies)
    - [Network Rules](https://docs.snowflake.com/en/sql-reference/sql/create-network-rule)
    """)

with col2:
    st.markdown("""
    **Session & Auth**
    - [Session Policies](https://docs.snowflake.com/en/sql-reference/sql/create-session-policy)
    - [Authentication Policies](https://docs.snowflake.com/en/sql-reference/sql/create-authentication-policy)
    """)

with col3:
    st.markdown("""
    **Access Control**
    - [RBAC Overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
    - [Database Roles](https://docs.snowflake.com/en/user-guide/security-access-control-considerations)
    """)

# Footer
st.markdown("---")
st.markdown("*Built for demonstrating Snowflake security best practices*")
