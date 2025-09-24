# Deployment Troubleshooting Guide

## Quick Fix for Environment.yml Issues

If you're seeing the error: `[092812] Unsupported Anaconda feature or malformed environment.yml file`, here's how to fix it:

### ✅ Immediate Solution (Recommended)

**Use the simplified deployment script:**

```sql
-- Run this instead of the regular deployment
@deploy_simple.sql
```

This script:
- ✅ Deploys without environment.yml dependencies
- ✅ Relies on Snowflake's built-in packages
- ✅ Uses the application's automatic fallback system
- ✅ Works immediately without package configuration

### 🔧 Manual Fix

If you've already started deployment:

1. **Remove the problematic file:**
```sql
REMOVE @CORTEX_APPS.SLIDE_BUILDER.SLIDE_BUILDER_STAGE/environment.yml;
```

2. **Upload only essential files:**
```bash
PUT file://real_cortex_app.py @CORTEX_APPS.SLIDE_BUILDER.SLIDE_BUILDER_STAGE/;
PUT file://cortex_integration.py @CORTEX_APPS.SLIDE_BUILDER.SLIDE_BUILDER_STAGE/;
```

3. **Recreate the Streamlit app:**
```sql
DROP STREAMLIT CORTEX_SLIDE_BUILDER;
CREATE STREAMLIT CORTEX_SLIDE_BUILDER
ROOT_LOCATION = '@CORTEX_APPS.SLIDE_BUILDER.SLIDE_BUILDER_STAGE'
MAIN_FILE = 'real_cortex_app.py'
QUERY_WAREHOUSE = 'COMPUTE_WH';
```

### 📊 What This Means

**Good News**: The application is designed to work without external package dependencies!

- **Automatic Fallbacks**: Uses Plotly → Altair → Streamlit built-ins → Data tables
- **Zero Dependencies**: Core functionality works with just Python standard library
- **Smart Detection**: Automatically detects and uses available packages

### 🎯 Application Status

After using the simple deployment:

| Feature | Status | Notes |
|---------|--------|-------|
| Core App | ✅ Works | Full functionality |
| Slide Generation | ✅ Works | AI-powered analysis |
| Visualizations | ✅ Works | Automatic fallbacks |
| Cortex Integration | ✅ Works | With demo fallback |
| Export | ✅ Works | JSON export available |

### 🚀 Testing Your Deployment

After deployment, test that everything works:

1. **Access the app** via Snowsight → Projects → Streamlit
2. **Check package status** - the app will show which visualization library it's using
3. **Generate slides** - select topics and create a slide deck
4. **Verify functionality** - all features should work regardless of available packages

### 📚 Why This Happened

Snowflake Streamlit environments have specific restrictions:
- Limited conda/pip package installation
- Restricted environment.yml format
- Built-in package preference
- Security limitations

**Our Solution**: Build the app to be self-sufficient and use intelligent fallbacks!

### 🛟 Need More Help?

If you continue to have issues:

1. **Check the full deployment guide**: `docs/deployment_guide.md`
2. **Run package tests**: Use `test_packages.py` to check available packages
3. **Use demo mode**: The app works perfectly in demo mode for testing
4. **Contact support**: See troubleshooting section in the deployment guide

---

**Bottom Line**: The application is designed to work regardless of package availability. Use `deploy_simple.sql` for the most reliable deployment experience!
