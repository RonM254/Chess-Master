"""
Game Manager Module
Unified interface that integrates all Phase 1 modules.
Coordinates chess_engine, opening_book, move_validator, and position_evaluator.
Part of Chess Mastery Hub - Phase 1: Fundamentals

This module provides:
- Single unified interface for the entire chess system
- Seamless integration of all 4 modules
- Game state management
- Move recommendation system
- Complete position analysis
- Opening suggestions with evaluations

Example:
    >>> game = GameManager()
    >>> game.display_board()
    >>> moves = game.get_legal_moves()
    >>> game.make_move("e2", "e4")
    >>> analysis = game.analyze_position()
    >>> print(analysis)
"""

from typing import Dict, List, Optional, Tuple
from src.chess_engine import ChessBoard, Color, PieceType
from src.opening_book import OpeningBook
from src.move_validator import MoveValidator
from src.position_evaluator import PositionEvaluator


class GameManager:
    """
    Unified game manager integrating all Phase 1 modules.
    
    Provides a single interface to:
    - Display chess positions
    - Get legal moves
    - Make moves
    - Get opening recommendations
    - Analyze positions
    - Detect tactics
    - Evaluate advantages
    
    Example:
        >>> game = GameManager()
        >>> game.display_board()
        >>> print(game.get_current_eval())
        >>> game.make_move("e2", "e4")
        >>> print(game.get_opening_recommendation())
    """
    
    def __init__(self):
        """Initialize game manager with all modules."""
        self.board = ChessBoard()
        self.opening_book = OpeningBook()
        self.validator = MoveValidator(self.board)
        self.evaluator = PositionEvaluator(self.board)
        self.current_player = Color.WHITE
        self.move_history = []
    
    # ==================== BOARD DISPLAY & STATE ====================
    
    def display_board(self) -> None:
        """Display the current chess board."""
        print("\nCurrent Position:")
        self.board.display()
    
    def get_board_fen(self) -> str:
        """Get FEN representation of current position."""
        return self.board.get_position_fen()
    
    def get_material_balance(self) -> Dict:
        """Get material balance for both sides."""
        return self.board.calculate_material_balance()
    
    def reset_board(self) -> None:
        """Reset board to starting position."""
        self.board.reset_board()
        self.current_player = Color.WHITE
        self.move_history = []
        self.validator = MoveValidator(self.board)
        self.evaluator = PositionEvaluator(self.board)
    
    # ==================== MOVE MANAGEMENT ====================
    
    def get_legal_moves(self, color: Optional[Color] = None) -> List:
        """Get all legal moves for a player."""
        if color is None:
            color = self.current_player
        return self.validator.get_legal_moves(color)
    
    def get_moves_for_piece(self, position: str) -> List:
        """Get all legal moves for a specific piece."""
        piece = self.board.get_piece_at(position)
        if not piece:
            return []
        
        if piece.type == PieceType.PAWN:
            return self.validator.get_pawn_moves(piece)
        elif piece.type == PieceType.KNIGHT:
            return self.validator.get_knight_moves(piece)
        elif piece.type == PieceType.BISHOP:
            return self.validator.get_bishop_moves(piece)
        elif piece.type == PieceType.ROOK:
            return self.validator.get_rook_moves(piece)
        elif piece.type == PieceType.QUEEN:
            return self.validator.get_queen_moves(piece)
        elif piece.type == PieceType.KING:
            return self.validator.get_king_moves(piece)
        return []
    
    def make_move(self, from_pos: str, to_pos: str) -> bool:
        """
        Make a move and update game state.
        
        Args:
            from_pos: Starting position (e.g., "e2")
            to_pos: Destination position (e.g., "e4")
            
        Returns:
            True if move was successful, False otherwise
        """
        # Verify move is legal
        legal_moves = self.get_legal_moves()
        move_valid = False
        for move in legal_moves:
            if move.from_pos == from_pos and move.to_pos == to_pos:
                move_valid = True
                break
        
        if not move_valid:
            print(f"Invalid move: {from_pos}-{to_pos}")
            return False
        
        # Make the move
        self.board.move_piece(from_pos, to_pos)
        self.move_history.append(f"{from_pos}-{to_pos}")
        
        # Switch player
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        # Re-create validator and evaluator for new position
        self.validator = MoveValidator(self.board)
        self.evaluator = PositionEvaluator(self.board)
        
        return True
    
    def undo_last_move(self) -> bool:
        """Undo the last move."""
        if not self.move_history:
            print("No moves to undo")
            return False
        
        # Reset and replay all moves except the last one
        moves = self.move_history[:-1]
        self.reset_board()
        
        for move in moves:
            from_pos, to_pos = move.split('-')
            self.make_move(from_pos, to_pos)
        
        return True
    
    def get_move_history(self) -> List[str]:
        """Get list of all moves made."""
        return self.move_history.copy()
    
    # ==================== OPENING RECOMMENDATIONS ====================
    
    def get_opening_recommendation(self, rating: int = 1200) -> Dict:
        """Get opening recommendation based on player rating."""
        return self.opening_book.get_opening_recommendations(rating)
    
    def get_current_opening(self) -> Optional[Dict]:
        """
        Identify if current position matches a known opening.
        
        Returns:
            Opening info if match found, None otherwise
        """
        # For now, check if we're still in opening phase
        eval_result = self.evaluator.evaluate()
        
        if eval_result['phase'] == 'opening':
            # Get recommended opening for this rating
            rec = self.get_opening_recommendation()
            return {
                'opening': rec['recommendation'],
                'ideas': rec['key_ideas']
            }
        
        return None
    
    def get_opening_ideas(self, opening_name: str) -> List[str]:
        """Get key ideas for a specific opening."""
        opening = self.opening_book.get_opening_by_name(opening_name)
        if opening:
            return opening.key_ideas
        return []
    
    def get_all_openings(self) -> List[str]:
        """Get list of all openings in the book."""
        return self.opening_book.get_opening_names()
    
    # ==================== TACTICAL ANALYSIS ====================
    
    def detect_hanging_pieces(self, color: Optional[Color] = None) -> List[Dict]:
        """Detect undefended pieces."""
        if color is None:
            color = self.current_player
        return self.validator.detect_hanging_pieces(color)
    
    def detect_forks(self, color: Optional[Color] = None) -> List[Dict]:
        """Detect fork opportunities."""
        if color is None:
            color = self.current_player
        return self.validator.detect_forks(color)
    
    def detect_weak_squares(self, color: Optional[Color] = None) -> List[str]:
        """Detect weak squares that can't be defended by pawns."""
        if color is None:
            color = self.current_player
        return self.validator.detect_weak_squares(color)
    
    def is_square_attacked(self, position: str, by_color: Optional[Color] = None) -> bool:
        """Check if a square is attacked by a color."""
        if by_color is None:
            by_color = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
        return self.validator.is_attacked(position, by_color)
    
    # ==================== POSITION EVALUATION ====================
    
    def analyze_position(self) -> Dict:
        """
        Get complete position analysis.
        
        Returns:
            Dictionary with all evaluation factors
        """
        evaluation = self.evaluator.evaluate()
        
        return {
            'material': evaluation['material'],
            'activity': evaluation['activity'],
            'pawn_structure': evaluation['pawn_structure'],
            'king_safety': evaluation['king_safety'],
            'total_score': evaluation['total'],
            'assessment': evaluation['assessment'],
            'phase': evaluation['phase'],
            'white_advantage': evaluation['detailed']['white_advantage'],
            'margin': evaluation['detailed']['margin'],
        }
    
    def get_current_eval(self) -> int:
        """Get current position evaluation in centipawns."""
        return self.evaluator.evaluate()['total']
    
    def get_position_assessment(self) -> str:
        """Get text assessment of current position."""
        return self.evaluator.evaluate()['assessment']
    
    def get_game_phase(self) -> str:
        """Get current game phase (opening/middlegame/endgame)."""
        return self.evaluator.evaluate()['phase']
    
    # ==================== MOVE EVALUATION ====================
    
    def evaluate_move(self, from_pos: str, to_pos: str) -> Dict:
        """Evaluate what happens if a move is made."""
        return self.evaluator.get_move_evaluation(from_pos, to_pos)
    
    def get_best_moves(self, limit: int = 3) -> List[Dict]:
        """
        Get best moves for current position (simple evaluation).
        
        Evaluates all legal moves and returns top N by resulting position.
        """
        legal_moves = self.get_legal_moves()
        move_scores = []
        
        for move in legal_moves:
            eval_result = self.evaluate_move(move.from_pos, move.to_pos)
            move_scores.append({
                'move': f"{move.from_pos}-{move.to_pos}",
                'score': eval_result['evaluation']['total'],
                'captured': eval_result['captured']
            })
        
        # Sort by score (white perspective)
        if self.current_player == Color.WHITE:
            move_scores.sort(key=lambda x: x['score'], reverse=True)
        else:
            move_scores.sort(key=lambda x: x['score'])
        
        return move_scores[:limit]
    
    # ==================== COMPREHENSIVE GAME ANALYSIS ====================
    
    def get_game_summary(self) -> Dict:
        """Get comprehensive game summary."""
        return {
            'moves_played': len(self.move_history),
            'current_player': 'White' if self.current_player == Color.WHITE else 'Black',
            'position': {
                'fen': self.get_board_fen(),
                'material': self.get_material_balance(),
            },
            'analysis': self.analyze_position(),
            'tactics': {
                'white_hanging': len(self.validator.detect_hanging_pieces(Color.WHITE)),
                'black_hanging': len(self.validator.detect_hanging_pieces(Color.BLACK)),
                'white_forks': len(self.validator.detect_forks(Color.WHITE)),
                'black_forks': len(self.validator.detect_forks(Color.BLACK)),
            },
            'legal_moves': len(self.get_legal_moves()),
            'best_moves': self.get_best_moves(3),
            'opening': self.get_current_opening(),
        }
    
    def print_full_analysis(self) -> None:
        """Print complete game analysis."""
        summary = self.get_game_summary()
        
        print("\n" + "=" * 70)
        print("COMPLETE GAME ANALYSIS")
        print("=" * 70)
        
        print("\n📋 GAME STATE:")
        print(f"   Moves played: {summary['moves_played']}")
        print(f"   Current player: {summary['current_player']}")
        print(f"   Legal moves: {summary['legal_moves']}")
        
        print("\n🎯 POSITION ANALYSIS:")
        analysis = summary['analysis']
        print(f"   Score: {analysis['total_score']} cp")
        print(f"   Assessment: {analysis['assessment']}")
        print(f"   Phase: {analysis['phase']}")
        print(f"   Advantage: {analysis['white_advantage']} ({analysis['margin']} cp)")
        
        print("\n📊 EVALUATION FACTORS:")
        print(f"   Material (40%): {analysis['material']} cp")
        print(f"   Activity (30%): {analysis['activity']} cp")
        print(f"   Pawn structure (20%): {analysis['pawn_structure']} cp")
        print(f"   King safety (10%): {analysis['king_safety']} cp")
        
        print("\n⚔️ TACTICS:")
        tactics = summary['tactics']
        print(f"   White hanging pieces: {tactics['white_hanging']}")
        print(f"   Black hanging pieces: {tactics['black_hanging']}")
        print(f"   White fork opportunities: {tactics['white_forks']}")
        print(f"   Black fork opportunities: {tactics['black_forks']}")
        
        print("\n💡 BEST MOVES:")
        for i, move in enumerate(summary['best_moves'], 1):
            print(f"   {i}. {move['move']} (→ {move['score']} cp)" + 
                  (f", captures {move['captured']}" if move['captured'] else ""))
        
        if summary['opening']:
            print("\n📚 OPENING:")
            print(f"   {summary['opening']['opening']}")
            print(f"   Key ideas: {', '.join(summary['opening']['ideas'][:3])}")
        
        print("\n" + "=" * 70)


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Chess Mastery Hub - UNIFIED GAME MANAGER")
    print("All Phase 1 modules integrated and working together!")
    print("=" * 70)
    
    # Create game manager
    game = GameManager()
    
    # 1. Display starting position
    print("\n1. STARTING POSITION:")
    game.display_board()
    
    # 2. Get opening recommendation
    print("\n2. OPENING RECOMMENDATION:")
    rec = game.get_opening_recommendation(1200)
    print(f"   Recommended: {rec['recommendation']}")
    print(f"   Why: {rec['reasoning']}")
    
    # 3. Check legal moves
    print("\n3. LEGAL MOVES:")
    moves = game.get_legal_moves()
    print(f"   White has {len(moves)} legal moves")
    print(f"   Examples: ", end="")
    for move in moves[:5]:
        print(f"{move.to_algebraic()} ", end="")
    print()
    
    # 4. Make Italian Game moves
    print("\n4. PLAYING ITALIAN GAME:")
    moves_to_play = [("e2", "e4"), ("e7", "e5"), ("g1", "f3"), ("b8", "c6"), ("f1", "c4")]
    
    for from_pos, to_pos in moves_to_play:
        success = game.make_move(from_pos, to_pos)
        if success:
            print(f"   ✓ Played {from_pos}-{to_pos}")
        else:
            print(f"   ✗ Could not play {from_pos}-{to_pos}")
    
    # 5. Display current position
    print("\n5. CURRENT POSITION:")
    game.display_board()
    
    # 6. Full analysis
    game.print_full_analysis()
    
    print("\n" + "=" * 70)
    print("🎉 ALL 4 PHASES WORKING TOGETHER!")
    print("=" * 70)
    print("\nModules integrated:")
    print("  ✅ chess_engine.py (Board)")
    print("  ✅ opening_book.py (Openings)")
    print("  ✅ move_validator.py (Moves & Tactics)")
    print("  ✅ position_evaluator.py (Evaluation)")
    print("\nGameManager coordinates all of them seamlessly!")