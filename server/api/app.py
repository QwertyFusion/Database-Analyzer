from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for rendering plots
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

@app.route('/plot', methods=['POST'])
def plot():
    try:
        data = request.json.get('data')
        plot_type = request.json.get('plot_type')
        column_name = request.json.get('column_name')
        y_column_name = request.json.get('y_column_name', None)

        df = pd.DataFrame(data)
        
        if column_name not in df.columns:
            return jsonify({'error': f'Column "{column_name}" not found in data.'})
        
        if y_column_name and y_column_name not in df.columns:
            return jsonify({'error': f'Column "{y_column_name}" not found in data.'})

        # Try to convert columns to numeric if they are not already
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
        if y_column_name:
            df[y_column_name] = pd.to_numeric(df[y_column_name], errors='coerce')

        plt.figure(figsize=(9, 5))

        if plot_type == 'line':
            df[column_name].plot(kind='line')
            plt.title(f'Line Plot of {column_name}')
            plt.xlabel("RowNumber")
            plt.ylabel(column_name)
        elif plot_type == 'bar':
            value_counts = df[column_name].value_counts()
            value_counts.plot(kind='bar')
            plt.title(f'Bar Plot of {column_name}')
        elif plot_type == 'hist':
            df[column_name].plot(kind='hist')
            plt.title(f'Histogram of {column_name}')
            plt.xlabel(column_name)
        elif plot_type == 'scatter' and y_column_name:
            df.plot(kind='scatter', x=column_name, y=y_column_name)
            plt.title(f'Scatter Plot of {column_name} vs {y_column_name}')
        elif plot_type == 'box':
            df[column_name].plot(kind='box')
            plt.title(f'Box Plot of {column_name}')
        elif plot_type == 'heatmap':
            numeric_df = df.select_dtypes(include=[np.number])
            if column_name in numeric_df.columns:
                sns.heatmap(numeric_df[[column_name]].corr(), annot=True, cmap='coolwarm')
            else:
                sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
            plt.title(f'Heatmap of Correlation Matrix')
        elif plot_type == 'density':
            df[column_name].plot(kind='density')
            plt.title(f'Density Plot of {column_name}')
            plt.xlabel(column_name)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return jsonify({'plot': plot_url})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
