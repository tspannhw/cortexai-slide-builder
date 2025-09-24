-- Simple Snowflake Cortex AI Slide Builder Deployment Script
-- This script deploys with minimal dependencies and maximum compatibility

-- 1. Create database and schema if they don't exist
CREATE DATABASE IF NOT EXISTS CORTEX_APPS;
CREATE SCHEMA IF NOT EXISTS CORTEX_APPS.SLIDE_BUILDER;

USE DATABASE CORTEX_APPS;
USE SCHEMA SLIDE_BUILDER;

-- 2. Create a stage for the application files
CREATE OR REPLACE STAGE SLIDE_BUILDER_STAGE
DIRECTORY = (ENABLE = TRUE)
COMMENT = 'Stage for Cortex AI Slide Builder application files';

-- 3. Upload ONLY the essential application files
-- Run these commands from your local environment:

/*
PUT file://real_cortex_app.py @SLIDE_BUILDER_STAGE/;
PUT file://cortex_integration.py @SLIDE_BUILDER_STAGE/;
*/

-- 4. Create the Streamlit application (without environment.yml)
CREATE OR REPLACE STREAMLIT CORTEX_SLIDE_BUILDER
ROOT_LOCATION = '@SLIDE_BUILDER_STAGE'
MAIN_FILE = 'real_cortex_app.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse
COMMENT = 'Snowflake Cortex AI Slide Builder - Minimal deployment without environment dependencies';

-- 5. Grant necessary permissions
GRANT USAGE ON DATABASE CORTEX_APPS TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA CORTEX_APPS.SLIDE_BUILDER TO ROLE PUBLIC;
GRANT READ ON STAGE CORTEX_APPS.SLIDE_BUILDER.SLIDE_BUILDER_STAGE TO ROLE PUBLIC;
GRANT USAGE ON STREAMLIT CORTEX_APPS.SLIDE_BUILDER.CORTEX_SLIDE_BUILDER TO ROLE PUBLIC;

-- 6. Test basic functionality (optional)
SELECT 'Testing basic Cortex availability...' as step;
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'snowflake-arctic',
    'Hello! Please respond with: "Cortex AI is working"'
) as cortex_test;

-- 7. Show the application information
SHOW STREAMLITS LIKE 'CORTEX_SLIDE_BUILDER';

-- 8. Deployment completion message
SELECT 'Snowflake Cortex AI Slide Builder deployed successfully!' as deployment_status;
SELECT 'Application relies on built-in Snowflake packages and automatic fallbacks' as package_info;

-- Instructions to access the application
SELECT 'To access your Streamlit application:' as instructions;
SELECT '1. Go to Snowsight (your Snowflake web interface)' as step_1;
SELECT '2. Navigate to Projects > Streamlit' as step_2;
SELECT '3. Find and click on CORTEX_SLIDE_BUILDER application' as step_3;
SELECT 'The app will automatically use available packages with smart fallbacks' as note;
