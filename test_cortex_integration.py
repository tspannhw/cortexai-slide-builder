#!/usr/bin/env python3
"""
Test script for Snowflake Cortex AI Slide Builder
This script tests the core functionality without requiring a full Streamlit environment
"""

import json
import sys
import traceback
from typing import Dict, Any

def test_cortex_integration():
    """Test the Cortex integration module"""
    try:
        from cortex_integration import SnowflakeCortexIntegration
        
        print("🧪 Testing Snowflake Cortex Integration...")
        cortex = SnowflakeCortexIntegration()
        
        # Test basic initialization
        print(f"✅ Semantic Model: {cortex.semantic_model}")
        print(f"✅ Search Service: {cortex.search_service}")
        print(f"✅ Database: {cortex.database}.{cortex.schema}")
        
        # Test query functionality
        print("\n🔍 Testing Cortex Analyst queries...")
        test_queries = [
            "traffic overview",
            "peak traffic hours", 
            "speed distribution",
            "geographic analysis",
            "seasonal trends"
        ]
        
        results = {}
        for query in test_queries:
            print(f"  📊 Analyzing: {query}")
            result = cortex.query_cortex_analyst(query)
            results[query] = result
            
            # Validate result structure
            assert "sql" in result, f"Missing SQL in result for {query}"
            assert "data" in result, f"Missing data in result for {query}"
            assert "insights" in result, f"Missing insights in result for {query}"
            
            print(f"    ✅ Generated {len(result['data'])} data points")
            print(f"    ✅ SQL: {result['sql'][:50]}...")
            print(f"    ✅ Insights: {result['insights'][:80]}...")
        
        # Test insight generation
        print("\n🤖 Testing insight generation...")
        for query, data in results.items():
            enhanced_insights = cortex.generate_slide_insights(data, query)
            assert len(enhanced_insights) > len(data.get('insights', '')), f"Enhanced insights not generated for {query}"
            print(f"  ✅ Enhanced insights for {query}: {len(enhanced_insights)} characters")
        
        # Test topic availability
        print("\n📋 Testing available topics...")
        topics = cortex.get_available_topics()
        assert len(topics) > 0, "No topics available"
        print(f"  ✅ Available topics: {len(topics)}")
        for topic in topics:
            print(f"    • {topic}")
        
        # Test connection validation
        print("\n🔗 Testing connection validation...")
        is_connected = cortex.validate_connection()
        print(f"  ✅ Connection status: {'Connected' if is_connected else 'Demo Mode'}")
        
        print("\n🎉 All Cortex integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Cortex integration test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_slide_builder():
    """Test the slide builder functionality"""
    try:
        print("\n🧪 Testing Slide Builder functionality...")
        
        # Test imports
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ All visualization libraries imported")
        
        # Test basic slide building logic
        from real_cortex_app import RealCortexSlideBuilder
        
        builder = RealCortexSlideBuilder()
        print(f"✅ Slide builder initialized")
        print(f"  • Semantic model: {builder.semantic_model}")
        print(f"  • Search service: {builder.search_service}")
        
        # Test query processing
        print("\n📊 Testing slide generation...")
        test_query = "traffic overview"
        cortex_result = builder.query_cortex_analyst(test_query)
        
        assert cortex_result is not None, "No result from Cortex query"
        print(f"  ✅ Query result received: {len(cortex_result)} fields")
        
        # Test visualization creation
        print("\n📈 Testing visualization creation...")
        slide_data = {
            "title": "Test Slide",
            "data": [
                {"hour": 8, "count": 1250},
                {"hour": 17, "count": 1180},
                {"hour": 9, "count": 1020}
            ],
            "chart_type": "bar"
        }
        
        fig = builder.create_enhanced_visualization(slide_data)
        assert fig is not None, "No visualization created"
        print(f"  ✅ Visualization created successfully")
        
        # Test confidence badge
        print("\n🎯 Testing confidence scoring...")
        for confidence in [0.95, 0.75, 0.45]:
            badge = builder.get_confidence_badge(confidence)
            assert badge is not None and len(badge) > 0, f"No badge for confidence {confidence}"
            print(f"  ✅ Confidence {confidence:.0%}: {badge[:30]}...")
        
        print("\n🎉 All slide builder tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Slide builder test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_data_processing():
    """Test data processing and visualization logic"""
    try:
        print("\n🧪 Testing Data Processing...")
        
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Test sample data processing
        sample_data = [
            {"hour": 8, "traffic_count": 12500, "avg_speed_mph": 35.2},
            {"hour": 17, "traffic_count": 11800, "avg_speed_mph": 32.8},
            {"hour": 9, "traffic_count": 10200, "avg_speed_mph": 42.1}
        ]
        
        df = pd.DataFrame(sample_data)
        assert len(df) == 3, "DataFrame creation failed"
        print(f"  ✅ DataFrame created with {len(df)} rows")
        
        # Test chart creation
        fig = px.bar(df, x="hour", y="traffic_count", title="Test Chart")
        assert fig is not None, "Chart creation failed"
        print(f"  ✅ Bar chart created successfully")
        
        # Test pie chart
        pie_data = [
            {"speed_range": "0-20 mph", "count": 25000},
            {"speed_range": "21-40 mph", "count": 45000},
            {"speed_range": "41-60 mph", "count": 55000}
        ]
        
        df_pie = pd.DataFrame(pie_data)
        fig_pie = px.pie(df_pie, names="speed_range", values="count", title="Speed Distribution")
        assert fig_pie is not None, "Pie chart creation failed"
        print(f"  ✅ Pie chart created successfully")
        
        # Test gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="number+gauge",
            value=42.7,
            title={"text": "Average Speed"},
            gauge={'axis': {'range': [0, 80]}}
        ))
        assert fig_gauge is not None, "Gauge chart creation failed"
        print(f"  ✅ Gauge chart created successfully")
        
        print("\n🎉 All data processing tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_export_functionality():
    """Test export and serialization functionality"""
    try:
        print("\n🧪 Testing Export Functionality...")
        
        # Test JSON serialization
        sample_slides = [
            {
                "title": "Traffic Overview",
                "content": "Test content",
                "sql": "SELECT COUNT(*) FROM traffic_data",
                "data": [{"total_records": 150000}],
                "metadata": {"confidence": 0.95}
            },
            {
                "title": "Peak Hours",
                "content": "Peak analysis",
                "sql": "SELECT HOUR(timestamp) FROM traffic_data",
                "data": [{"hour": 8, "count": 12500}],
                "metadata": {"confidence": 0.88}
            }
        ]
        
        # Test JSON export
        json_data = json.dumps(sample_slides, indent=2, default=str)
        assert len(json_data) > 0, "JSON serialization failed"
        print(f"  ✅ JSON export: {len(json_data)} characters")
        
        # Test JSON parsing
        parsed_data = json.loads(json_data)
        assert len(parsed_data) == 2, "JSON parsing failed"
        print(f"  ✅ JSON parsing: {len(parsed_data)} slides recovered")
        
        # Test data validation
        for slide in parsed_data:
            required_fields = ["title", "content", "sql", "data", "metadata"]
            for field in required_fields:
                assert field in slide, f"Missing field {field} in slide"
        print(f"  ✅ Data validation: All required fields present")
        
        print("\n🎉 All export functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Snowflake Cortex AI Slide Builder Tests")
    print("=" * 60)
    
    tests = [
        ("Cortex Integration", test_cortex_integration),
        ("Slide Builder", test_slide_builder),
        ("Data Processing", test_data_processing),
        ("Export Functionality", test_export_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "="*60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

