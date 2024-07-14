from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    try:
        if 'csvData' not in request.form or 'question' not in request.form:
            return jsonify({'error': 'CSV data or question not provided'}), 400

        # Deserialize the JSON string into a DataFrame
        csv_data_str = request.form['csvData']
        csv_data = json.loads(csv_data_str)
        df = pd.DataFrame(csv_data)

        # Convert columns to appropriate data types
        df = convert_column_types(df)

        # Log DataFrame for debugging
        print("DataFrame Loaded:")
        print(df.head())

        # Get the question
        question = request.form['question']
        print(f"Question: {question}")

        response = handle_question(question, df)

        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500

def convert_column_types(df):
    try:
        # Convert columns to numeric if possible
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')

        # Convert columns to boolean if they contain binary values
        for col in df.columns:
            if df[col].dropna().astype(str).isin(['0', '1']).all():
                df[col] = df[col].astype(bool)

        return df
    except Exception as e:
        print(f"Error in convert_column_types: {str(e)}")
        raise

def handle_question(question, df):
    try:
        question = question.strip().lower()
        if 'dataframe' in question:
            return generate_dataframe_sample(df)
        elif 'top' in question or 'first' in question:
            return generate_n_rows(df, n=extract_number(question, default=5), position='top')
        elif 'tail' in question or 'last' in question:
            return generate_n_rows(df, n=extract_number(question, default=5), position='tail')
        elif 'row' in question or 'rows' in question or 'row count' in question or 'number of rows' in question:
            return get_row_count(df)
        elif 'column names' in question or 'columns name' in question or 'columns names' in question or 'column name' in question or ('name' in question and 'column' in question) or ('name' in question and 'columns' in question) or ('names' in question and 'column' in question) or ('names' in question and 'columns' in question):
            return get_column_names(df)
        elif 'column' in question or 'columns' in question or 'number of columns' in question:
            return get_number_of_columns(df)
        elif 'shape' in question:
            return get_dataframe_shape(df)
        elif 'data types' in question or 'data type' in question or 'dtypes' in question:
            return get_data_types(df)
        elif 'missing values' in question or 'missing' in question or 'null' in question:
            return get_missing_values(df)
        elif 'maximum' in question or 'max' in question:
            column_name = extract_column_name(question, df)
            if column_name:
                return get_max_value(df, column_name)
            else:
                return 'Column name not specified or not found'
        elif 'minimum' in question or 'min' in question:
            column_name = extract_column_name(question, df)
            if column_name:
                return get_min_value(df, column_name)
            else:
                return 'Column name not specified or not found'
        elif 'plot' in question:
            return plot(df)
        else:
            return f'Unhandled question type: {question}. Please ask me database type questions'
    except Exception as e:
        print(f"Error in handle_question: {str(e)}")
        return f"Error in handle_question: {str(e)}"

def plot(df):
    return 'Sorry, I can’t generate any plots (line, bar, scatter, etc.). Please go to the plot section to generate them.'

def generate_dataframe_sample(df):
    return format_dataframe(df.head())

def generate_n_rows(df, n, position):
    if position == 'top':
        return format_dataframe(df.head(n))
    elif position == 'tail':
        return format_dataframe(df.tail(n))

def get_row_count(df):
    return f'Total number of rows: {len(df)}'

def get_number_of_columns(df):
    return f'Total number of columns: {df.shape[1]}'

def get_column_names(df):
    return f'Column names: {", ".join(df.columns)}'

def get_dataframe_shape(df):
    return f'Shape of the DataFrame: {df.shape}'

def get_data_types(df):
    return f'Data types of the DataFrame: {df.dtypes.astype(str).to_dict()}'

def get_missing_values(df):
    try:
        missing_values = df.isnull().sum()
        missing_values_dict = missing_values[missing_values > 0].to_dict()
        return f'Missing values: {missing_values_dict}'
    except Exception as e:
        print(f"Error in get_missing_values: {str(e)}")
        return f"Error in get_missing_values: {str(e)}"

def get_max_value(df, column_name):
    if column_name in df.columns:
        try:
            max_value = df[column_name].max()
            return f'Maximum value in {column_name}: {max_value}'
        except TypeError as e:
            return f'Cannot determine maximum value for column {column_name} with non-numeric data: {str(e)}'
    else:
        return f'Column {column_name} not found'

def get_min_value(df, column_name):
    if column_name in df.columns:
        try:
            min_value = df[column_name].min()
            return f'Minimum value in {column_name}: {min_value}'
        except TypeError as e:
            return f'Cannot determine minimum value for column {column_name} with non-numeric data: {str(e)}'
    else:
        return f'Column {column_name} not found'

def extract_number(question, default=5):
    words = question.split()
    for word in words:
        if word.isdigit():
            return int(word)
    return default

def extract_column_name(question, df):
    words = question.split()
    for word in words:
        # Case-insensitive match
        for column in df.columns:
            if word.lower() == column.lower():
                return column
    return None

def format_dataframe(df):
    formatted_rows = []
    header = " | ".join(df.columns)
    separator = "" * len(header)
    formatted_rows.append(header)
    formatted_rows.append(separator)
    for index, row in df.iterrows():
        formatted_rows.append(" | ".join(map(str, row.values)))
    return "    ------->    ".join(formatted_rows)



if __name__ == '__main__':
    app.run(port=5000)
