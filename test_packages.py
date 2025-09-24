#!/usr/bin/env python3
"""
Package availability test for Snowflake Cortex AI Slide Builder
Run this script in your Snowflake Streamlit environment to test package availability
"""

import sys
import importlib

def test_package(package_name, required=True):
    """Test if a package is available"""
    try:
        importlib.import_module(package_name)
        status = "✅ Available"
        print(f"{package_name:25} : {status}")
        return True
    except ImportError as e:
        status = "❌ Missing" if required else "⚠️  Optional (Missing)"
        print(f"{package_name:25} : {status}")
        if required:
            print(f"    Error: {e}")
        return False

def main():
    """Test all packages needed for the application"""
    print("🧪 Testing Package Availability for Snowflake Cortex AI Slide Builder")
    print("=" * 70)
    print()
    
    # Required packages
    print("📦 Required Packages:")
    required_packages = [
        "streamlit",
        "pandas", 
        "json",
        "time",
        "typing",
        "logging"
    ]
    
    required_available = 0
    for package in required_packages:
        if test_package(package, required=True):
            required_available += 1
    
    print()
    
    # Visualization packages (with fallbacks)
    print("📊 Visualization Packages (with fallbacks):")
    viz_packages = [
        "plotly.express",
        "plotly.graph_objects", 
        "altair"
    ]
    
    viz_available = 0
    for package in viz_packages:
        if test_package(package, required=False):
            viz_available += 1
    
    print()
    
    # Snowflake packages
    print("❄️  Snowflake Packages:")
    snowflake_packages = [
        "snowflake.connector",
        "snowflake.snowpark",
        "snowflake.snowpark.context"
    ]
    
    snowflake_available = 0
    for package in snowflake_packages:
        if test_package(package, required=False):
            snowflake_available += 1
    
    print()
    
    # Optional packages
    print("🔧 Optional Packages:")
    optional_packages = [
        "requests",
        "numpy",
        "PIL",
        "pptx",
        "reportlab"
    ]
    
    optional_available = 0
    for package in optional_packages:
        if test_package(package, required=False):
            optional_available += 1
    
    print()
    print("=" * 70)
    print("📊 Summary:")
    print(f"Required packages:     {required_available}/{len(required_packages)} available")
    print(f"Visualization packages: {viz_available}/{len(viz_packages)} available")
    print(f"Snowflake packages:    {snowflake_available}/{len(snowflake_packages)} available")
    print(f"Optional packages:     {optional_available}/{len(optional_packages)} available")
    
    print()
    
    if required_available == len(required_packages):
        print("✅ All required packages are available!")
    else:
        print("❌ Some required packages are missing")
        
    if viz_available > 0:
        print("✅ Visualization packages available")
        if viz_available >= 2:
            print("   • Plotly available for rich visualizations")
        elif "altair" in [pkg.split(".")[-1] for pkg in viz_packages]:
            print("   • Altair available as fallback")
        else:
            print("   • Using Streamlit built-in charts")
    else:
        print("⚠️  No visualization packages available, will use data tables")
    
    if snowflake_available > 0:
        print("✅ Snowflake packages available - can use real Cortex integration")
    else:
        print("⚠️  Snowflake packages not available - will use demo mode")
    
    print()
    print("🚀 Application Status:")
    if required_available == len(required_packages):
        print("   Ready to run! The application will work with available packages.")
        print("   Automatic fallbacks ensure functionality regardless of missing optional packages.")
    else:
        print("   ❌ Cannot run - missing required packages")
        print("   Please ensure all required packages are installed.")
    
    print()
    print("📚 For package installation help, see:")
    print("   • requirements.txt - pip package list")
    print("   • environment.yml - conda environment file")
    print("   • docs/deployment_guide.md - deployment instructions")

if __name__ == "__main__":
    main()
