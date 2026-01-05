"""
Example: Review a Chess Game
============================
Simple example showing how to review a chess game programmatically.

This is the place to plug in your game for review!
"""

import sys
from pathlib import Path

# Add project root to path so we can import 'src'
# If running as 'python src/example_game.py', __file__ is inside src/
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.game_manager import GameManager
from src.chess_engine import Color


def review_example_game():
    """Review an example game (Italian Game)."""
    
    # Create game manager
    game = GameManager()
    
    # Define your game moves here
    # Format: List of tuples (from_pos, to_pos)
    moves = [
        ("e2", "e4"),  # 1. e4
        ("e7", "e5"),  # 1... e5
        ("g1", "f3"),  # 2. Nf3
        ("b8", "c6"),  # 2... Nc6
        ("f1", "c4"),  # 3. Bc4
        ("f8", "c5"),  # 3... Bc5
        ("c2", "c3"),  # 4. c3
        ("g8", "f6"),  # 4... Nf6
        ("d2", "d4"),  # 5. d4
    ]
    
    print("=" * 70)
    print("REVIEWING GAME")
    print("=" * 70)
    print(f"\\nPlaying {len(moves)} moves...\\n")
    
    # Play all moves
    for i, (from_pos, to_pos) in enumerate(moves, 1):
        player = "White" if i % 2 == 1 else "Black"
        success = game.make_move(from_pos, to_pos)
        
        if success:
            print(f"[OK] {i}. {player}: {from_pos}-{to_pos}")
        else:
            print(f"[INVALID] {i}. {player}: {from_pos}-{to_pos}")
            break
    
    # Display final position
    print("\\n" + "=" * 70)
    print("FINAL POSITION")
    print("=" * 70)
    game.display_board()
    
    # Get comprehensive analysis
    print("\\n" + "=" * 70)
    print("COMPREHENSIVE ANALYSIS")
    print("=" * 70)
    game.print_full_analysis()
    
    # Additional analysis
    print("\\n" + "=" * 70)
    print("ADDITIONAL INSIGHTS")
    print("=" * 70)
    
    # Material balance
    material = game.get_material_balance()
    print(f"\\nMaterial Balance:")
    print(f"  White: {material['white']} points")
    print(f"  Black: {material['black']} points")
    print(f"  Advantage: {material['advantage']} ({material['advantage_side']})")
    
    # Tactics
    white_hanging = game.detect_hanging_pieces(Color.WHITE)
    black_hanging = game.detect_hanging_pieces(Color.BLACK)
    print(f"\\nTactical Opportunities:")
    print(f"  White hanging pieces: {len(white_hanging)}")
    print(f"  Black hanging pieces: {len(black_hanging)}")
    
    if white_hanging:
        print("  White hanging:")
        for piece in white_hanging:
            print(f"    - {piece['piece'].get_symbol()} on {piece['position']}")
    
    if black_hanging:
        print("  Black hanging:")
        for piece in black_hanging:
            print(f"    - {piece['piece'].get_symbol()} on {piece['position']}")
    
    # Best moves
    best = game.get_best_moves(3)
    print(f"\\nBest Moves for {game.current_player.value.capitalize()}:")
    for i, move in enumerate(best, 1):
        print(f"  {i}. {move['move']} → {move['score']} cp")
    
    print("\\n" + "=" * 70)
    print("REVIEW COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    review_example_game()
