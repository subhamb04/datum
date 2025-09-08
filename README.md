# Datum - AI-Powered Data Analysis Agent

A simple yet powerful data analysis agent that uses AI to generate SQL queries, execute them against your data, and provide visualizations and insights through a web interface.

## Features

- **Natural Language Queries**: Ask questions about your data in plain English
- **AI-Generated SQL**: Automatically converts questions into SQL queries
- **Data Visualization**: Generates charts and graphs from query results
- **Intelligent Insights**: Provides narrative analysis and recommendations
- **Web Interface**: Clean, user-friendly Gradio interface
- **DuckDB Integration**: Fast, in-memory SQL database for data analysis
- **LangSmith Tracing**: Built-in observability and debugging with LangSmith integration

## Project Structure

```
datum/
├── app.py              # Main application with LangGraph workflow
├── nodes.py            # Agent nodes (SQL generation, execution, charting, narration)
├── state.py            # Typed state definition for the agent
├── llm.py              # LLM configuration (Google Gemini)
├── db.py               # Database setup and data loading
├── charts.py           # Chart generation utilities
├── data/               # Sample datasets
│   ├── sales.csv
│   ├── marketing_spend.csv
│   └── customers.csv
└── requirements.txt    # Python dependencies
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

2. **View results**: The agent will provide:
   - **Query Result**: Data table with your results
   - **Chart**: Visual representation of the data
   - **Insights**: AI-generated analysis and recommendations
   - **SQL**: The generated SQL query for transparency

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
