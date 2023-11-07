from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

def find_present_value(payment, interest_rate, years):
    yearly_values = []
    for year in range(1, years + 1):
        year_value = payment * ((1 + interest_rate) ** year)
        yearly_values.append((year, round(year_value, 2)))
    total_value = sum(value for _, value in yearly_values)
    return yearly_values, round(total_value, 2)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    payment = data.get('payment')
    interest_rate = data.get('interest_rate')
    years = data.get('years')
    if payment is None or interest_rate is None or years is None:
        return jsonify({'error': 'Missing data'}), 400
    yearly_values, total_value = find_present_value(payment, interest_rate, years)
    return jsonify({'yearly_values': yearly_values, 'total_value': total_value})

if __name__ == '__main__':
    app.run(debug=True)