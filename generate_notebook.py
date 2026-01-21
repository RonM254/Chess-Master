import json
import os
import re

def create_notebook_cell(source_code, cell_type="code"):
    """Create a notebook cell dictionary."""
    return {
        "cell_type": cell_type,
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source_code.splitlines()]
    }

def clean_source_code(content):
    """Clean up source code for the notebook."""
    lines = content.splitlines()
    cleaned_lines = []
    
    for line in lines:
        # Remove internal imports
        if line.strip().startswith("from src."):
            continue
        if "sys.path" in line or "project_root" in line:
            continue
            
        cleaned_lines.append(line)
        
    return "\n".join(cleaned_lines)

def generate_notebook():
    notebook_structure = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    # 1. Introduction
    intro_markdown = """# Unified Chess Analysis Notebook

This notebook combines all the modules of the Chess Master project into a single, interactive environment. 
You can run this notebook to play games, analyze positions, and explore openings.

## Modules Included:
1. **Chess Engine**: Core board and piece representation.
2. **Opening Book**: Database of common openings.
3. **Move Validator**: Rules and tactical pattern detection.
4. **Position Evaluator**: Strategic analysis engine.
5. **Game Manager**: Unified interface for interaction.
"""
    notebook_structure["cells"].append(create_notebook_cell(intro_markdown, "markdown"))

    # File order based on dependencies
    files_to_process = [
        ("src/chess_engine.py", "## 1. Chess Engine\nCore data structures for the board and pieces."),
        ("src/opening_book.py", "## 2. Opening Book\nDatabase of openings and principles."),
        ("src/move_validator.py", "## 3. Move Validator\nLogic for move generation and validation."),
        ("src/position_evaluator.py", "## 4. Position Evaluator\nStatic evaluation function for positions."),
        ("src/game_manager.py", "## 5. Game Manager\nHigh-level interface to coordinate components.")
    ]

    base_path = os.getcwd()

    for relative_path, description in files_to_process:
        full_path = os.path.join(base_path, relative_path)
        
        # Add section header
        notebook_structure["cells"].append(create_notebook_cell(description, "markdown"))
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                cleaned_content = clean_source_code(content)
                notebook_structure["cells"].append(create_notebook_cell(cleaned_content, "code"))
                print(f"Processed {relative_path}")
        except FileNotFoundError:
            print(f"Error: Could not find {full_path}")
            return

    # Add Interactive Demo Cell
    demo_code = """# Interactive Demo
print("Initializing Game Manager...")
game = GameManager()

print("\\n1. Starting Position:")
game.display_board()

print("\\n2. Playing a sample game (Italian Game):")
# 1.e4 e5 2.Nf3 Nc6 3.Bc4
moves = [("e2", "e4"), ("e7", "e5"), ("g1", "f3"), ("b8", "c6"), ("f1", "c4")]

for start, end in moves:
    success = game.make_move(start, end)
    if success:
        print(f"Played {start}-{end}")

print("\\nCurrent Position:")
game.display_board()

print("\\n3. Analysis:")
analysis = game.analyze_position()
print(f"Evaluation: {analysis['total_score']} centipawns")
print(f"Assessment: {analysis['assessment']}")

print("\\n4. Opening Info:")
opening = game.get_current_opening()
if opening:
    print(f"Current Opening: {opening['opening']}")
    print("Key Ideas:")
    for idea in opening['ideas']:
        print(f"- {idea}")
"""
    notebook_structure["cells"].append(create_notebook_cell("## 6. Interactive Demo\nRun this cell to see the engine in action.", "markdown"))
    notebook_structure["cells"].append(create_notebook_cell(demo_code, "code"))

    # Write the notebook
    output_file = "Chess_Analysis.ipynb"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(notebook_structure, f, indent=1)
    
    print(f"\nSuccessfully created {output_file}")

if __name__ == "__main__":
    generate_notebook()
