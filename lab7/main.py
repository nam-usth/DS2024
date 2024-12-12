from flask import Flask, render_template, request, jsonify
from sudoku import generator  # Import your Sudoku generation logic

app = Flask(__name__)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate_sudoku():
    """Generates a new Sudoku puzzle."""
    difficulty = request.args.get('difficulty', 'easy') 
    puzzle = generator.generate_sudoku(difficulty)
    return jsonify(puzzle)

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    """Solves a given Sudoku puzzle."""
    puzzle = request.get_json()
    solved_puzzle = solver.solve_sudoku(puzzle)
    return jsonify(solved_puzzle)

if __name__ == '__main__':
    app.run(debug=True)