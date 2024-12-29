# SQL Data Assistant

## Overview
SQL Data Assistant is a Streamlit-powered application that enables users to upload datasets, ask natural language questions, and receive SQL queries and results as output. This tool is particularly useful for data analysts, developers, and anyone looking to interact with data using SQL without writing queries manually.

## Features
- Upload CSV or Excel files for processing.
- Automatically normalize column names for SQL compatibility.
- Ask natural language questions about your dataset.
- Generate SQL queries dynamically using OpenAI's GPT-powered assistant.
- Execute the generated SQL query and display the results.
- In-memory SQLite database for query execution.

## Requirements
- Python 3.9 or later
- Streamlit
- Pandas
- Phidata
- OpenAI API Key
- SQLite (comes pre-installed with Python)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-repo/sql-data-assistant.git
cd sql-data-assistant
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up OpenAI API Key
You need an OpenAI API Key to use the assistant. Obtain one from [OpenAI](https://platform.openai.com/).

Store your key securely, as you'll need to input it into the application.

## Usage

### Step 1: Run the Application
```bash
streamlit run app.py
```

### Step 2: Interact with the App
1. **Upload a Dataset**:
   - Use the sidebar to upload a CSV or Excel file.
   - The application will display the data and normalize the column names.
2. **Enter Your Question**:
   - Ask a natural language question, such as "What is the highest data_value?".
3. **View Results**:
   - The application will generate an SQL query, execute it, and display the results.

## Example Questions
- What is the average value in the `Data_value` column?
- How many rows have `STATUS` equal to 'F'?
- Show all rows where `Period` is greater than 2018.

## File Structure
```
sql-data-assistant/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── sample_data/         # Directory for example datasets (if any)
```

## Error Handling
### Common Issues
1. **Unicode Errors**:
   - If special characters or emojis cause errors, ensure UTF-8 encoding is used.
2. **SQL Execution Errors**:
   - Ensure column names in your dataset match the generated SQL query.
3. **File Format Errors**:
   - Only CSV and Excel files are supported.

### Debugging Tips
- Check the Streamlit logs in the terminal for detailed error messages.
- Use the normalized column names displayed in the app to ensure compatibility.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments
- [Streamlit](https://streamlit.io/): For creating an intuitive web framework for Python.
- [OpenAI](https://openai.com/): For providing the GPT-based assistant.
- [Pandas](https://pandas.pydata.org/): For data manipulation and analysis.

---
Happy querying! 🚀

