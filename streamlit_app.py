import streamlit as st
import graphviz

# Page configuration
st.set_page_config(
    page_title="RBAC Database Setup - Page 1",
    page_icon="🗄️",
    layout="wide"
)

# Title and description
st.title("🗄️ Snowflake RBAC Database Setup")
st.markdown("### Complete RBAC Structure: Database, Schema, and Access Roles")
st.markdown("---")

# Input section
st.subheader("📝 Configuration")
col1, col2 = st.columns(2)

with col1:
    database_name = st.text_input(
        "Database Name",
        placeholder="Enter database name (e.g., MARKETING_DB)",
        help="The name of the database to create"
    )

with col2:
    schema_name = st.text_input(
        "Schema Name",
        placeholder="Enter schema name (e.g., CRM_SCHEMA)",
        help="The name of the managed access schema to create"
    )

# Only show visualizations if both inputs are provided
if database_name and schema_name:
    st.markdown("---")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Visual Diagram", "📜 Generated SQL", "🧪 Test Personas"])
    
    with tab1:
        st.subheader("Role Hierarchy and Permissions")
        
        # Create a graphviz diagram
        dot = graphviz.Digraph(comment='RBAC Structure')
        dot.attr(rankdir='TB', size='14,10', compound='true', splines='ortho', nodesep='0.6', ranksep='0.8')
        dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='11')
        
        # Role names
        admin_role = f'RL_{database_name}_ADMIN'
        read_role = f'DB_R_DBR_{database_name}'
        create_role = f'DB_C_DBR_{database_name}'
        write_role = f'DB_W_DBR_{database_name}'
        
        # Schema access roles
        schema_read_role = f'SC_R_DBR_{database_name}'
        schema_create_role = f'SC_C_DBR_{database_name}'
        schema_write_role = f'SC_W_DBR_{database_name}'
        
        # Account level functional roles
        analyst_role = f'{database_name}_ANALYST'
        developer_role = f'{database_name}_DEVELOPER'
        support_role = f'{database_name}_SUPPORT'
        
        # Level labels (all with same group to align vertically on left)
        dot.node('LABEL_ACCOUNT', 'Object\nAdmin', shape='plaintext', fontsize='12', fontname='Arial Bold',
                width='1.5', height='0.6', fixedsize='true', group='labels')
        dot.node('LABEL_PROJECT', 'Project\nAdmin', shape='plaintext', fontsize='12', fontname='Arial Bold',
                width='1.5', height='0.6', fixedsize='true', group='labels')
        dot.node('LABEL_FUNCTIONAL', 'Functional\nAccess', shape='plaintext', fontsize='12', fontname='Arial Bold',
                width='1.5', height='0.6', fixedsize='true', group='labels')
        dot.node('LABEL_SCHEMA_ACCESS', 'Schema\nAccess', shape='plaintext', fontsize='12', fontname='Arial Bold',
                width='1.5', height='0.6', fixedsize='true', group='labels')
        
        # Keep labels vertically aligned with invisible edges
        dot.edge('LABEL_ACCOUNT', 'LABEL_PROJECT', style='invis')
        dot.edge('LABEL_PROJECT', 'LABEL_FUNCTIONAL', style='invis')
        dot.edge('LABEL_FUNCTIONAL', 'LABEL_SCHEMA_ACCESS', style='invis')
        
        # SYSADMIN  Level
        with dot.subgraph() as s:
            s.attr(rank='same')
            s.node('LABEL_ACCOUNT')
            s.node('SYSADMIN', 'SYSADMIN', 
                  fillcolor='#7CC7E8', color='#2980B9', fontcolor='white', 
                  style='rounded,filled', width='2', height='0.8')
            # Invisible edge to keep label on left
            s.edge('LABEL_ACCOUNT', 'SYSADMIN', style='invis')
        
        # Center SYSADMIN over database cluster
        dot.edge('SYSADMIN', 'CREATE_ROLE', style='invis', minlen='1')
        
        # Project Admin Level
        with dot.subgraph() as s:
            s.attr(rank='same')
            s.node('LABEL_PROJECT')
            s.node('ADMIN_ROLE', f'{admin_role}', 
                  fillcolor='#C67BA0', color='#922B5E', fontcolor='white',
                  style='rounded,filled', width='2.5', height='0.8')
            # Invisible edge to keep label on left
            s.edge('LABEL_PROJECT', 'ADMIN_ROLE', style='invis')
        
        # Center ADMIN_ROLE over database cluster
        dot.edge('ADMIN_ROLE', 'CREATE_ROLE', style='invis', minlen='1')
        
        # Functional Access Level - Account roles
        with dot.subgraph() as s:
            s.attr(rank='same')
            s.node('LABEL_FUNCTIONAL')
            s.node('ANALYST_ROLE', f'{analyst_role}', 
                  fillcolor='#5DADE2', color='#21618C', fontcolor='white',
                  style='rounded,filled', width='2', height='0.8')
            s.node('DEVELOPER_ROLE', f'{developer_role}', 
                  fillcolor='#48C9B0', color='#117A65', fontcolor='white',
                  style='rounded,filled', width='2', height='0.8')
            s.node('SUPPORT_ROLE', f'{support_role}', 
                  fillcolor='#F8C471', color='#B7950B', fontcolor='white',
                  style='rounded,filled', width='2', height='0.8')
            # Invisible edges to keep label on left and roles ordered
            s.edge('LABEL_FUNCTIONAL', 'ANALYST_ROLE', style='invis')
            s.edge('ANALYST_ROLE', 'DEVELOPER_ROLE', style='invis')
            s.edge('DEVELOPER_ROLE', 'SUPPORT_ROLE', style='invis')
        
        # Align functional roles to span the full width of database cluster
        # Connect each functional role to its corresponding DB role below
        dot.edge('ANALYST_ROLE', 'READ_ROLE', style='invis', minlen='1', weight='10')
        dot.edge('DEVELOPER_ROLE', 'CREATE_ROLE', style='invis', minlen='1', weight='10')
        dot.edge('SUPPORT_ROLE', 'WRITE_ROLE', style='invis', minlen='1', weight='12')
        
        # Database level - large container
        with dot.subgraph(name='cluster_database') as db:
            db.attr(label=f'Database: {database_name}', 
                   labelloc='b', labeljust='l',
                   style='rounded,filled', 
                   fillcolor='#B8D4E8',
                   color='#2C5F7C',
                   fontcolor='#1F618D',
                   fontsize='13',
                   fontname='Arial Bold',
                   penwidth='3',
                   margin='25')
            
            # Database Roles inside database but outside schema (horizontal)
            db.node('READ_ROLE', f'{read_role}\n \nRead (R)', 
                      fillcolor='#9B59B6', color='#6C3483', fontcolor='white',
                      width='2', height='1')
            db.node('CREATE_ROLE', f'{create_role}\n \nCreate (C)', 
                      fillcolor='#9B59B6', color='#6C3483', fontcolor='white',
                      width='2', height='1')
            db.node('WRITE_ROLE', f'{write_role}\n \nWrite (W)', 
                      fillcolor='#9B59B6', color='#6C3483', fontcolor='white',
                      width='2', height='1')
            
            # Force all database roles to be on the same horizontal rank
            with db.subgraph() as db_roles:
                db_roles.attr(rank='same')
                db_roles.node('READ_ROLE')
                db_roles.node('CREATE_ROLE')
                db_roles.node('WRITE_ROLE')
            
            # Invisible edges for left-to-right ordering
            db.edge('READ_ROLE', 'CREATE_ROLE', style='invis')
            db.edge('CREATE_ROLE', 'WRITE_ROLE', style='invis')
            
            # Schema cluster inside database (below the roles)
            with db.subgraph(name='cluster_schema') as schema:
                schema.attr(label=f'Schema: {schema_name}', 
                          labelloc='b', labeljust='l',
                          style='rounded,filled',
                          fillcolor='#E8F4F8',
                          color='#34495E',
                          fontcolor='#2C3E50',
                          fontsize='12',
                          fontname='Arial Bold',
                          penwidth='2.5',
                          margin='20')
                
                # Schema access roles (inside the schema)
                schema.node('SCHEMA_READ_ROLE', f'{schema_read_role}\n(Schema Read)', 
                          fillcolor='#BB8FCE', color='#6C3483', fontcolor='white',
                          width='2', height='0.9')
                schema.node('SCHEMA_CREATE_ROLE', f'{schema_create_role}\n(Schema Create)', 
                          fillcolor='#BB8FCE', color='#6C3483', fontcolor='white',
                          width='2', height='0.9')
                schema.node('SCHEMA_WRITE_ROLE', f'{schema_write_role}\n(Schema Write)', 
                          fillcolor='#BB8FCE', color='#6C3483', fontcolor='white',
                          width='2', height='0.9')
                
                # Keep schema roles on same rank
                with schema.subgraph() as schema_roles:
                    schema_roles.attr(rank='same')
                    schema_roles.node('SCHEMA_READ_ROLE')
                    schema_roles.node('SCHEMA_CREATE_ROLE')
                    schema_roles.node('SCHEMA_WRITE_ROLE')
                
                # Invisible edges for ordering
                schema.edge('SCHEMA_READ_ROLE', 'SCHEMA_CREATE_ROLE', style='invis')
                schema.edge('SCHEMA_CREATE_ROLE', 'SCHEMA_WRITE_ROLE', style='invis')
                
                # Tables area inside schema (below schema roles)
                schema.node('TABLES_AREA', 'Tables\n(Future Objects)', 
                          fillcolor='#F39C12', color='#D68910', fontcolor='white',
                          shape='cylinder', width='5', height='1.2')
                
                # Connect schema roles to tables
                schema.edge('SCHEMA_READ_ROLE', 'TABLES_AREA', style='dashed', color='#7F8C8D', arrowhead='vee')
                schema.edge('SCHEMA_CREATE_ROLE', 'TABLES_AREA', style='dashed', color='#7F8C8D', arrowhead='vee')
                schema.edge('SCHEMA_WRITE_ROLE', 'TABLES_AREA', style='dashed', color='#7F8C8D', arrowhead='vee')
            
            # Connect database roles to schema roles (inheritance/grants)
            db.edge('READ_ROLE', 'SCHEMA_READ_ROLE', color='#9B59B6', penwidth='1.5', style='dashed')
            db.edge('READ_ROLE', 'SCHEMA_CREATE_ROLE', color='#9B59B6', penwidth='1.5', style='dashed')
            db.edge('READ_ROLE', 'SCHEMA_WRITE_ROLE', color='#9B59B6', penwidth='1.5', style='dashed')
            
            # Invisible edge to keep schema below roles
            db.edge('CREATE_ROLE', 'SCHEMA_CREATE_ROLE', style='invis')
        
        # Keep Schema Access label on the left, aligned with schema area
        # Use constraint and minlen to position label at schema level
        dot.edge('LABEL_FUNCTIONAL', 'LABEL_SCHEMA_ACCESS', style='invis', minlen='2')
        dot.edge('LABEL_SCHEMA_ACCESS', 'TABLES_AREA', style='invis', constraint='false')
        
        # Relationships between levels
        dot.edge('SYSADMIN', 'ADMIN_ROLE', label='creates DB\ntransfers ownership', 
                color='#2980B9', penwidth='2', fontsize='10')
        
        # Admin role creates account roles
        dot.edge('ADMIN_ROLE', 'ANALYST_ROLE', label='creates', 
                color='#C67BA0', penwidth='1.5', fontsize='9')
        dot.edge('ADMIN_ROLE', 'DEVELOPER_ROLE', label='creates', 
                color='#C67BA0', penwidth='1.5', fontsize='9')
        dot.edge('ADMIN_ROLE', 'SUPPORT_ROLE', label='creates', 
                color='#C67BA0', penwidth='1.5', fontsize='9')
        
        # Admin role creates database roles
        dot.edge('ADMIN_ROLE', 'READ_ROLE', 
                color='#C67BA0', penwidth='1.5', fontsize='9', lhead='cluster_database')
        
        # Account roles are granted database roles (through schema roles)
        dot.edge('ANALYST_ROLE', 'SCHEMA_READ_ROLE', 
                color='#5DADE2', penwidth='1.2', fontsize='9', style='dashed')
        dot.edge('DEVELOPER_ROLE', 'SCHEMA_CREATE_ROLE', 
                color='#48C9B0', penwidth='1.2', fontsize='9', style='dashed')
        dot.edge('SUPPORT_ROLE', 'SCHEMA_WRITE_ROLE', 
                color='#F8C471', penwidth='1.2', fontsize='9', style='dashed')
        
        st.graphviz_chart(dot)
        
        # Legend
        st.markdown("#### Legend")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Hierarchy Levels:**")
            st.markdown("• Object Admin (SYSADMIN)")
            st.markdown("• Project Admin (Admin Role)")
            st.markdown("• Functional Access (Account Roles)")
            st.markdown("• Database Roles (Read, Create, Write)")
            st.markdown("• Schema Access Roles")
        with col2:
            st.markdown("**Relationships:**")
            st.markdown("➡️ **Solid**: Creates/Owns")
            st.markdown("⚪ **Dashed**: Permission grants")
    
    with tab2:
        st.subheader("Generated SQL Script")
        
        # Generate the SQL with replacements
        sql_script = f"""USE ROLE SYSADMIN;
USE SECONDARY ROLES NONE;
SET user_name = (SELECT CURRENT_USER());

CREATE WAREHOUSE IF NOT EXISTS SIMPLE_COMPUTE 
WITH 
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;

CREATE DATABASE IF NOT EXISTS {database_name}
    COMMENT = 'Marketing production CRM database with private access.';


USE ROLE SECURITYADMIN;

-- Create functional roles to manage the database
CREATE OR REPLACE ROLE RL_{database_name}_ADMIN;

-- Grant the role to the proper user
GRANT ROLE RL_{database_name}_ADMIN TO USER IDENTIFIER($user_name);;

-- Platform admin changes ownership to the DB_ADMIN role
GRANT OWNERSHIP ON DATABASE {database_name} TO ROLE RL_{database_name}_ADMIN;

-- Create Database Roles
USE ROLE RL_{database_name}_ADMIN;
USE DATABASE {database_name};

CREATE OR REPLACE DATABASE ROLE DB_R_DBR_{database_name}; -- read
CREATE OR REPLACE DATABASE ROLE DB_C_DBR_{database_name}; -- create
CREATE OR REPLACE DATABASE ROLE DB_W_DBR_{database_name}; -- write

SHOW DATABASE ROLES IN DATABASE {database_name};


-- Grant database permissions to database roles
GRANT USAGE ON DATABASE {database_name} TO DATABASE ROLE DB_R_DBR_{database_name};
GRANT CREATE SCHEMA ON DATABASE {database_name} TO DATABASE ROLE DB_C_DBR_{database_name};
GRANT ALL ON DATABASE {database_name} TO DATABASE ROLE DB_W_DBR_{database_name};

-- Create a Managed Access Schema
USE ROLE RL_{database_name}_ADMIN;

CREATE OR REPLACE SCHEMA {database_name}.{schema_name} WITH MANAGED ACCESS;

SHOW GRANTS ON SCHEMA {database_name}.{schema_name};


-- Create schema access roles using database roles
USE ROLE RL_{database_name}_ADMIN;


-- Create Schema access roles using database roles
CREATE OR REPLACE DATABASE ROLE SC_R_DBR_{database_name};
CREATE OR REPLACE DATABASE ROLE SC_C_DBR_{database_name};
CREATE OR REPLACE DATABASE ROLE SC_W_DBR_{database_name};

USE ROLE SYSADMIN;
USE WAREHOUSE SIMPLE_COMPUTE;
GRANT USAGE ON WAREHOUSE SIMPLE_COMPUTE TO ROLE RL_{database_name}_ADMIN;

USE ROLE RL_{database_name}_ADMIN;
USE WAREHOUSE SIMPLE_COMPUTE;
CREATE OR REPLACE TABLE {database_name}.{schema_name}.INVENTORY_LEVELS (
    INVENTORY_ID INT PRIMARY KEY,
    WAREHOUSE_ID INT NOT NULL,
    PRODUCT_ID INT NOT NULL,
    QUANTITY_ON_HAND INT DEFAULT 0,
    QUANTITY_RESERVED INT DEFAULT 0,
    REORDER_POINT INT DEFAULT 0,
    LAST_RESTOCK_DATE DATE,
    NEXT_REORDER_DATE DATE
) COMMENT = 'Inventory levels by warehouse and product';

INSERT INTO {database_name}.{schema_name}.INVENTORY_LEVELS (INVENTORY_ID, WAREHOUSE_ID, PRODUCT_ID, QUANTITY_ON_HAND, QUANTITY_RESERVED, REORDER_POINT, LAST_RESTOCK_DATE, NEXT_REORDER_DATE)
VALUES
    (701, 501, 101, 75, 10, 20, '2023-06-01', '2023-07-15'),
    (702, 501, 102, 35, 5, 15, '2023-06-01', '2023-07-01'),
    (703, 502, 101, 50, 8, 20, '2023-06-05', '2023-07-20'),
    (704, 502, 103, 250, 30, 50, '2023-06-10', '2023-08-01'),
    (705, 503, 104, 15, 2, 10, '2023-06-15', '2023-06-25'),
    (706, 503, 105, 60, 12, 25, '2023-06-12', '2023-07-30'),
    (707, 505, 102, 40, 6, 15, '2023-06-08', '2023-07-05');


-- Schema Object Grants
-- Read Only
GRANT USAGE ON SCHEMA {database_name}.{schema_name} TO DATABASE ROLE SC_R_DBR_{database_name};
GRANT SELECT ON ALL TABLES IN SCHEMA {database_name}.{schema_name} TO DATABASE ROLE SC_R_DBR_{database_name};
GRANT SELECT ON FUTURE TABLES IN SCHEMA {database_name}.{schema_name} TO DATABASE ROLE SC_R_DBR_{database_name};

-- create any object
GRANT ALL ON SCHEMA {database_name}.{schema_name} TO DATABASE ROLE SC_C_DBR_{database_name};
REVOKE MODIFY ON SCHEMA {database_name}.{schema_name} FROM DATABASE ROLE SC_C_DBR_{database_name};

-- write (allows renaming the schema)
GRANT ALL ON SCHEMA {database_name}.{schema_name} TO DATABASE ROLE SC_W_DBR_{database_name};

-- inheritance
GRANT DATABASE ROLE SC_R_DBR_{database_name} TO DATABASE ROLE SC_C_DBR_{database_name};
GRANT DATABASE ROLE SC_C_DBR_{database_name} TO DATABASE ROLE SC_W_DBR_{database_name};

SHOW GRANTS ON SCHEMA {database_name}.{schema_name};

-- grant database role to schema roles
USE ROLE RL_{database_name}_ADMIN;

GRANT DATABASE ROLE DB_R_DBR_{database_name} TO DATABASE ROLE SC_R_DBR_{database_name};
GRANT DATABASE ROLE DB_R_DBR_{database_name} TO DATABASE ROLE SC_C_DBR_{database_name};
GRANT DATABASE ROLE DB_R_DBR_{database_name} TO DATABASE ROLE SC_W_DBR_{database_name};


-- Create account level roles
USE ROLE SECURITYADMIN;

CREATE OR REPLACE ROLE {database_name}_ANALYST;
CREATE OR REPLACE ROLE {database_name}_DEVELOPER;
CREATE OR REPLACE ROLE {database_name}_SUPPORT;

-- grant schema roles to account roles
USE ROLE RL_{database_name}_ADMIN;
USE DATABASE {database_name};

GRANT DATABASE ROLE SC_R_DBR_{database_name} TO ROLE {database_name}_ANALYST;
GRANT DATABASE ROLE SC_C_DBR_{database_name} TO ROLE {database_name}_SUPPORT;
GRANT DATABASE ROLE SC_W_DBR_{database_name} TO ROLE {database_name}_DEVELOPER;

-- granting warehouse usage to our account roles
USE ROLE SYSADMIN;
GRANT USAGE ON WAREHOUSE SIMPLE_COMPUTE TO ROLE {database_name}_ANALYST;
GRANT USAGE ON WAREHOUSE SIMPLE_COMPUTE TO ROLE {database_name}_DEVELOPER;
GRANT USAGE ON WAREHOUSE SIMPLE_COMPUTE TO ROLE {database_name}_SUPPORT;

-- Granting roles to the user of your choice
USE ROLE SECURITYADMIN;
SET user_name = (SELECT CURRENT_USER());   
GRANT ROLE {database_name}_ANALYST TO USER IDENTIFIER($user_name);
GRANT ROLE {database_name}_DEVELOPER TO USER IDENTIFIER($user_name);
GRANT ROLE {database_name}_SUPPORT TO USER IDENTIFIER($user_name);

SHOW GRANTS ON DATABASE {database_name};
SHOW GRANTS ON SCHEMA {database_name}.{schema_name};

-- USE ROLE SECURITYADMIN;
-- DROP ROLE IF EXISTS {database_name}_ANALYST;
-- DROP ROLE IF EXISTS {database_name}_DEVELOPER;
-- DROP ROLE IF EXISTS {database_name}_SUPPORT;

-- USE ROLE RL_{database_name}_ADMIN;
-- DROP DATABASE IF EXISTS {database_name};
-- USE ROLE SECURITYADMIN;
-- DROP ROLE IF EXISTS RL_{database_name}_ADMIN;
"""
        
        st.code(sql_script, language='sql')
        
        # Download button
        st.download_button(
            label="📥 Download SQL Script",
            data=sql_script,
            file_name=f"rbac_setup_{database_name}_{schema_name}.sql",
            mime="text/plain"
        )
    
    with tab3:
        st.subheader("🧪 Test User Personas")
        st.markdown("Test different user roles to see what permissions they have in the database.")
        
        # Persona selection
        st.markdown("### Select User Persona")
        persona = st.selectbox(
            "Choose a role to test:",
            [
                f"{database_name}_ANALYST (Read Only)",
                f"{database_name}_DEVELOPER (Read & Write)",
                f"{database_name}_SUPPORT (Full Access)"
            ]
        )
        
        # Extract the role name from the selection
        role_name = persona.split(" ")[0]
        
        # Note about testing
        st.info(f"""
**Testing as {role_name}:**

To test this persona's permissions in your Snowflake workspace:

Copy and paste the example queries below into a Snowflake worksheet to test the permissions.
        """)
        
        # Examples section
        st.markdown("### 💡 Example Queries to Test")
        
        example_col1, example_col2, example_col3 = st.columns(3)
        
        with example_col1:
            st.markdown("**As ANALYST (Read Only):**")
            st.code(f"""
USE ROLE {database_name}_ANALYST;
USE SECONDARY ROLES NONE;
USE WAREHOUSE SIMPLE_COMPUTE;

-- ✅ Read is successful
SELECT * FROM {database_name}.{schema_name}.INVENTORY_LEVELS LIMIT 3;

-- ❌ Cannot create a table
CREATE OR REPLACE TABLE {database_name}.{schema_name}.ENGAGEMENT_LEVELS (
    ENGAGEMENT_ID INT PRIMARY KEY,
    ENGAGEMENT_LEVEL DATE
);

-- ❌ Cannot insert to existing table
INSERT INTO {database_name}.{schema_name}.INVENTORY_LEVELS 
VALUES (701, 501, 101, 75, 10, 20, '2023-06-01', '2023-07-15');
            """, language="sql")
        
        with example_col2:
            st.markdown("**As SUPPORT (Create Objects):**")
            st.code(f"""
USE ROLE {database_name}_SUPPORT;
USE SECONDARY ROLES NONE;
USE WAREHOUSE SIMPLE_COMPUTE;

-- ✅ Read is successful
SELECT * FROM {database_name}.{schema_name}.INVENTORY_LEVELS LIMIT 3;

-- ✅ Can create a table
CREATE OR REPLACE TABLE {database_name}.{schema_name}.ENGAGEMENT_LEVELS (
    ENGAGEMENT_ID INT PRIMARY KEY,
    ENGAGEMENT_LEVEL INT
);

-- ✅ Can insert data
INSERT INTO {database_name}.{schema_name}.ENGAGEMENT_LEVELS 
VALUES (1, 1);

-- ✅ Can drop table
DROP TABLE IF EXISTS {database_name}.{schema_name}.ENGAGEMENT_LEVELS;

-- ❌ Cannot modify the existing schema
ALTER SCHEMA {database_name}.{schema_name} SET COMMENT = 'test?';

-- ❌ Cannot create outside of this schema
CREATE SCHEMA {database_name}.SANDBOX;


            """, language="sql")
        
        with example_col3:
            st.markdown("**As DEVELOPER (Full Write):**")
            st.code(f"""
USE ROLE {database_name}_DEVELOPER;
USE SECONDARY ROLES NONE;
USE WAREHOUSE SIMPLE_COMPUTE;

-- ✅ Can create a table
CREATE OR REPLACE TABLE {database_name}.{schema_name}.ENGAGEMENT_LEVELS (
    ENGAGEMENT_ID INT PRIMARY KEY,
    ENGAGEMENT_LEVEL INT
);

-- ✅ Can insert data
INSERT INTO {database_name}.{schema_name}.ENGAGEMENT_LEVELS 
VALUES (1, 1);

-- ✅ Can alter schema in place
ALTER SCHEMA {database_name}.{schema_name} SET COMMENT = 'SANDBOX';

-- ✅ Can drop table
DROP TABLE IF EXISTS {database_name}.{schema_name}.ENGAGEMENT_LEVELS;
            """, language="sql")

else:
    st.info("👆 Please enter both Database Name and Schema Name to see the visualization and generated SQL.")

# Footer
st.markdown("---")
st.markdown("*This visualization covers the complete RBAC setup including database roles, schema access roles, and account-level functional roles*")

