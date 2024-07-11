from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    if 'csvData' not in request.form or 'question' not in request.form:
        return jsonify({'error': 'CSV data or question not provided'}), 400

    # Deserialize the JSON string into a DataFrame
    csv_data_str = request.form['csvData']
    csv_data = json.loads(csv_data_str)
    df = pd.DataFrame(csv_data)

    # Get the question
    question = request.form['question']

    response = handle_question(question, df)

    return jsonify(response)

def handle_question(question, df):
    question = question.strip().lower()
    if 'dataframe' in question:
        return generate_dataframe_sample(df)
    elif 'top' in question or 'first' in question:
        return generate_n_rows(df, n=extract_number(question, default=5), position='top')
    elif 'tail' in question or 'last' in question:
        return generate_n_rows(df, n=extract_number(question, default=5), position='tail')
    elif 'row' in question or 'rows' in question or 'row count' in question or 'number of rows' in question:
        return get_row_count(df)
    elif 'column names' in question or 'columns name' in question or 'columns names' in question or 'column name' in question:
        return get_column_names(df)
    elif 'column' in question or 'columns' in question or 'number of columns' in question:
        return get_number_of_columns(df)
    elif 'maximum' in question or 'max' in question:
        column_name = extract_column_name(question, df)
        if column_name:
            return get_max_value(df, column_name)
        else:
            return {'error': 'Column name not specified or not found'}
    elif 'minimum' in question or 'min' in question:
        column_name = extract_column_name(question, df)
        if column_name:
            return get_min_value(df, column_name)
        else:
            return {'error': 'Column name not specified or not found'}
    elif 'plot' in question:
        return plot(df)
    else:
        return {'error': f'Unhandled question type: {question}'}


response_data = {}
images = []

def plot(df):
    return {'error': f'Please go to Plot Section'}

def generate_dataframe_sample(df):    #correct
    return df.head().to_dict()

def generate_n_rows(df, n, position):   #correct
    if position == 'top':
        return df.head(n).to_dict()
    elif position == 'tail':
        return df.tail(n).to_dict()

def get_row_count(df):      #correct
    return {'Total number of rows': len(df)}

def get_number_of_columns(df):      #correct
    return {'Total number of columns': df.shape[1]}

def get_column_names(df):     #correct
    return {'Column names': df.columns.tolist()}

def get_max_value(df, column_name):   #correct
    if column_name in df.columns:
        return {f'Maximum value in {column_name}': df[column_name].max()}
    else:
        return {'error': f'Column {column_name} not found'}
    
def get_min_value(df, column_name):   #correct
    if column_name in df.columns:
        return {f'Minimum value in {column_name}': df[column_name].min()}
    else:
        return {'error': f'Column {column_name} not found'}

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


if __name__ == '__main__':
    app.run(port=5000)
