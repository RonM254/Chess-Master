# Chess Master Analysis

This project provides a comprehensive Chess Analysis tool compacted into a single, interactive Jupyter Notebook.

## Overview

The entire chess engine, including move validation, opening theory, and position evaluation, is contained within **`Chess_Analysis.ipynb`**.

### Features
*   **Chess Engine**: Complete board representation and piece logic.
*   **Opening Book**: Analyze common openings (Italian, Spanish, French, Scandinavian).
*   **Move Validator**: Checks legal moves and detects tactical patterns (forks, pins, etc.).
*   **Position Evaluator**: sophisticated evaluation function using material, activity, and pawn structure.
*   **Interactive Demo**: Play through games and see real-time analysis directly in the notebook.

## Getting Started

### Prerequisites
*   Python 3.8+
*   Jupyter Notebook or JupyterLab
*   Recommended: VS Code with Python/Jupyter extensions

### How to Run
1.  Open **`Chess_Analysis.ipynb`** in your notebook editor.
2.  Click **"Run All"** to execute the code cells.
3.  Scroll to the bottom to interact with the demo.

## Project Structure
*   `Chess_Analysis.ipynb`: The main application.
*   `generate_notebook.py`: Utility script used to generate the notebook (can be ignored or used to regenerate).
