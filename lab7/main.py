from flask import Flask, render_template, request, jsonify
from sudoku import generator 

app = Flask(__name__)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate_sudoku():
    """Generates a new Sudoku puzzle."""
    difficulty = request.args.get('difficulty', 'easy') # Get difficulty from the request.
    puzzle = generator.generate_sudoku(difficulty)
    return jsonify(puzzle)

if __name__ == '__main__':
    app.run(debug=True)