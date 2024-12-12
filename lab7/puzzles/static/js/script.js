document.addEventListener('DOMContentLoaded', () => {
    generateNewGame();

    document.getElementById('new-game-btn').addEventListener('click', generateNewGame);
    document.getElementById('solve-btn').addEventListener('click', solvePuzzle);
});

function generateNewGame() {
    const difficulty = document.getElementById('difficulty').value;
    fetch(`/generate?difficulty=${difficulty}`)
        .then(response => response.json())
        .then(puzzle => {
            displayPuzzle(puzzle);
        });
}


function solvePuzzle() {
    const puzzle = getPuzzleFromGrid();
    fetch('/solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(puzzle)
    })
    .then(response => response.json())
    .then(solvedPuzzle => {
        displayPuzzle(solvedPuzzle);
    });
}

function displayPuzzle(puzzle) {
    const table = document.getElementById('sudoku-grid');
    table.innerHTML = '';

    for (let i = 0; i < 9; i++) {
        const row = table.insertRow();
        for (let j = 0; j < 9; j++) {
            const cell = row.insertCell();
            if (puzzle[i][j] !== 0) {
                cell.textContent = puzzle[i][j];
                cell.classList.add('initial');
            } else {
                const input = document.createElement('input');
                input.type = 'number';
                input.min = '1';
                input.max = '9';
                input.addEventListener('input', () => {
                    if (input.value.length > 1) {
                        input.value = input.value.slice(0, 1);
                    }
                });
                cell.appendChild(input);
            }
        }
    }
}

function getPuzzleFromGrid() {
    const table = document.getElementById('sudoku-grid');
    const puzzle = [];

    for (let i = 0; i < 9; i++) {
        const row = [];
        for (let j = 0; j < 9; j++) {
            const cell = table.rows[i].cells[j];
            const input = cell.querySelector('input');
            if (input) {
                row.push(input.value ? parseInt(input.value) : 0);
            } else {
                row.push(parseInt(cell.textContent));
            }
        }
        puzzle.push(row);
    }

    return puzzle;
}