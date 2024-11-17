from flask import Flask, request, render_template, send_file
import pandas as pd
from serpapi import GoogleSearch
import openai
import os

# Set your API keys here
SERP_API_KEY = 'your_serpapi_key' 
OPENAI_API_KEY = 'your_openai_api_key'

app = Flask(__name__)

# Function to upload the CSV file
def upload_file(file_path):
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV file.")
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Perform web search using SerpAPI
def perform_web_search(query, api_key=SERP_API_KEY):
    try:
        search = GoogleSearch({"q": query, "api_key": api_key})
        results = search.get_dict()
        return results.get('organic_results', [])
    except Exception as e:
        print(f"Web search error: {e}")
        return []

# Extract information using OpenAI LLM
def extract_information_with_llm(snippets, query, api_key=OPENAI_API_KEY):
    try:
        openai.api_key = api_key
        prompt = (
            f"Here are some search results for the query '{query}':\n\n"
            f"{snippets}\n\n"
            f"Provide the most accurate and concise information for the query."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"LLM extraction error for query '{query}': {e}")
        return "Error during extraction"

# Process the CSV file and extract required information
def process_data(file_path, entity_column, columns_to_extract):
    # Upload and read the CSV file
    data = upload_file(file_path)
    if data is None:
        return None

    # Check if the entity column exists
    if entity_column not in data.columns:
        print(f"Entity column '{entity_column}' not found in the file.")
        return None

    # Prepare a list to store the extracted data
    extracted_data = []

    for entity in data[entity_column]:
        print(f"Processing: {entity}")
        row = {"Entity": entity}  # Initialize row with the entity name
        
        # Loop over each column to extract
        for column in columns_to_extract:
            query = f"{column} of {entity}"
            search_results = perform_web_search(query)  # Perform web search for each query
            snippets = "\n".join([res.get('snippet', '') for res in search_results])  # Extract the snippet
            if snippets:
                extracted_info = extract_information_with_llm(snippets, query)  # Extract info using LLM
            else:
                extracted_info = "No data found"
            
            # Split the extracted information for each column separately
            row[column] = extracted_info

        extracted_data.append(row)  # Add row to the results

    # Convert the extracted data to a DataFrame and save to CSV
    output_df = pd.DataFrame(extracted_data)
    output_file = "extracted_results.csv"
    output_df.to_csv(output_file, index=False)

    return output_file

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and data processing
@app.route('/process', methods=['POST'])
def process():
    file_path = request.form['file_path']
    entity_column = request.form['entity_column']
    columns_to_extract = [col.strip() for col in request.form['columns'].split(',')]

    # Process the data and get the output file path
    output_file = process_data(file_path, entity_column, columns_to_extract)
    
    if output_file:
        return send_file(output_file, as_attachment=True)
    else:
        return "Error processing the file", 500

if __name__ == '__main__':
    app.run(debug=True)
