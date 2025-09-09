---
title: datum
app_file: app.py
sdk: gradio
sdk_version: 5.44.1
---
# Datum - AI-Powered Data Analysis Agent

A simple yet powerful data analysis agent that uses AI to generate SQL queries, execute them against your data, and provide visualizations and insights through a web interface.

## Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **Auto Routing (Chat vs SQL)**: Agent decides between a quick chat reply or full SQL/database analysis
- **AI-Generated SQL**: Automatically converts questions into SQL queries
- **Data Visualization**: Generates charts and graphs from query results
- **Intelligent Insights**: Provides narrative analysis and recommendations
- **Web Interface**: Clean, user-friendly Gradio interface
- **DuckDB Integration**: Fast, in-memory SQL database for data analysis
- **LangSmith Tracing**: Built-in observability and debugging with LangSmith integration

## Project Structure

```
datum/
├── app.py                  # Main application with LangGraph workflow
├── builder/
│   ├── graph_builder.py    # Graph with router + conditional edges
│   ├── nodes.py            # Agent nodes (decider, chat, SQL, charting, narration)
│   ├── state.py            # Typed state definition for the agent
│   └── ui.py               # Gradio UI wiring
├── clients/
│   └── llm.py              # LLM configuration (Google Gemini)
├── datastore/
│   └── db.py               # DuckDB setup and data loading
├── utils/
│   ├── charts.py           # Chart generation utilities
│   ├── insight_utils.py    # Insight helpers
│   └── tracer_utils.py     # LangSmith tracing helpers
├── data/                   # Sample datasets
│   ├── sales.csv
│   ├── marketing_spend.csv
│   └── customers.csv
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google API key for Gemini AI

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd datum
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   LANGCHAIN_PROJECT=datum-analysis  # Optional: for LangSmith tracing
   LANGCHAIN_API_KEY=your_langsmith_api_key  # Optional: for LangSmith tracing
   LANGCHAIN_TRACING_V2=true  # Optional: enable LangSmith tracing
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the web interface**
   Open your browser and navigate to the URL shown in the terminal (typically `http://127.0.0.1:7860`)

## Usage

1. **Ask a question**: Type your data analysis question in natural language
   - Example: "What are the top 3 regions by revenue?"
   - Example: "Show me marketing spend by channel"
   - Example: "Which products have the highest unit sales?"

2. **Agent chooses the path automatically**
   - **Chat route**: Direct conversational answer when no database analysis is needed
   - **SQL route**: The agent generates SQL and provides:
     - **Query Result** (table)
     - **Chart** (visualization)
     - **Insights** (narrative + recommendation)
     - **SQL** (for transparency)

### Routing at a Glance
The `decider` node analyzes your question and sets a `route` of `chat` or `sql`. The graph then either calls `general_chat` or runs the SQL flow (`sql_generator` → `sql_executor` → `chart_generator` + `narrator`).

## Sample Data

The project includes sample datasets:
- **Sales**: Date, region, product, revenue, units sold
- **Marketing Spend**: Date, region, channel, spend amount
- **Customers**: Customer ID, region, age, income

## Technology Stack

- **LangGraph**: Workflow orchestration
- **Google Gemini**: AI language model
- **DuckDB**: In-memory SQL database
- **Gradio**: Web interface
- **Matplotlib**: Chart generation
- **Pandas**: Data manipulation
- **LangSmith**: Observability and tracing platform

## Customization

- **Add your own data**: Replace CSV files in the `data/` directory and update the schema in `nodes.py`
- **Modify the LLM**: Change the model or provider in `llm.py`
- **Customize charts**: Modify chart generation logic in `charts.py`
- **Extend the workflow**: Add new nodes to the LangGraph workflow in `app.py`

## Observability & Debugging

The application includes built-in LangSmith tracing for monitoring and debugging:

- **Trace Execution**: All agent steps are automatically traced and logged
- **Performance Monitoring**: Track execution times and token usage
- **Debug Information**: View detailed logs of SQL generation, execution, and LLM calls
- **Project Organization**: Traces are organized by project name for easy filtering

To enable tracing, set the LangSmith environment variables in your `.env` file. Without these variables, the application will run normally but without tracing capabilities.

## Troubleshooting

- **API Key Error**: Ensure your `GOOGLE_API_KEY` is set correctly in the `.env` file
- **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Data Issues**: Verify your CSV files are in the correct format and location
- **Tracing Issues**: Check LangSmith credentials if you want to use the observability features

## License

This project is open source and available under the MIT License.
