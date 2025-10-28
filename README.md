
This project was developed during my summer internship at ABB R&D Electrification (2025).
It’s a Python desktop application that leverages Google Gemini AI to classify sustainability-related research papers and visualize emerging trends in the field.

# Article Classification Tool 



## Project Overview
This project is a Tkinter-based GUI application that helps researchers and data analysts to automatically classify scientific articles using Google's Gemini AI. It includes features for retrieving articles from Scopus and generating visualizations.

### Key Features:
- **Gemini AI Classification**: Advanced topic classification using Google's Gemini model
- **Scopus Integration**: Fetch articles from Scopus using ISSN and year range
- **Interactive Visualizations**: 
  - Word cloud generation from article abstracts
  - Interactive graphs showing article distribution over time
  - Citation analysis dashboards
- **Simplified Workflow**: Streamlined UI with fewer clicks for better user experience

## Prerequisites

### System Requirements
- **Python**: Version 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Internet Connection**: Required for API calls to Scopus and Gemini

### Required Software
1. **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/)
2. **Git**: Download from [git-scm.com](https://git-scm.com/downloads)
3. **pip**: Usually comes with Python installation

### API Access Requirements
- **Scopus API Key**: Free registration at [Elsevier Developer Portal](https://dev.elsevier.com/apikey/manage)
- **Gemini API Key**: Free registration at [Google AI Studio](https://makersuite.google.com/app/apikey)

## Installation 

### 1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
###    Copy and paste these commands one by one:

```bash
git clone https://github.com/JakobSertcanli04/DataFiltrationProject
cd DataFiltrationProject
```

### 2. Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Additional Required Models
```bash
python -m spacy download en_core_web_sm
```

### 5. Configure API Keys
1. **Get Scopus API Key**:
   - Visit [Elsevier Developer Portal](https://dev.elsevier.com/apikey/manage)
   - Create a free account
   - Generate an API key
   - Update the API key in `source/scopus_data.py` (line 15)

2. **Get Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a free account
   - Generate an API key
   - Update the API key in `source/gemini.py` (line 35)

### 6. Verify Installation
```bash
python source/main.py
```
If the GUI window opens, installation is successful!

## ISSN Support

### Supported ISSN Format
The application supports **standard ISSN (International Standard Serial Number)** format:

- **Format**: 8 digits with optional hyphen (e.g., `1879-0690` or `187909090`)
- **Validation**: The program automatically validates ISSN existence in Scopus database
- **Database**: All ISSN queries are performed against the Scopus database via Elsevier API

### How ISSN is Used
1. **Journal Identification**: ISSN is used to uniquely identify journals in the Scopus database
2. **Article Retrieval**: All articles from the specified journal are fetched using the ISSN
3. **Data Validation**: The program first verifies the ISSN exists before proceeding with article retrieval

### Example ISSN Usage
```python
# Example from the codebase
journal = scopus_instance.getJournal("1879-0690", years, citation_limit)
```

### Finding ISSN Numbers
- **Journal Websites**: Most journals display their ISSN on their homepage
- **Scopus Database**: Search for journals directly on [scopus.com](https://www.scopus.com)
- **ISSN International Centre**: Visit [issn.org](https://www.issn.org) for official ISSN database

## Usage

### Running the Application
```bash
python source/main.py
```

### Workflow

#### 1. Fetch Articles from Scopus
1. Enter the ISSN of the journal you want to retrieve (e.g., `1879-0690`)
2. Specify the start and end years (e.g., 2020-2024)
3. Set a citation limit (optional, default: 0)
4. Choose where to save the CSV file
5. Click "Fetch Articles"

#### 2. Classify Articles with Gemini
1. Select your CSV file using the browse button
2. Enter topics for classification (comma-separated)
   - Example: `Semiconductor,Battery,Printed Circuit Board,Electrical Waste,Water Refinement,Emission`
3. Set minimum citation count (default: 10)
4. Click "Run Gemini Classification"

#### 3. Generate Visualizations
- **Word Cloud**: Click "Generate Word Cloud" to create a word cloud from article abstracts
- **Graph**: Click "Generate Graph" to create an interactive chart showing article distribution over time

## Input CSV Format
Your input CSV must have the following column headers:
- `DOI`
- `Title` 
- `Abstract`
- `Date`
- `Link`
- `CitationCount`
- `Label` (will be added after classification)

## Dependencies

### Core Dependencies
- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **requests**: HTTP library for API calls
- **matplotlib**: Basic plotting library
- **plotly**: Interactive visualizations
- **wordcloud**: Word cloud generation
- **google-generativeai**: Gemini AI integration
- **tqdm**: Progress bars
- **scikit-learn**: Machine learning utilities
- **pillow**: Image processing

### Additional Dependencies
- **spacy**: Natural language processing
- **tkinter**: GUI framework (usually comes with Python)

## Troubleshooting

### Common Issues
1. **API Key Errors**:
   - Ensure API keys are correctly updated in the respective files
   - Verify API keys are active and have sufficient quota

2. **ISSN Not Found**:
   - Verify the ISSN format (8 digits, optional hyphen)
   - Check if the journal exists in Scopus database
   - Ensure the ISSN is active and not discontinued

3. **Installation Issues**:
   - Make sure Python 3.7+ is installed
   - Use virtual environment to avoid dependency conflicts
   - Update pip: `pip install --upgrade pip`

4. **Memory Issues**:
   - For large datasets, increase system RAM
   - Process smaller year ranges at a time

### Getting Help
- Check the log output in the application for detailed error messages
- Ensure all prerequisites are properly installed
- Verify internet connectivity for API calls
- For large datasets, processing may take time - monitor the log output

## Notes
- The Gemini classifier requires an internet connection
- The Scopus fetching feature requires API access (follow Scopus Terms & Conditions)
- Visualizations are saved as files and opened in your default browser
- Word clouds are generated for articles with sufficient citations (default: 15+ citations)
- ISSN queries are performed against the Scopus database via Elsevier's API


       
