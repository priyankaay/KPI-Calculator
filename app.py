from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  
@app.route('/calculate', methods=['POST'])
def calculate_sum():
    try:

        kpi = request.form['kpi']
        csvfile = request.files['csvfile']

        df = pd.read_csv(csvfile)

        if kpi in df.columns:
            print(f"Found column '{kpi}' in the CSV file.") 
            df[kpi] = df[kpi].str.replace(',', '').astype(int)
            total_sum = df[kpi].sum()
            return f"Total sum of '{kpi}' column: {total_sum}"
        else:
            print(f"Column '{kpi}' not found in the CSV file.")  
            return f"Column '{kpi}' not found in the CSV file."
    
        return render_template('calculate.html')

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

