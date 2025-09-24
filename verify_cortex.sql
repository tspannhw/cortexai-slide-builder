-- Snowflake Cortex AI Verification Script
-- Run this script to verify Cortex AI availability in your account

-- Step 1: Check current context
SELECT 'Current context check:' as step;
SELECT CURRENT_ACCOUNT() as account, CURRENT_ROLE() as role, CURRENT_USER() as user;

-- Step 2: Check if Cortex parameters are enabled
SELECT 'Checking Cortex parameters...' as step;
SHOW PARAMETERS LIKE '%CORTEX%' IN ACCOUNT;

-- Step 3: Test basic Cortex Complete function
SELECT 'Testing Cortex Complete function...' as step;
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'snowflake-arctic',
    'Hello! Please respond with: "Snowflake Cortex AI is working correctly"'
) as cortex_test_result;

-- Step 4: Check available Cortex functions
SELECT 'Checking available Cortex functions...' as step;
SHOW FUNCTIONS LIKE 'SNOWFLAKE.CORTEX.%';

-- Step 5: Test Cortex Complete with different models (if available)
SELECT 'Testing different Cortex models...' as step;

-- Try different models (comment out if not available)
-- SELECT SNOWFLAKE.CORTEX.COMPLETE('llama2-7b-chat', 'Hello world') as llama_test;
-- SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-7b', 'Hello world') as mistral_test;

-- Step 6: Check permissions on Cortex schema
SELECT 'Checking permissions...' as step;
SHOW GRANTS ON SCHEMA SNOWFLAKE.CORTEX TO ROLE CURRENT_ROLE();

-- Step 7: Verify semantic model access (for the application)
SELECT 'Checking semantic model access...' as step;
-- Check if DEMO database exists
SHOW DATABASES LIKE 'DEMO';

-- Check if semantic models stage exists
-- Note: This may fail if you don't have access - that's okay for testing
SELECT 'Checking semantic models stage...' as step;
-- DESCRIBE STAGE @DEMO.DEMO.SEMANTIC_MODELS;

-- Step 8: Summary
SELECT 'Cortex verification complete!' as summary;
SELECT 'If all tests above passed, Cortex AI is available in your account.' as result;
SELECT 'If any failed, contact your Snowflake administrator to enable Cortex AI.' as next_steps;
