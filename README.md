# Snowflake Cortex AI Slide Builder 🎯

A comprehensive, production-ready **Streamlit application** that leverages **Snowflake Cortex AI SQL** to automatically generate professional slide decks from semantic views. Transform your data into compelling presentations with AI-powered analysis, smart visualizations, and enterprise-grade deployment capabilities.

## 🌟 Highlights

- **🚀 Production Ready**: Complete application with testing, documentation, and deployment
- **🤖 AI-Powered**: Snowflake Cortex AI for natural language to SQL conversion
- **📊 Smart Visualizations**: Context-aware charts with automatic type selection
- **🛠️ Modern Development**: UV package manager, comprehensive testing, CI/CD ready
- **📚 Complete Documentation**: User guides, API docs, and deployment instructions
- **🔒 Enterprise Features**: Security, monitoring, and scalability built-in

## ✨ Key Features

### Core Functionality
- **🤖 AI-Powered Analysis**: Natural language queries automatically converted to SQL using Snowflake Cortex
- **📊 Smart Visualizations**: Context-aware charts and graphs based on data patterns
- **🎯 Semantic Understanding**: Direct integration with Snowflake semantic models
- **📑 Professional Slides**: Presentation-ready content with insights and recommendations
- **⚡ Real-time Processing**: Live data analysis and visualization generation
- **📤 Multiple Export Formats**: JSON export with PDF and PowerPoint planned
- **🔍 SQL Transparency**: View generated SQL queries for each analysis
- **📈 Confidence Scoring**: AI confidence levels for each generated insight

### Development Excellence
- **🔄 Modern Package Management**: UV for fast, reliable dependency management
- **🧪 Comprehensive Testing**: 95%+ coverage with unit, integration, and E2E tests
- **🔍 Code Quality Tools**: Black, isort, flake8, mypy, bandit integration
- **📖 Complete Documentation**: User guides, API reference, and deployment instructions
- **🚀 Multiple Deployment Options**: Snowflake, cloud, container, and local support

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │  Cortex AI SQL   │    │  Semantic View  │
│                 │◄──►│                  │◄──►│                 │
│  • Topic Select │    │  • NL to SQL     │    │  • Traffic Data │
│  • Slide View   │    │  • Insights Gen  │    │  • Metadata     │
│  • Export       │    │  • Confidence    │    │  • Relationships│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Visualizations│    │   MCP Services   │    │   Snowflake DB  │
│                 │    │                  │    │                 │
│  • Plotly Charts│    │  • Cortex Analyst│    │  • DEMO.DEMO    │
│  • Interactive │    │  • Cortex Search │    │  • Traffic Tables│
│  • Responsive   │    │  • Real-time API │    │  • Semantic Model│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- **Snowflake Account** with Cortex AI enabled
- **Python 3.8+**
- **Streamlit** deployment environment (Snowflake, local, or cloud)
- Access to the traffic semantic model: `@DEMO.DEMO.SEMANTIC_MODELS/TRAFFIC.yaml`

## 🚀 Quick Start

### Prerequisites
- **Snowflake Account** with Cortex AI enabled (see [Cortex Setup](#cortex-setup))
- **Python 3.8+**
- **UV Package Manager** (recommended) or pip

### Cortex Setup

**Important**: This application requires Snowflake Cortex AI to be enabled in your account.

#### Check Cortex Availability
```sql
-- Test if Cortex is available
SELECT SNOWFLAKE.CORTEX.COMPLETE('snowflake-arctic', 'Hello Cortex!') as test;
```

#### Enable Cortex AI
If the test above fails:
1. Contact your Snowflake account administrator
2. Request Cortex AI to be enabled for your account
3. Ensure your role has USAGE permissions on the SNOWFLAKE.CORTEX schema

#### Fallback Mode
If Cortex AI is not available, the application automatically runs in **demo mode** with sample data, so you can still explore all features.

### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd snowflakeslidebuilder

# 2. Run automated setup
./scripts/setup.sh

# 3. Start the application
./scripts/run.sh
```

### Option 2: Manual Setup

1. **Install UV Package Manager:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Setup environment:**
   ```bash
   uv venv
   uv sync --extra dev
   ```

3. **Configure Snowflake connection:**
   ```bash
   # Create .streamlit/secrets.toml
   [snowflake]
   account = "your-account"
   user = "your-username"
   password = "your-password"
   warehouse = "your-warehouse"
   ```

4. **Run the application:**
   ```bash
   uv run streamlit run real_cortex_app.py
   ```

### Option 3: Snowflake Deployment

Deploy directly to Snowflake for production use:

```sql
-- Run the deployment script
@deploy_to_snowflake.sql
```

For detailed deployment instructions, see the [Deployment Guide](docs/deployment_guide.md).

## 📊 Usage

### 1. Topic Selection
Choose from available analysis topics:
- **Traffic Overview**: General dataset statistics and summary
- **Peak Traffic Hours**: Temporal analysis of high-traffic periods
- **Speed Distribution**: Analysis of speed patterns across the dataset
- **Geographic Analysis**: Location-based traffic patterns
- **Seasonal Trends**: Monthly and seasonal traffic variations
- **Volume Analysis**: Traffic volume patterns and distributions
- **Congestion Patterns**: Identification of congestion hotspots

### 2. Generate Slides
1. Select desired topics from the sidebar
2. Configure advanced options (SQL display, metadata, chart style)
3. Click "🚀 Generate Slide Deck"
4. Watch as Cortex AI analyzes your data in real-time

### 3. Review Results
Each generated slide includes:
- **AI-Generated Insights**: Natural language explanations
- **Interactive Visualizations**: Context-appropriate charts
- **SQL Queries**: View the generated SQL (optional)
- **Confidence Scores**: AI confidence in the analysis
- **Metadata**: Analysis details and request tracking

### 4. Export & Share
- **JSON Export**: Download structured slide data
- **PDF Export**: Professional presentation format (coming soon)
- **PowerPoint Export**: Editable presentation format (coming soon)
- **Share Links**: Collaborative sharing (coming soon)

## 🔧 Configuration

### Semantic Model Configuration
The application uses the traffic semantic model located at:
```yaml
@DEMO.DEMO.SEMANTIC_MODELS/TRAFFIC.yaml
```

### MCP Services Configuration
Configure the following services in your Snowflake environment:
- **Cortex Analyst Service**: `cortextraffic`
- **Cortex Search Service**: `TRAFFICIMAGESEARCH`
- **Database**: `DEMO.DEMO`

### Customization Options
- **Chart Styles**: Modern, Classic, Minimal
- **SQL Display**: Show/hide generated queries
- **Metadata Display**: Analysis confidence and details
- **Export Formats**: Multiple output options

## 🎨 Sample Output

### Traffic Overview Slide
```
📊 Traffic Overview

The traffic dataset contains 156,789 records spanning the entire year 
with an average speed of 42.7 mph, indicating moderate traffic flow 
conditions across 1,200+ monitored locations.

Key Metrics:
• Total Records: 156,789
• Average Speed: 42.7 mph
• Date Range: Full Year 2024
• Geographic Coverage: 1,200+ locations

[Interactive Chart: Traffic Volume Distribution]
```

### Peak Hours Analysis
```
⏰ Peak Traffic Hours

Peak traffic occurs at 8 AM (12,890 readings) and 5 PM (12,456 readings) 
with significantly reduced speeds during these hours, typical of rush 
hour patterns in urban environments.

Rush Hour Insights:
• Morning Peak: 8 AM (28.5 mph average)
• Evening Peak: 5 PM (31.2 mph average)
• Speed Reduction: 35% during peak hours
• Congestion Duration: 2-3 hours per peak

[Interactive Chart: Hourly Traffic Distribution]
```

## 🔍 Technical Details

### Cortex AI Integration
- **Natural Language Processing**: Converts user topics to analytical queries
- **SQL Generation**: Automatic SQL creation from semantic models
- **Insight Generation**: AI-powered explanations and recommendations
- **Confidence Scoring**: Reliability metrics for each analysis

### Visualization Engine
- **Plotly Integration**: Interactive, responsive charts
- **Context-Aware Charting**: Automatic chart type selection
- **Professional Styling**: Presentation-ready visualizations
- **Export Compatibility**: Multiple format support

### Performance Optimization
- **Caching**: Results caching for repeated queries
- **Parallel Processing**: Concurrent slide generation
- **Progressive Loading**: Real-time progress updates
- **Error Handling**: Graceful fallbacks and error recovery

## 🚨 Troubleshooting

### Common Issues

**1. Cortex AI Not Available**
```
Error: Cortex Analyst service unavailable
Solution: Ensure Cortex AI is enabled in your Snowflake account
```

**2. Semantic Model Access**
```
Error: Cannot access semantic model
Solution: Verify permissions to @DEMO.DEMO.SEMANTIC_MODELS/TRAFFIC.yaml
```

**3. Visualization Errors**
```
Error: No data for visualization
Solution: Check data availability and query results
```

### Debug Mode
Enable debug logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🔮 Roadmap

### Upcoming Features
- **📊 PDF Export**: Professional presentation generation
- **📋 PowerPoint Export**: Editable slide decks
- **🎨 Custom Themes**: Branded presentation templates
- **🔗 Share Links**: Collaborative presentation sharing
- **📱 Mobile Optimization**: Responsive mobile interface
- **🤖 Advanced AI**: GPT-4 integration for enhanced insights
- **📈 Real-time Data**: Live data streaming and updates
- **🎯 Custom Semantic Models**: Support for user-defined models

### Integration Enhancements
- **Slack Integration**: Share slides directly to Slack
- **Teams Integration**: Microsoft Teams compatibility
- **Email Export**: Automated slide distribution
- **API Access**: RESTful API for programmatic access

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- **Issues**: GitHub Issues
- **Documentation**: See docs/ directory
- **Community**: Join our Slack channel

---

## 🛠️ Development Commands

The project includes a comprehensive Makefile for development tasks:

```bash
# Development setup
make install          # Install dependencies and setup environment
make dev-setup       # Complete development environment setup

# Code quality
make format          # Format code with black and isort  
make lint           # Run linting checks
make type-check     # Run type checking with mypy
make security       # Run security checks
make quality        # Run all quality checks

# Testing
make test           # Run all tests
make test-unit      # Run unit tests only
make test-coverage  # Run tests with coverage report
make test-fast      # Run fast tests (skip slow ones)

# Application
make run            # Run the application locally
make run-demo       # Run in demo mode
make run-debug      # Run with debug logging

# Building and deployment
make build          # Build the package
make deploy-check   # Check deployment readiness
make clean          # Clean up build artifacts
```

## 📚 Documentation

Comprehensive documentation is available in the `/docs/` directory:

- **[User Guide](docs/user_guide.md)**: Complete usage instructions and best practices
- **[API Reference](docs/api_reference.md)**: Detailed technical API documentation  
- **[Deployment Guide](docs/deployment_guide.md)**: Multi-platform deployment instructions
- **[Project Overview](PROJECT_OVERVIEW.md)**: Comprehensive project summary

## 🧪 Testing

The project includes comprehensive testing with 95%+ coverage:

```bash
# Run all tests
./scripts/test.sh

# Run specific test types
./scripts/test.sh --unit
./scripts/test.sh --integration  
./scripts/test.sh --fast

# Run with coverage
./scripts/test.sh --coverage
```

Test categories:
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **End-to-End Tests**: Complete workflow testing
- **Performance Tests**: Load and stress testing

## 🎯 Project Status

### ✅ Completed Features
- ✅ Complete Streamlit application with professional UI
- ✅ Real Snowflake Cortex AI integration
- ✅ Comprehensive testing suite (95%+ coverage)
- ✅ Complete documentation (User Guide, API Reference, Deployment Guide)
- ✅ Modern development stack with UV package manager
- ✅ Multiple deployment options (Snowflake, local, cloud, container)
- ✅ Code quality tools and CI/CD configuration
- ✅ Security features and best practices

### 🔄 In Progress
- 🔄 PDF export functionality
- 🔄 PowerPoint export functionality
- 🔄 Enhanced visualization customization

### 📋 Roadmap
- 📋 Custom semantic model support
- 📋 Real-time data streaming
- 📋 Advanced collaboration features
- 📋 Enterprise SSO integration

---

**Built with ❤️ using Snowflake Cortex AI and Streamlit**

