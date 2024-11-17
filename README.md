# AI-Agent
## How to Use the Application

Follow the steps below to use the application for extracting data from your CSV file.

### 1. Start the Application
Run the Flask app by executing the following command in your terminal:
```bash
python app.py
```
The app will start running locally and will be available at:
```
http://127.0.0.1:5000/
```

### 2. Access the Application in Your Browser
Open your browser and go to the above URL. You will see the application interface.

### 3. Input CSV File Path
- Enter the full path of the CSV file you want to process. Example:
  ```
  E:\AI Agent\Real_Companies_Data.csv
  ```
Make sure the file path is correct and points to a valid CSV file.

### 4. Enter Entity Column Name
- Input the column name from the CSV file that contains the primary entity for which data extraction is required. For example, if the column contains "Company Name," enter `Company Name`.

### 5. Specify Columns to Extract
- Provide a comma-separated list of column names you want to extract information for. For example:
  ```
  Founder Name, CEO Name, Locations
  ```

### 6. Submit the Form
- Click on the "Extract Data" button. The application will:
  1. Read your CSV file.
  2. Use SerpAPI to perform web searches for the specified columns.
  3. Use OpenAI GPT to extract and summarize relevant data.
  4. Save the extracted data to a new CSV file.

### 7. View and Download Results
Once the data extraction is complete:
- The extracted data will be displayed on a new page.
- A link to download the output CSV file (e.g., `extracted_results.csv`) will be provided.
