"""
Chess Game Reviewer
===================
Main entry point for playing and reviewing chess games.

Usage:
    python src/review_game.py

This script allows you to:
- Play a game by entering moves
- Get comprehensive analysis after each move
- Review the complete game with full analysis
"""

import sys
from pathlib import Path

# Add project root to path so we can import 'src'
# If running as 'python src/review_game.py', __file__ is inside src/
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.game_manager import GameManager
from src.chess_engine import Color


def parse_move(move_str: str) -> tuple:
    """
    Parse a move string into (from_pos, to_pos).
    
    Accepts formats:
    - "e2-e4" or "e2e4" or "e2 e4"
    - "e2e4"
    """
    move_str = move_str.strip().replace(" ", "").replace("-", "")
    if len(move_str) == 4:
        return (move_str[0:2], move_str[2:4])
    return None


def review_game(moves: list):
    """
    Review a complete game by playing all moves and analyzing.
    
    Args:
        moves: List of moves in format [("e2", "e4"), ("e7", "e5"), ...]
    """
    print("\\n" + "=" * 70)
    print("CHESS GAME REVIEW")
    print("=" * 70)
    
    game = GameManager()
    
    print("\\n📋 GAME SUMMARY:")
    print(f"   Total moves to review: {len(moves)}")
    
    # Play all moves
    print("\\n🎮 PLAYING GAME:")
    for i, (from_pos, to_pos) in enumerate(moves, 1):
        success = game.make_move(from_pos, to_pos)
        player = "White" if i % 2 == 1 else "Black"
        move_num = (i + 1) // 2
        
        if success:
            print(f"   {move_num}. {player}: {from_pos}-{to_pos} ✓")
        else:
            print(f"   {move_num}. {player}: {from_pos}-{to_pos} ✗ INVALID MOVE")
            print(f"      ⚠️  Game stopped - invalid move detected!")
            break
    
    # Display final position
    print("\\n📊 FINAL POSITION:")
    game.display_board()
    
    # Full analysis
    print("\\n" + "=" * 70)
    game.print_full_analysis()
    
    # Move-by-move review
    print("\\n" + "=" * 70)
    print("MOVE-BY-MOVE REVIEW")
    print("=" * 70)
    
    # Reset and replay with analysis
    game.reset_board()
    for i, (from_pos, to_pos) in enumerate(moves, 1):
        if not game.make_move(from_pos, to_pos):
            break
        
        player = "White" if i % 2 == 1 else "Black"
        move_num = (i + 1) // 2
        
        print(f"\\n{move_num}. {player}: {from_pos}-{to_pos}")
        analysis = game.analyze_position()
        print(f"   Score: {analysis['total_score']} cp ({analysis['assessment']})")
        print(f"   Phase: {analysis['phase']}")
        
        # Show best moves after this move
        best = game.get_best_moves(2)
        if best:
            print(f"   Best responses: ", end="")
            for move in best:
                print(f"{move['move']} ({move['score']} cp) ", end="")
            print()
    
    print("\\n" + "=" * 70)
    print("REVIEW COMPLETE")
    print("=" * 70)


def interactive_game():
    """Interactive mode: play moves one by one with analysis."""
    print("\\n" + "=" * 70)
    print("INTERACTIVE CHESS GAME")
    print("=" * 70)
    print("\\nEnter moves in format: e2e4 or e2-e4 or e2 e4")
    print("Commands: 'quit' to exit, 'undo' to undo last move, 'analyze' for full analysis")
    print("=" * 70)
    
    game = GameManager()
    game.display_board()
    
    move_count = 0
    
    while True:
        player = "White" if game.current_player == Color.WHITE else "Black"
        move_num = (move_count // 2) + 1
        
        print(f"\\nMove {move_num} - {player} to move")
        print("Enter move (or 'quit'/'undo'/'analyze'): ", end="")
        
        user_input = input().strip().lower()
        
        if user_input == 'quit':
            print("\\nGame ended.")
            break
        elif user_input == 'undo':
            if game.undo_last_move():
                move_count = max(0, move_count - 1)
                print("   ✓ Move undone")
                game.display_board()
            else:
                print("   ✗ No moves to undo")
        elif user_input == 'analyze':
            game.print_full_analysis()
        else:
            parsed = parse_move(user_input)
            if parsed:
                from_pos, to_pos = parsed
                success = game.make_move(from_pos, to_pos)
                if success:
                    move_count += 1
                    print(f"   ✓ {from_pos}-{to_pos} played")
                    game.display_board()
                    
                    # Quick analysis
                    analysis = game.analyze_position()
                    print(f"\\n   Position: {analysis['assessment']} ({analysis['total_score']} cp)")
                    print(f"   Phase: {analysis['phase']}")
                else:
                    print(f"   ✗ Invalid move: {from_pos}-{to_pos}")
            else:
                print("   ✗ Invalid format. Use: e2e4 or e2-e4")


def main():
    """Main entry point."""
    print("\\n" + "=" * 70)
    print("CHESS MASTERY HUB - GAME REVIEWER")
    print("=" * 70)
    print("\\nChoose mode:")
    print("1. Review a pre-defined game (example game)")
    print("2. Interactive mode (play moves one by one)")
    print("3. Review custom game (paste moves)")
    print("\\nEnter choice (1-3): ", end="")
    
    choice = input().strip()
    
    if choice == "1":
        # Example: Italian Game
        example_moves = [
            ("e2", "e4"),  # White
            ("e7", "e5"),  # Black
            ("g1", "f3"),  # White
            ("b8", "c6"),  # Black
            ("f1", "c4"),  # White
            ("f8", "c5"),  # Black
            ("c2", "c3"),  # White
            ("g8", "f6"),  # Black
            ("d2", "d4"),  # White
        ]
        review_game(example_moves)
        
    elif choice == "2":
        interactive_game()
        
    elif choice == "3":
        print("\\nEnter moves (one per line, format: e2e4)")
        print("Enter empty line when done:")
        moves = []
        while True:
            move_str = input().strip()
            if not move_str:
                break
            parsed = parse_move(move_str)
            if parsed:
                moves.append(parsed)
            else:
                print(f"   ⚠️  Invalid format: {move_str}")
        
        if moves:
            review_game(moves)
        else:
            print("No moves entered.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
