# TenderX - Country Information Agent

An intelligent AI-powered assistant that answers natural language questions about countries using real-time data from public APIs. Built with modern Python and leveraging state-of-the-art language models for seamless user interaction.

## 🌟 Features

- **Natural Language Understanding**: Ask questions about countries in plain English
- **Intelligent Tool Selection**: AI automatically selects the most appropriate data source
- **Real-time Data Retrieval**: Access current information about population, capital, currency, language, and region
- **Robust Error Handling**: Graceful handling of API failures with clear, user-friendly output
- **Interactive CLI**: User-friendly command-line interface with real-time feedback
- **Multi-source Data**: Aggregates information from multiple reliable APIs

## 🛠️ Supported Queries

The agent can handle various types of country-related queries:

- **Population queries**: "What's the population of France?"
- **Capital information**: "What's the capital of Japan?"
- **Currency details**: "What currency does Germany use?"
- **Language information**: "What languages are spoken in Canada?"
- **Regional data**: "Which countries are in Western Europe?"

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Hugging Face API token** ([Get one here](https://huggingface.co/settings/tokens))
- **Internet connection** for API calls

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Raghavsharma10/TenderX
cd TenderX
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root by copying the example:
```bash
cp env.example .env
```

Then edit the `.env` file and add your actual Hugging Face API token:
```env
HF_TOKEN=your_actual_hugging_face_token_here
```

**Note**: Never commit your `.env` file to version control as it contains sensitive information.

## 🎯 Usage

### Running the Application
```bash
python simple_agents.py
```

### Example Interactions

```
Ask about a country: population of france
🔎 Raw tool plan: {'tool_name': 'get_country_by_name', 'parameters': {'name': 'France', 'fields': ['population']}}
🛠️  Calling get_country_by_name with {'name': 'France', 'fields': ['population']}

💬 France has a population of approximately 67,391,582 people.

Ask about a country: capital of japan
🔎 Raw tool plan: {'tool_name': 'get_country_by_name', 'parameters': {'name': 'Japan', 'fields': ['capital']}}
🛠️  Calling get_country_by_name with {'name': 'Japan', 'fields': ['capital']}

💬 The capital of Japan is Tokyo.
```

### Exiting the Application
Type `exit` or `quit` to close the application.

## 🏗️ Architecture

The project consists of three main components:

### 1. **API Wrapper** (`api_wrapper.py`)
- Interfaces with the REST Countries API
- Provides functions for different types of country data queries
- Handles API responses and error cases

### 2. **Tool Selector** (`tool_selector.py`)
- Uses Hugging Face LLM to understand user intent
- Selects the most appropriate API function for each query
- Implements robust JSON parsing for LLM responses

### 3. **Agent** (`simple_agents.py`)
- Main application logic and user interface
- Orchestrates the interaction between components
- Provides user-friendly output formatting

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `HF_TOKEN` | Hugging Face API token for LLM access | Yes |

### API Endpoints

The system uses the following external APIs:
- **REST Countries API**: For country data retrieval
- **Hugging Face Inference API**: For natural language understanding

## 📊 Available Data Fields

The system can retrieve the following information for countries:
- Population
- Capital cities
- Currencies
- Languages
- Subregions
- And more (based on REST Countries API availability)

## 🐛 Troubleshooting

### Common Issues

1. **"Could not understand the query"**
   - Ensure your Hugging Face token is valid
   - Check your internet connection
   - Try rephrasing your question

2. **"API returned no data"**
   - Verify the country name is spelled correctly
   - Check if the REST Countries API is accessible

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Verify you're using the correct Python version

### Debug Mode

The application provides detailed logging to help diagnose issues:
- Raw LLM outputs are displayed with 🧪 prefix
- API calls are logged with 🛠️ prefix
- Error messages are clearly marked with ❌ prefix

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [REST Countries API](https://restcountries.com/) for country data
- [Hugging Face](https://huggingface.co/) for LLM inference services
- [Zephyr-7B-Beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta) model for natural language understanding

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

## 🔮 Future Enhancements

- Web interface for easier access
- Support for more data sources
- Caching for improved performance
- Multi-language support
- Integration with additional APIs

---

**Made with ❤️ by [Raghav Sharma](https://github.com/Raghavsharma10)**

*Empowering users with AI-driven country information retrieval* 