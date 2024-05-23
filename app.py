from flask import Flask, request, render_template, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('dashboard', filename=file.filename))

@app.route('/dashboard/<filename>')
def dashboard(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)
    columns = df.columns.tolist()
    return render_template('dashboard.html', filename=filename, columns=columns)




@app.route('/sum/<filename>', methods=['POST'])
def sum_column(filename):
    column_name = request.form['column']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)
      
    if column_name in df.columns:
        df[column_name] = df[column_name].str.replace(',', '').astype(int)
        total_sum = df[column_name].sum()  # Calculate the sum for the specified column
        return f"The total sum of '{column_name}' is: {total_sum}"
    return redirect(url_for('dashboard', filename=filename, error='Column not found'))

@app.route('/display_sum')
def display_sum():
    column = request.args.get('column')
    total_sum = request.args.get('total_sum')
    return render_template('display_sum.html', column=column, total_sum=total_sum)

@app.route('/stock_availability')
def stock_availability():
    return render_template('stock_availability.html')

if __name__ == '__main__':
    app.run(debug=True)












