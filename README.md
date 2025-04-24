# Retail Footfall Analyzer

A LangGraph-powered tool for analyzing retail footfall patterns and providing competitive insights for retail businesses.

## Overview

The Retail Footfall Analyzer creates a conversational AI workflow that processes natural language queries about footfall patterns and competitor analysis for retail locations. It leverages OpenAI's language models through LangGraph to provide structured insights about peak hours, customer traffic, and competitive landscape.

## Features

- **Location-based Analysis**: Get footfall insights for specific retail locations
- **Peak Hour Identification**: Discover the busiest times for retail stores
- **Competitor Insights**: Compare traffic patterns with competitor stores
- **Actionable Recommendations**: Receive strategic insights for business optimization

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/retail-footfall-analyzer.git
cd retail-footfall-analyzer

# Install dependencies
pip install langchain_openai langchain_core langchain_community langgraph==0.2.59
```

## Configuration

Create a `.env` file in the project root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Alternatively, you can provide the API key when initializing the analyzer.

## Usage

### Basic Usage

```python
from retail_footfall_analyzer import RetailFootfallAnalyzer

# Initialize the analyzer
analyzer = RetailFootfallAnalyzer()

# Run an analysis query
query = "Analyze the footfall patterns for retail stores in Marathahalli, Bangalore. Focus on peak hours and comparison with competitors."
result = analyzer.analyze(query)

# Access the final analysis
final_message = result['messages'][-1]
print(final_message.content)
```

### Customization

You can customize the analyzer by providing different parameters:

```python
# Use a different OpenAI model
analyzer = RetailFootfallAnalyzer(
    model_name="gpt-4",
    temperature=0.2
)
```

## Integrating with Real APIs

The default implementation uses mock data. To connect to a real retail footfall data API:

1. Replace the implementation in the `_query_retail_footprint_api` method with your actual API call
2. Add any necessary authentication (API keys, etc.)
3. Update the response parsing to match the format returned by your API

Example integration with a hypothetical API:

```python
def _query_retail_footprint_api(self, query: str) -> str:
    """Real API integration example"""
    api_key = os.getenv("RETAIL_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    
    params = {
        "location": self._extract_location(query),
        "include_competitors": True
    }
    
    response = requests.get(
        "https://api.retail-analytics.com/footfall",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        return response.text
    else:
        return json.dumps({"error": f"API error: {response.status_code}"})
```

## Project Structure

- `retail_footfall_analyzer.py` - Main module containing the RetailFootfallAnalyzer class
- `requirements.txt` - Dependencies
- `examples/` - Example usage scripts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
