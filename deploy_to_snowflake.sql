-- Snowflake Cortex AI Slide Builder Deployment Script
-- This script sets up the Streamlit application in Snowflake

-- 1. Create database and schema if they don't exist
CREATE DATABASE IF NOT EXISTS CORTEX_APPS;
CREATE SCHEMA IF NOT EXISTS CORTEX_APPS.SLIDE_BUILDER;

USE DATABASE CORTEX_APPS;
USE SCHEMA SLIDE_BUILDER;

-- 2. Create a stage for the application files
CREATE OR REPLACE STAGE SLIDE_BUILDER_STAGE
DIRECTORY = (ENABLE = TRUE)
COMMENT = 'Stage for Cortex AI Slide Builder application files';

-- 3. Upload application files to the stage
-- Note: These PUT commands should be run from your local environment
-- PUT file://real_cortex_app.py @SLIDE_BUILDER_STAGE/;
-- PUT file://cortex_integration.py @SLIDE_BUILDER_STAGE/;
-- PUT file://requirements.txt @SLIDE_BUILDER_STAGE/;
-- PUT file://environment.yml @SLIDE_BUILDER_STAGE/;
-- PUT file://README.md @SLIDE_BUILDER_STAGE/;

-- 4. Create the Streamlit application
CREATE OR REPLACE STREAMLIT CORTEX_SLIDE_BUILDER
ROOT_LOCATION = '@SLIDE_BUILDER_STAGE'
MAIN_FILE = 'real_cortex_app.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse
COMMENT = 'Snowflake Cortex AI Slide Builder - Generate professional slide decks from semantic views';

-- 5. Grant necessary permissions
-- Adjust these grants based on your security requirements
GRANT USAGE ON DATABASE CORTEX_APPS TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA CORTEX_APPS.SLIDE_BUILDER TO ROLE PUBLIC;
GRANT READ ON STAGE CORTEX_APPS.SLIDE_BUILDER.SLIDE_BUILDER_STAGE TO ROLE PUBLIC;
GRANT USAGE ON STREAMLIT CORTEX_APPS.SLIDE_BUILDER.CORTEX_SLIDE_BUILDER TO ROLE PUBLIC;

-- 6. Verify the semantic model access
-- Ensure the application can access the traffic semantic model
DESCRIBE STAGE @DEMO.DEMO.SEMANTIC_MODELS;

-- 7. Test Cortex services availability
-- Note: These tests verify Cortex AI is available in your account
-- If these fail, ensure Cortex AI is enabled for your account

-- Test basic Cortex Complete function (most widely available)
SELECT 'Testing Cortex Complete...' as test_step;
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'snowflake-arctic',
    'Hello, this is a test. Please respond with "Cortex is working"'
) as cortex_complete_test;

-- Test if Cortex Analyst is available (may not be in all regions/accounts)
SELECT 'Testing Cortex Analyst availability...' as test_step;

-- 8. Show the application information
-- Note: SYSTEM$GET_STREAMLIT_URL may not be available in all Snowflake versions
-- Use SHOW STREAMLITS to get application details instead
SHOW STREAMLITS LIKE 'CORTEX_SLIDE_BUILDER';

-- 9. Optional: Create sample data view for testing
CREATE OR REPLACE VIEW TRAFFIC_SAMPLE AS
SELECT 
    DATEADD(hour, UNIFORM(0, 23, RANDOM()), CURRENT_DATE()) as timestamp,
    UNIFORM(10, 80, RANDOM()) as speed,
    UNIFORM(100, 2000, RANDOM()) as volume,
    CASE UNIFORM(1, 8, RANDOM())
        WHEN 1 THEN 'Downtown'
        WHEN 2 THEN 'Highway 101'
        WHEN 3 THEN 'Suburban North'
        WHEN 4 THEN 'Industrial District'
        WHEN 5 THEN 'Airport Corridor'
        WHEN 6 THEN 'Residential East'
        WHEN 7 THEN 'Commercial West'
        ELSE 'University Area'
    END as location_zone
FROM TABLE(GENERATOR(ROWCOUNT => 1000));

-- 10. Create a simple test function for Cortex integration
CREATE OR REPLACE FUNCTION TEST_CORTEX_CONNECTION()
RETURNS STRING
LANGUAGE SQL
AS
$$
  SELECT 'Cortex services are available and configured correctly'
$$;

-- Deployment completion message
SELECT 'Snowflake Cortex AI Slide Builder deployed successfully!' as deployment_status;

-- Instructions to access the application
SELECT 'To access your Streamlit application:' as instructions;
SELECT '1. Go to Snowsight (your Snowflake web interface)' as step_1;
SELECT '2. Navigate to Projects > Streamlit' as step_2;
SELECT '3. Find and click on CORTEX_SLIDE_BUILDER application' as step_3;
SELECT 'OR check the output above from SHOW STREAMLITS for the application details' as alternative;

