import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from typing import List, Dict, Any
import base64
from io import BytesIO
import requests
from cortex_integration import SnowflakeCortexIntegration

# Page configuration
st.set_page_config(
    page_title="Snowflake Cortex AI Slide Builder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .slide-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    
    .slide-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .slide-content {
        font-size: 1.2rem;
        line-height: 1.6;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    
    .insight-box {
        background: #f0f2f6;
        padding: 1rem;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

class SnowflakeCortexSlideBuilder:
    def __init__(self):
        self.cortex = SnowflakeCortexIntegration()
        self.slides = []
        
    def query_cortex_analyst(self, query: str) -> Dict[Any, Any]:
        """Query Snowflake Cortex Analyst with natural language"""
        try:
            return self.cortex.query_cortex_analyst(query)
        except Exception as e:
            st.error(f"Error querying Cortex Analyst: {str(e)}")
            return {}
    
    def generate_slide_content(self, topic: str, data: Dict[Any, Any]) -> Dict[str, Any]:
        """Generate slide content based on Cortex analysis"""
        enhanced_insights = self.cortex.generate_slide_insights(data, topic)
        slide = {
            "title": topic.title(),
            "content": enhanced_insights,
            "sql": data.get("sql", ""),
            "data": data.get("data", []),
            "chart_type": self._determine_chart_type(topic),
            "metadata": data.get("metadata", {})
        }
        return slide
    
    def _determine_chart_type(self, topic: str) -> str:
        """Determine appropriate chart type based on topic"""
        if "hour" in topic.lower() or "time" in topic.lower():
            return "bar"
        elif "distribution" in topic.lower() or "range" in topic.lower():
            return "pie"
        elif "trend" in topic.lower():
            return "line"
        else:
            return "metric"
    
    def create_visualization(self, slide_data: Dict[str, Any]) -> go.Figure:
        """Create appropriate visualization based on slide data"""
        data = slide_data["data"]
        chart_type = slide_data["chart_type"]
        
        if not data:
            return go.Figure().add_annotation(text="No data available", showarrow=False)
        
        df = pd.DataFrame(data)
        
        if chart_type == "bar":
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], 
                        title=slide_data["title"],
                        color_discrete_sequence=['#667eea'])
        elif chart_type == "pie":
            fig = px.pie(df, names=df.columns[0], values=df.columns[1],
                        title=slide_data["title"])
        elif chart_type == "line":
            fig = px.line(df, x=df.columns[0], y=df.columns[1],
                         title=slide_data["title"],
                         color_discrete_sequence=['#667eea'])
        else:
            # Metric display
            fig = go.Figure(go.Indicator(
                mode="number",
                value=list(data[0].values())[0] if data else 0,
                title={"text": slide_data["title"]},
                number={'font': {'size': 60}}
            ))
        
        fig.update_layout(
            template="plotly_white",
            height=400,
            font=dict(size=12)
        )
        
        return fig

def main():
    st.title("🎯 Snowflake Cortex AI Slide Builder")
    st.markdown("### Generate insightful slide decks using Snowflake Cortex AI SQL and Semantic Views")
    
    # Initialize the slide builder
    slide_builder = SnowflakeCortexSlideBuilder()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        st.markdown(f"**Semantic Model:** {slide_builder.semantic_model}")
        
        st.header("📊 Slide Topics")
        available_topics = slide_builder.cortex.get_available_topics()
        topics = st.multiselect(
            "Select topics for your slide deck:",
            available_topics,
            default=["Traffic Overview", "Peak Traffic Hours", "Speed Distribution"]
        )
        
        auto_generate = st.checkbox("Auto-generate insights", value=True)
        
        if st.button("🚀 Generate Slide Deck", type="primary"):
            st.session_state.generate_slides = True
            st.session_state.selected_topics = topics
    
    # Main content area
    if st.session_state.get("generate_slides", False):
        st.header("📑 Generated Slide Deck")
        
        # Generate slides for each selected topic
        slides = []
        progress_bar = st.progress(0)
        
        for i, topic in enumerate(st.session_state.selected_topics):
            progress_bar.progress((i + 1) / len(st.session_state.selected_topics))
            
            # Query Cortex Analyst
            with st.spinner(f"Analyzing {topic.lower()}..."):
                cortex_data = slide_builder.query_cortex_analyst(topic.lower())
                slide_data = slide_builder.generate_slide_content(topic, cortex_data)
                slides.append(slide_data)
        
        # Display slides
        for i, slide in enumerate(slides):
            st.markdown("---")
            
            # Slide container
            with st.container():
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="slide-container">
                        <div class="slide-title">{slide['title']}</div>
                        <div class="slide-content">{slide['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show SQL query in expander
                    with st.expander("🔍 View SQL Query"):
                        st.code(slide['sql'], language='sql')
                
                with col2:
                    # Create and display visualization
                    if slide['data']:
                        fig = slide_builder.create_visualization(slide)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No visualization data available")
        
        # Export options
        st.markdown("---")
        st.header("📤 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export as PDF"):
                st.info("PDF export functionality would be implemented here")
        
        with col2:
            if st.button("📋 Export as PowerPoint"):
                st.info("PowerPoint export functionality would be implemented here")
        
        with col3:
            if st.button("📄 Export as JSON"):
                json_data = json.dumps(slides, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="slide_deck.json",
                    mime="application/json"
                )
    
    else:
        # Welcome screen
        st.markdown("""
        ## Welcome to Snowflake Cortex AI Slide Builder! 🎉
        
        This application demonstrates how to use **Snowflake Cortex AI SQL** to automatically generate 
        insightful slide decks from semantic views.
        
        ### Features:
        - 🤖 **AI-Powered Analysis**: Uses Snowflake Cortex to analyze your data
        - 📊 **Automatic Visualizations**: Generates appropriate charts and graphs
        - 🎯 **Semantic Understanding**: Works with Snowflake semantic models
        - 📑 **Professional Slides**: Creates presentation-ready content
        - 📤 **Multiple Export Formats**: PDF, PowerPoint, and JSON support
        
        ### How it works:
        1. Select topics you want to analyze from the sidebar
        2. Click "Generate Slide Deck" to start the analysis
        3. Cortex AI will query your semantic model and generate insights
        4. View your generated slides with visualizations
        5. Export in your preferred format
        
        **Get started by selecting topics in the sidebar!** 👈
        """)
        
        # Sample data preview
        st.header("📋 Sample Traffic Data Overview")
        
        # Create sample data for demonstration
        sample_data = {
            "Metric": ["Total Records", "Average Speed (mph)", "Peak Hour", "Locations Monitored"],
            "Value": ["150,000", "45.2", "8 AM", "1,200"]
        }
        
        df_sample = pd.DataFrame(sample_data)
        st.table(df_sample)

if __name__ == "__main__":
    main()
