# Snowflake Streamlit Access Guide

## How to Access Your Deployed Streamlit Application

After successfully deploying the Snowflake Cortex AI Slide Builder to Snowflake, follow these steps to access and use your application.

## Method 1: Through Snowsight Web Interface (Recommended)

### Step 1: Open Snowsight
1. Go to your Snowflake account URL (usually `https://app.snowflake.com/`)
2. Log in with your credentials
3. You should see the Snowsight interface

### Step 2: Navigate to Streamlit Apps
1. In the left sidebar, click on **"Projects"**
2. Select **"Streamlit"** from the dropdown menu
3. You'll see a list of all Streamlit applications in your account

### Step 3: Launch Your Application
1. Look for **"CORTEX_SLIDE_BUILDER"** in the list
2. Click on the application name or the **"Open"** button
3. The application will open in a new tab or window

## Method 2: Using SQL Commands

### Check Deployed Applications
```sql
-- View all Streamlit applications
SHOW STREAMLITS;

-- View specific application
SHOW STREAMLITS LIKE 'CORTEX_SLIDE_BUILDER';
```

### Get Application Details
The `SHOW STREAMLITS` command returns information including:
- **name**: Application name
- **database_name**: Database where it's deployed
- **schema_name**: Schema where it's deployed
- **owner**: Application owner
- **url**: Direct URL to the application (if available)

### Access via URL
If the URL column shows a direct link:
1. Copy the URL from the query results
2. Open it in a new browser tab
3. Log in if prompted

## Method 3: Through Snowflake Classic Console (Legacy)

If you're using the classic Snowflake web interface:

1. Log into your Snowflake account
2. Navigate to **Worksheets**
3. Run: `SHOW STREAMLITS;`
4. Look for the application URL in the results
5. Click or copy the URL to access the application

## Troubleshooting Access Issues

### Issue: Can't Find Streamlit Menu
**Solution**: Ensure you have the necessary permissions and that Streamlit is enabled in your account.

```sql
-- Check your current role
SELECT CURRENT_ROLE();

-- Check permissions
SHOW GRANTS TO ROLE YOUR_ROLE_NAME;
```

### Issue: Application Not Listed
**Solution**: Verify the application was deployed successfully.

```sql
-- Check if application exists
SHOW STREAMLITS IN SCHEMA CORTEX_APPS.SLIDE_BUILDER;

-- Check application status
DESCRIBE STREAMLIT CORTEX_APPS.SLIDE_BUILDER.CORTEX_SLIDE_BUILDER;
```

### Issue: Permission Denied
**Solution**: Ensure you have the correct role and permissions.

```sql
-- Switch to the correct role
USE ROLE CORTEX_SLIDE_BUILDER_ROLE;

-- Or grant yourself access
GRANT USAGE ON STREAMLIT CORTEX_APPS.SLIDE_BUILDER.CORTEX_SLIDE_BUILDER TO ROLE YOUR_ROLE;
```

### Issue: Application Won't Load
**Solutions**:
1. **Check browser compatibility**: Use Chrome, Firefox, or Safari
2. **Clear browser cache**: Refresh the page or clear cache
3. **Check network**: Ensure you have a stable internet connection
4. **Verify deployment**: Run the deployment verification commands

```sql
-- Verify files are uploaded
LIST @CORTEX_APPS.SLIDE_BUILDER.SLIDE_BUILDER_STAGE;

-- Check application configuration
SHOW STREAMLITS LIKE 'CORTEX_SLIDE_BUILDER';
```

## Application Usage

Once you successfully access the application:

1. **Welcome Screen**: You'll see the Snowflake Cortex AI Slide Builder interface
2. **Sidebar Configuration**: Use the left sidebar to select analysis topics
3. **Generate Slides**: Click "Generate Slide Deck" to create your presentation
4. **View Results**: Review the generated slides with visualizations
5. **Export**: Download your results in JSON format

## Getting Help

### Check Application Logs
If the application has issues, you can check logs through:
1. The Streamlit interface (if it loads partially)
2. Snowflake query history for any SQL errors
3. Browser developer console for client-side errors

### Contact Support
- **Internal**: Contact your Snowflake administrator
- **Snowflake Support**: Create a support ticket if needed
- **Documentation**: Refer to the complete [User Guide](docs/user_guide.md)

## Quick Reference Commands

```sql
-- Essential commands for managing your Streamlit app
SHOW STREAMLITS;                           -- List all apps
SHOW STREAMLITS LIKE 'CORTEX_SLIDE_BUILDER';  -- Show specific app
DESC STREAMLIT CORTEX_APPS.SLIDE_BUILDER.CORTEX_SLIDE_BUILDER;  -- App details
SELECT CURRENT_ROLE();                     -- Check current role
SHOW GRANTS TO ROLE CORTEX_SLIDE_BUILDER_ROLE;  -- Check permissions
```

---

**Need more help?** See the complete [Deployment Guide](docs/deployment_guide.md) for detailed troubleshooting and configuration options.
