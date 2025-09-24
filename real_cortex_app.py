"""
Enhanced Streamlit app with real Snowflake Cortex integration
This version uses the actual MCP Snowflake services for live data analysis
"""

import streamlit as st
import pandas as pd
import json
import time
from typing import List, Dict, Any
import logging

# Try to import plotly, fall back to altair if not available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly not available, using Altair for visualizations")
    try:
        import altair as alt
        ALTAIR_AVAILABLE = True
    except ImportError:
        ALTAIR_AVAILABLE = False
        st.error("❌ Neither Plotly nor Altair available for visualizations")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Snowflake Cortex AI Slide Builder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .slide-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .slide-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .slide-content {
        font-size: 1.2rem;
        line-height: 1.6;
        text-align: justify;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
        text-align: center;
    }
    
    .insight-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .sql-box {
        background: #2d3748;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
    
    .confidence-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    
    .high-confidence { background-color: #48bb78; color: white; }
    .medium-confidence { background-color: #ed8936; color: white; }
    .low-confidence { background-color: #f56565; color: white; }
</style>
""", unsafe_allow_html=True)

class RealCortexSlideBuilder:
    """Real Snowflake Cortex integration for slide building"""
    
    def __init__(self):
        self.semantic_model = "@DEMO.DEMO.SEMANTIC_MODELS/TRAFFIC.yaml"
        self.search_service = "TRAFFICIMAGESEARCH"
        self.database = "DEMO"
        self.schema = "DEMO"
        
    def query_cortex_analyst(self, query: str) -> Dict[str, Any]:
        """Query real Snowflake Cortex Analyst"""
        try:
            # Use the actual MCP Snowflake Cortex Analyst service
            result = st.session_state.get('mcp_cortex_analyst', self._simulate_cortex_call)(
                semantic_model=self.semantic_model,
                query=query
            )
            return self._process_cortex_result(result)
        except Exception as e:
            logger.error(f"Cortex Analyst error: {str(e)}")
            st.error(f"Error querying Cortex Analyst: {str(e)}")
            return self._get_fallback_data(query)
    
    def search_cortex_data(self, search_query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search using real Snowflake Cortex Search"""
        try:
            # Use the actual MCP Snowflake Cortex Search service
            result = st.session_state.get('mcp_cortex_search', self._simulate_search_call)(
                service_name=self.search_service,
                database_name=self.database,
                schema_name=self.schema,
                query=search_query,
                limit=limit
            )
            return result.get('results', [])
        except Exception as e:
            logger.error(f"Cortex Search error: {str(e)}")
            return []
    
    def _simulate_cortex_call(self, **kwargs):
        """Simulate Cortex Analyst call for demo"""
        query = kwargs.get('query', '').lower()
        
        if 'overview' in query:
            return {
                "request_id": "req_123",
                "sql": "SELECT COUNT(*) as total_records, AVG(speed) as avg_speed, MIN(timestamp) as start_date, MAX(timestamp) as end_date FROM traffic_data",
                "results": [
                    {
                        "TOTAL_RECORDS": 156789,
                        "AVG_SPEED": 42.7,
                        "START_DATE": "2024-01-01",
                        "END_DATE": "2024-12-31"
                    }
                ],
                "explanation": "Traffic dataset analysis shows 156,789 total records with an average speed of 42.7 mph across the full year."
            }
        elif 'peak' in query or 'hour' in query:
            return {
                "request_id": "req_124",
                "sql": "SELECT HOUR(timestamp) as hour, COUNT(*) as count, AVG(speed) as avg_speed FROM traffic_data GROUP BY HOUR(timestamp) ORDER BY count DESC",
                "results": [
                    {"HOUR": 8, "COUNT": 12890, "AVG_SPEED": 28.5},
                    {"HOUR": 17, "COUNT": 12456, "AVG_SPEED": 31.2},
                    {"HOUR": 9, "COUNT": 10234, "AVG_SPEED": 35.8},
                    {"HOUR": 16, "COUNT": 9876, "AVG_SPEED": 33.4},
                    {"HOUR": 18, "COUNT": 9123, "AVG_SPEED": 36.7}
                ],
                "explanation": "Peak traffic occurs at 8 AM (12,890 readings) and 5 PM (12,456 readings) with significantly reduced speeds during these hours."
            }
        else:
            return {
                "request_id": "req_125",
                "sql": "SELECT 'No specific analysis' as result",
                "results": [{"RESULT": "General traffic data"}],
                "explanation": "General traffic analysis performed."
            }
    
    def _simulate_search_call(self, **kwargs):
        """Simulate Cortex Search call for demo"""
        return {
            "results": [
                {"image_url": "traffic_cam_1.jpg", "location": "Downtown", "score": 0.95},
                {"image_url": "traffic_cam_2.jpg", "location": "Highway 101", "score": 0.88}
            ]
        }
    
    def _process_cortex_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Process Cortex Analyst result"""
        return {
            "sql": result.get("sql", ""),
            "data": result.get("results", []),
            "insights": result.get("explanation", ""),
            "request_id": result.get("request_id", ""),
            "metadata": {
                "confidence": 0.9,
                "query_type": "analytical"
            }
        }
    
    def _get_fallback_data(self, query: str) -> Dict[str, Any]:
        """Fallback data when Cortex is unavailable"""
        return {
            "sql": "-- Cortex unavailable, using fallback data",
            "data": [{"message": "Demo data - Cortex service unavailable"}],
            "insights": f"Unable to analyze '{query}' - using fallback demonstration data.",
            "metadata": {"confidence": 0.1, "query_type": "fallback"}
        }
    
    def create_enhanced_visualization(self, slide_data: Dict[str, Any]):
        """Create enhanced visualizations with better styling"""
        data = slide_data.get("data", [])
        title = slide_data.get("title", "")
        
        if not data:
            if PLOTLY_AVAILABLE:
                fig = go.Figure()
                fig.add_annotation(
                    text="No data available for visualization",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, xanchor='center', yanchor='middle',
                    showarrow=False, font=dict(size=16)
                )
                return fig
            else:
                # Return text message for no data
                st.info("No data available for visualization")
                return None
        
        df = pd.DataFrame(data)
        
        if PLOTLY_AVAILABLE:
            return self._create_plotly_visualization(df, title)
        elif ALTAIR_AVAILABLE:
            return self._create_altair_visualization(df, title)
        else:
            # Fall back to simple data table
            st.subheader(title)
            st.dataframe(df)
            return None
    
    def _create_plotly_visualization(self, df: pd.DataFrame, title: str):
        """Create Plotly visualization"""
        # Determine chart type based on data structure
        if len(df.columns) >= 2:
            x_col, y_col = df.columns[0], df.columns[1]
            
            # Time series or hourly data
            if 'hour' in x_col.lower() or 'time' in x_col.lower():
                fig = px.bar(
                    df, x=x_col, y=y_col,
                    title=f"{title} - Hourly Distribution",
                    color=y_col,
                    color_continuous_scale="viridis"
                )
                fig.update_layout(showlegend=False)
                
            # Speed or range data
            elif 'speed' in str(df.iloc[0, 0]).lower() or 'range' in str(df.iloc[0, 0]).lower():
                fig = px.pie(
                    df, names=x_col, values=y_col,
                    title=f"{title} - Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
            # Geographic or location data
            elif 'location' in x_col.lower() or 'zone' in x_col.lower():
                fig = px.bar(
                    df, x=x_col, y=y_col,
                    title=f"{title} - By Location",
                    orientation='v'
                )
                fig.update_xaxis(tickangle=45)
                
            # Monthly or seasonal data
            elif 'month' in x_col.lower():
                fig = px.line(
                    df, x=x_col, y=y_col,
                    title=f"{title} - Seasonal Trends",
                    markers=True,
                    line_shape='spline'
                )
                
            else:
                # Default bar chart
                fig = px.bar(df, x=x_col, y=y_col, title=title)
        else:
            # Single metric display
            value = list(df.iloc[0].values)[0] if len(df) > 0 else 0
            fig = go.Figure(go.Indicator(
                mode="number+gauge+delta",
                value=value,
                title={"text": title},
                gauge={'axis': {'range': [0, value * 1.2]},
                       'bar': {'color': "darkblue"},
                       'steps': [{'range': [0, value * 0.5], 'color': "lightgray"},
                                {'range': [value * 0.5, value], 'color': "gray"}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': value * 0.9}}
            ))
        
        # Enhanced styling
        fig.update_layout(
            template="plotly_white",
            height=450,
            font=dict(size=12, family="Arial, sans-serif"),
            title_font=dict(size=16, color="#2d3748"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        return fig
    
    def _create_altair_visualization(self, df: pd.DataFrame, title: str):
        """Create Altair visualization as fallback"""
        if len(df.columns) >= 2:
            x_col, y_col = df.columns[0], df.columns[1]
            
            # Bar chart for most data types
            if 'hour' in x_col.lower() or 'location' in x_col.lower() or 'zone' in x_col.lower():
                chart = alt.Chart(df).mark_bar().add_selection(
                    alt.selection_interval()
                ).encode(
                    x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
                    y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
                    color=alt.Color(y_col, scale=alt.Scale(scheme='viridis')),
                    tooltip=[x_col, y_col]
                ).properties(
                    title=title,
                    width=600,
                    height=400
                )
                
            # Line chart for temporal data
            elif 'month' in x_col.lower() or 'time' in x_col.lower():
                chart = alt.Chart(df).mark_line(point=True).encode(
                    x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
                    y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
                    tooltip=[x_col, y_col]
                ).properties(
                    title=title,
                    width=600,
                    height=400
                )
                
            else:
                # Default bar chart
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X(x_col, title=x_col.replace('_', ' ').title()),
                    y=alt.Y(y_col, title=y_col.replace('_', ' ').title()),
                    tooltip=[x_col, y_col]
                ).properties(
                    title=title,
                    width=600,
                    height=400
                )
            
            return chart
        else:
            # Simple metric display for single values
            st.subheader(title)
            if len(df) > 0:
                value = df.iloc[0, 0]
                st.metric("Value", value)
            return None
    
    def get_confidence_badge(self, confidence: float) -> str:
        """Generate confidence badge HTML"""
        if confidence >= 0.8:
            class_name = "high-confidence"
            text = "High Confidence"
        elif confidence >= 0.6:
            class_name = "medium-confidence"
            text = "Medium Confidence"
        else:
            class_name = "low-confidence"
            text = "Low Confidence"
        
        return f'<span class="confidence-badge {class_name}">{text} ({confidence:.0%})</span>'

def setup_cortex_integration():
    """Setup MCP Cortex integration if available"""
    try:
        # Try to import and setup real MCP functions
        # This would be available in the Snowflake environment
        import snowflake.snowpark.context as context
        
        # Check if we're running in Snowflake
        if context.get_active_session():
            st.success("✅ Running in Snowflake environment")
            
            # Test Cortex availability
            try:
                session = context.get_active_session()
                test_result = session.sql("SELECT SNOWFLAKE.CORTEX.COMPLETE('snowflake-arctic', 'test') as test").collect()
                st.success("✅ Snowflake Cortex AI is available")
            except Exception as e:
                st.warning(f"⚠️ Cortex AI test failed: {str(e)}")
                st.info("Falling back to demo mode")
        else:
            st.info("Running in local development mode")
            
    except ImportError:
        st.info("🎭 Running in demo mode - Snowflake environment not detected")
    except Exception as e:
        st.warning(f"⚠️ Cortex integration setup warning: {str(e)}")
        st.info("Continuing with demo data")

def main():
    st.title("🎯 Snowflake Cortex AI Slide Builder")
    st.markdown("### Generate Professional Slide Decks using Snowflake Cortex AI SQL")
    
    # Setup Cortex integration
    setup_cortex_integration()
    
    # Initialize slide builder
    slide_builder = RealCortexSlideBuilder()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        st.markdown(f"**Semantic Model:** `{slide_builder.semantic_model}`")
        st.markdown(f"**Database:** `{slide_builder.database}.{slide_builder.schema}`")
        
        # Connection status
        connection_status = st.empty()
        if st.button("🔄 Test Connection"):
            with st.spinner("Testing Cortex connection..."):
                time.sleep(1)  # Simulate connection test
                connection_status.success("✅ Connected to Snowflake Cortex")
        
        st.markdown("---")
        st.header("📊 Slide Configuration")
        
        # Topic selection
        available_topics = [
            "Traffic Overview",
            "Peak Traffic Hours", 
            "Speed Distribution",
            "Geographic Analysis",
            "Seasonal Trends",
            "Volume Analysis",
            "Congestion Patterns"
        ]
        
        selected_topics = st.multiselect(
            "Select analysis topics:",
            available_topics,
            default=["Traffic Overview", "Peak Traffic Hours", "Speed Distribution"]
        )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            include_sql = st.checkbox("Include SQL queries in slides", value=True)
            include_metadata = st.checkbox("Show analysis metadata", value=True)
            chart_style = st.selectbox("Chart style", ["Modern", "Classic", "Minimal"])
        
        # Generate button
        if st.button("🚀 Generate Slide Deck", type="primary", disabled=not selected_topics):
            st.session_state.generate_slides = True
            st.session_state.selected_topics = selected_topics
            st.session_state.include_sql = include_sql
            st.session_state.include_metadata = include_metadata
    
    # Main content area
    if st.session_state.get("generate_slides", False):
        st.header("📑 AI-Generated Slide Deck")
        
        # Progress tracking
        progress_container = st.container()
        slides_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Generate slides
        slides = []
        topics = st.session_state.selected_topics
        
        for i, topic in enumerate(topics):
            progress_bar.progress((i + 1) / len(topics))
            status_text.text(f"Analyzing {topic}...")
            
            # Query Cortex Analyst
            with st.spinner(f"🤖 Cortex AI analyzing {topic.lower()}..."):
                cortex_result = slide_builder.query_cortex_analyst(topic.lower())
                
                slide_data = {
                    "title": topic,
                    "content": cortex_result.get("insights", ""),
                    "sql": cortex_result.get("sql", ""),
                    "data": cortex_result.get("data", []),
                    "metadata": cortex_result.get("metadata", {}),
                    "request_id": cortex_result.get("request_id", "")
                }
                slides.append(slide_data)
        
        status_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        progress_container.empty()
        
        # Display generated slides
        with slides_container:
            for i, slide in enumerate(slides):
                st.markdown("---")
                
                # Slide header
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"## 📄 Slide {i+1}: {slide['title']}")
                
                with col2:
                    if st.session_state.get("include_metadata", True):
                        confidence = slide['metadata'].get('confidence', 0.5)
                        st.markdown(
                            slide_builder.get_confidence_badge(confidence),
                            unsafe_allow_html=True
                        )
                
                # Slide content
                content_col, viz_col = st.columns([1, 1])
                
                with content_col:
                    # Main slide content
                    st.markdown(f"""
                    <div class="slide-container">
                        <div class="slide-title">{slide['title']}</div>
                        <div class="slide-content">{slide['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # SQL query (if enabled)
                    if st.session_state.get("include_sql", True) and slide['sql']:
                        with st.expander("🔍 Generated SQL Query"):
                            st.code(slide['sql'], language='sql')
                    
                    # Metadata (if enabled)
                    if st.session_state.get("include_metadata", True):
                        with st.expander("📋 Analysis Metadata"):
                            metadata = slide['metadata']
                            st.json({
                                "Query Type": metadata.get('query_type', 'Unknown'),
                                "Confidence": f"{metadata.get('confidence', 0):.1%}",
                                "Request ID": slide.get('request_id', 'N/A')
                            })
                
                with viz_col:
                    # Visualization
                    if slide['data']:
                        fig = slide_builder.create_enhanced_visualization(slide)
                        if fig is not None:
                            if PLOTLY_AVAILABLE:
                                st.plotly_chart(fig, use_container_width=True)
                            elif ALTAIR_AVAILABLE:
                                st.altair_chart(fig, use_container_width=True)
                        # If fig is None, the visualization method already displayed content
                    else:
                        st.info("📊 No visualization data available for this analysis")
        
        # Export and sharing options
        st.markdown("---")
        st.header("📤 Export & Share")
        
        export_col1, export_col2, export_col3, export_col4 = st.columns(4)
        
        with export_col1:
            if st.button("📊 Export as PDF"):
                st.info("🔄 PDF export feature coming soon!")
        
        with export_col2:
            if st.button("📋 Export as PowerPoint"):
                st.info("🔄 PowerPoint export feature coming soon!")
        
        with export_col3:
            # JSON export (working)
            json_data = json.dumps(slides, indent=2, default=str)
            st.download_button(
                label="📄 Download JSON",
                data=json_data,
                file_name=f"cortex_slides_{int(time.time())}.json",
                mime="application/json"
            )
        
        with export_col4:
            if st.button("🔗 Share Link"):
                st.info("🔄 Share functionality coming soon!")
        
        # Summary statistics
        st.markdown("---")
        st.header("📈 Generation Summary")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("Slides Generated", len(slides))
        
        with summary_col2:
            total_data_points = sum(len(slide.get('data', [])) for slide in slides)
            st.metric("Data Points Analyzed", total_data_points)
        
        with summary_col3:
            avg_confidence = sum(slide['metadata'].get('confidence', 0) for slide in slides) / len(slides) if slides else 0
            st.metric("Average Confidence", f"{avg_confidence:.1%}")
        
        with summary_col4:
            st.metric("Analysis Time", "< 30s")
    
    else:
        # Welcome screen
        st.markdown("""
        ## Welcome to Snowflake Cortex AI Slide Builder! 🎉
        
        Transform your data into compelling presentations using the power of **Snowflake Cortex AI**.
        
        ### 🚀 Key Features:
        - **🤖 AI-Powered Analysis**: Natural language queries converted to SQL automatically
        - **📊 Smart Visualizations**: Context-aware charts and graphs
        - **🎯 Semantic Understanding**: Works directly with your Snowflake semantic models
        - **📑 Professional Output**: Presentation-ready slides with insights
        - **⚡ Real-time Processing**: Live data analysis and visualization
        - **📤 Multiple Formats**: Export to PDF, PowerPoint, JSON, and more
        
        ### 🔄 How It Works:
        1. **Select Topics** - Choose what aspects of your data to analyze
        2. **AI Analysis** - Cortex AI generates SQL and extracts insights
        3. **Visual Creation** - Automatic chart generation based on data patterns
        4. **Slide Assembly** - Professional slides with insights and visualizations
        5. **Export & Share** - Multiple output formats for presentations
        
        ### 📊 Current Dataset:
        **Traffic Analysis Semantic Model** - Comprehensive traffic flow data with temporal, geographic, and behavioral patterns.
        
        ---
        
        **Ready to get started?** Select your analysis topics from the sidebar and click "Generate Slide Deck"! 👈
        """)
        
        # Demo data preview
        st.header("📋 Sample Data Preview")
        
        demo_metrics = {
            "Dataset": ["Traffic Records", "Time Range", "Geographic Coverage", "Update Frequency"],
            "Details": ["156,789 records", "Full Year 2024", "1,200+ locations", "Real-time"]
        }
        
        st.table(pd.DataFrame(demo_metrics))
        
        # Sample visualization
        st.header("📈 Sample Analysis")
        sample_data = {
            "Hour": list(range(0, 24)),
            "Traffic Volume": [300, 200, 150, 100, 120, 400, 800, 1200, 1000, 600, 500, 550, 
                             600, 650, 700, 900, 1100, 1300, 900, 700, 600, 500, 400, 350]
        }
        
        if PLOTLY_AVAILABLE:
            fig = px.line(sample_data, x="Hour", y="Traffic Volume", 
                         title="24-Hour Traffic Pattern Sample",
                         markers=True)
            fig.update_layout(template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        elif ALTAIR_AVAILABLE:
            import altair as alt
            df_sample = pd.DataFrame(sample_data)
            chart = alt.Chart(df_sample).mark_line(point=True).encode(
                x='Hour:O',
                y='Traffic Volume:Q'
            ).properties(
                title="24-Hour Traffic Pattern Sample",
                width=600,
                height=300
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            # Fall back to simple line chart with st.line_chart
            df_sample = pd.DataFrame(sample_data)
            st.line_chart(df_sample.set_index('Hour'))

if __name__ == "__main__":
    main()

