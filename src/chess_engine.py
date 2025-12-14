"""
Chess Engine Core Module
Implements the chess board, pieces, and basic move validation.
Part of Chess Mastery Hub - Phase 1: Fundamentals

Phase 1.1: Piece Movement & Board Representation
================================================

This module provides:
- Color and PieceType enums for type safety
- Piece class hierarchy with unicode symbols
- ChessBoard class with standard starting position
- Board display and piece lookup
- Material calculation for position evaluation

Author: Your Name
Version: 0.1.0
Date: 2025-12-14
"""

from enum import Enum
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass


class Color(Enum):
    """Represents the color of a chess piece"""
    WHITE = "white"
    BLACK = "black"
    
    def opposite(self) -> 'Color':
        """Returns the opposite color"""
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class PieceType(Enum):
    """Represents the type of chess piece"""
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class Piece:
    """
    Represents a single chess piece.
    
    Attributes:
        type: PieceType (PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING)
        color: Color (WHITE or BLACK)
        position: str (e.g., "e4" in algebraic notation)
        value: int (material value in centipawns)
        
    Example:
        >>> white_pawn = Piece(PieceType.PAWN, Color.WHITE, "e2")
        >>> print(white_pawn.get_symbol())
        ♙
        >>> white_pawn.value
        1
    """
    
    # Standard piece values (in points, multiply by 100 for centipawns)
    PIECE_VALUES = {
        PieceType.PAWN: 1,
        PieceType.KNIGHT: 3,
        PieceType.BISHOP: 3,
        PieceType.ROOK: 5,
        PieceType.QUEEN: 9,
        PieceType.KING: 0  # King cannot be captured, so no value
    }
    
    # Unicode chess piece symbols
    SYMBOLS = {
        (PieceType.PAWN, Color.WHITE): "♙",
        (PieceType.PAWN, Color.BLACK): "♟",
        (PieceType.KNIGHT, Color.WHITE): "♘",
        (PieceType.KNIGHT, Color.BLACK): "♞",
        (PieceType.BISHOP, Color.WHITE): "♗",
        (PieceType.BISHOP, Color.BLACK): "♝",
        (PieceType.ROOK, Color.WHITE): "♖",
        (PieceType.ROOK, Color.BLACK): "♜",
        (PieceType.QUEEN, Color.WHITE): "♕",
        (PieceType.QUEEN, Color.BLACK): "♛",
        (PieceType.KING, Color.WHITE): "♔",
        (PieceType.KING, Color.BLACK): "♚",
    }
    
    def __init__(self, piece_type: PieceType, color: Color, position: str):
        """
        Initialize a chess piece.
        
        Args:
            piece_type: Type of piece (PieceType enum)
            color: Color of piece (Color enum)
            position: Position in algebraic notation (e.g., "e4")
        """
        self.type = piece_type
        self.color = color
        self.position = position
        self.value = self.PIECE_VALUES[piece_type]
        self.move_count = 0  # Track moves for castling rights
    
    def get_symbol(self) -> str:
        """
        Returns the unicode chess piece symbol.
        
        Returns:
            str: Unicode character representing the piece
            
        Example:
            >>> piece = Piece(PieceType.QUEEN, Color.WHITE, "d1")
            >>> piece.get_symbol()
            '♕'
        """
        return self.SYMBOLS.get((self.type, self.color), "?")
    
    def __repr__(self) -> str:
        """String representation of piece"""
        return f"{self.get_symbol()} {self.color.value} {self.type.value} on {self.position}"
    
    def __str__(self) -> str:
        """Human readable representation"""
        return f"{self.color.value.upper()} {self.type.value.upper()} on {self.position}"


class ChessBoard:
    """
    Represents the chess board and manages game state.
    
    The board uses algebraic notation:
    - Files (columns): a-h (left to right)
    - Ranks (rows): 1-8 (bottom to top from white's perspective)
    - Positions: combination of file and rank (e.g., "e4")
    
    Attributes:
        pieces: List of Piece objects on the board
        move_history: List of moves in algebraic notation
        white_king_moved: Whether white king has moved (for castling)
        black_king_moved: Whether black king has moved (for castling)
        
    Example:
        >>> board = ChessBoard()
        >>> board.display()
        >>> material = board.calculate_material_balance()
        >>> print(f"Material balance: {material['advantage']} (White perspective)")
    """
    
    # Board coordinates
    FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']
    
    def __init__(self):
        """Initialize the chess board with starting position"""
        self.pieces: List[Piece] = []
        self.move_history: List[str] = []
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_a1_moved = False
        self.white_rook_h1_moved = False
        self.black_rook_a8_moved = False
        self.black_rook_h8_moved = False
        self.setup_starting_position()
    
    def setup_starting_position(self) -> None:
        """
        Initialize board with the standard chess starting position.
        
        Position:
            8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
            7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
            6 . . . . . . . .
            5 . . . . . . . .
            4 . . . . . . . .
            3 . . . . . . . .
            2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
            1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
              a b c d e f g h
        """
        self.pieces = []
        
        # White pawns on rank 2
        for file in self.FILES:
            self.pieces.append(Piece(PieceType.PAWN, Color.WHITE, f"{file}2"))
        
        # White back rank (rank 1)
        self.pieces.append(Piece(PieceType.ROOK, Color.WHITE, "a1"))
        self.pieces.append(Piece(PieceType.KNIGHT, Color.WHITE, "b1"))
        self.pieces.append(Piece(PieceType.BISHOP, Color.WHITE, "c1"))
        self.pieces.append(Piece(PieceType.QUEEN, Color.WHITE, "d1"))
        self.pieces.append(Piece(PieceType.KING, Color.WHITE, "e1"))
        self.pieces.append(Piece(PieceType.BISHOP, Color.WHITE, "f1"))
        self.pieces.append(Piece(PieceType.KNIGHT, Color.WHITE, "g1"))
        self.pieces.append(Piece(PieceType.ROOK, Color.WHITE, "h1"))
        
        # Black pawns on rank 7
        for file in self.FILES:
            self.pieces.append(Piece(PieceType.PAWN, Color.BLACK, f"{file}7"))
        
        # Black back rank (rank 8)
        self.pieces.append(Piece(PieceType.ROOK, Color.BLACK, "a8"))
        self.pieces.append(Piece(PieceType.KNIGHT, Color.BLACK, "b8"))
        self.pieces.append(Piece(PieceType.BISHOP, Color.BLACK, "c8"))
        self.pieces.append(Piece(PieceType.QUEEN, Color.BLACK, "d8"))
        self.pieces.append(Piece(PieceType.KING, Color.BLACK, "e8"))
        self.pieces.append(Piece(PieceType.BISHOP, Color.BLACK, "f8"))
        self.pieces.append(Piece(PieceType.KNIGHT, Color.BLACK, "g8"))
        self.pieces.append(Piece(PieceType.ROOK, Color.BLACK, "h8"))
    
    def get_piece_at(self, position: str) -> Optional[Piece]:
        """
        Get the piece at a specific position.
        
        Args:
            position: Position in algebraic notation (e.g., "e4")
            
        Returns:
            Piece object if piece exists at position, None otherwise
            
        Example:
            >>> board = ChessBoard()
            >>> piece = board.get_piece_at("e2")
            >>> print(piece.get_symbol())
            ♙
        """
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None
    
    def get_pieces_by_color(self, color: Color) -> List[Piece]:
        """
        Get all pieces of a specific color.
        
        Args:
            color: Color to filter by (Color enum)
            
        Returns:
            List of Piece objects of that color
            
        Example:
            >>> board = ChessBoard()
            >>> white_pieces = board.get_pieces_by_color(Color.WHITE)
            >>> len(white_pieces)
            16
        """
        return [p for p in self.pieces if p.color == color]
    
    def get_pieces_by_type(self, piece_type: PieceType, color: Optional[Color] = None) -> List[Piece]:
        """
        Get all pieces of a specific type.
        
        Args:
            piece_type: Type of piece to filter by (PieceType enum)
            color: Optional color filter (Color enum)
            
        Returns:
            List of Piece objects matching criteria
            
        Example:
            >>> board = ChessBoard()
            >>> white_knights = board.get_pieces_by_type(PieceType.KNIGHT, Color.WHITE)
            >>> len(white_knights)
            2
        """
        if color:
            return [p for p in self.pieces if p.type == piece_type and p.color == color]
        return [p for p in self.pieces if p.type == piece_type]
    
    def display(self) -> None:
        """
        Print ASCII representation of the chess board.
        
        Shows board from white's perspective (rank 1 at bottom).
        Uses unicode chess symbols.
        
        Example:
            >>> board = ChessBoard()
            >>> board.display()
              a  b  c  d  e f  g  h
            8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
            7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
            6 .  .  .  .  .  . .  .
            5 .  .  .  .  .  . .  .
            4 .  .  .  .  .  . .  .
            3 .  .  .  .  .  . .  .
            2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
            1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
              a  b  c  d  e f  g  h
        """
        print("\n  a b c d e f g h")
        print("  +-+-+-+-+-+-+-+")
        
        # Display from rank 8 down to 1 (white's perspective)
        for rank in reversed(self.RANKS):
            row = f"{rank}|"
            for file in self.FILES:
                piece = self.get_piece_at(f"{file}{rank}")
                if piece:
                    row += piece.get_symbol() + "|"
                else:
                    row += " |"
            print(row)
            print("  +-+-+-+-+-+-+-+")
        
        print("  a b c d e f g h\n")
    
    def calculate_material_balance(self) -> Dict[str, any]:
        """
        Calculate material balance from white's perspective.
        
        Returns a dictionary with:
            - white: Total white material value (points)
            - black: Total black material value (points)
            - advantage: Difference (positive = white ahead, negative = black ahead)
            - advantage_side: Which side is ahead ("white" or "black" or "equal")
            
        Returns:
            dict: Material balance information
            
        Example:
            >>> board = ChessBoard()
            >>> balance = board.calculate_material_balance()
            >>> print(f"White: {balance['white']} points")
            >>> print(f"Black: {balance['black']} points")
            >>> print(f"Balance: {balance['advantage']} (White perspective)")
        """
        white_material = sum(
            p.value for p in self.pieces if p.color == Color.WHITE
        )
        black_material = sum(
            p.value for p in self.pieces if p.color == Color.BLACK
        )
        
        advantage = white_material - black_material
        
        if advantage > 0:
            advantage_side = "white"
        elif advantage < 0:
            advantage_side = "black"
        else:
            advantage_side = "equal"
        
        return {
            "white": white_material,
            "black": black_material,
            "advantage": advantage,
            "advantage_side": advantage_side,
            "centipawns": advantage * 100  # Convert to centipawns for evaluation
        }
    
    def get_position_fen(self) -> str:
        """
        Get simplified FEN representation of position.
        
        Note: This is a simplified FEN that shows piece placement only.
        Full FEN also includes castling rights, en passant, move counts, etc.
        
        Returns:
            str: FEN string representation
            
        Example:
            >>> board = ChessBoard()
            >>> print(board.get_position_fen())
            rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
        """
        fen_rows = []
        
        for rank in reversed(self.RANKS):
            fen_row = ""
            empty_count = 0
            
            for file in self.FILES:
                piece = self.get_piece_at(f"{file}{rank}")
                if piece:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    # Add piece character (uppercase = white, lowercase = black)
                    piece_char = {
                        PieceType.PAWN: 'P',
                        PieceType.KNIGHT: 'N',
                        PieceType.BISHOP: 'B',
                        PieceType.ROOK: 'R',
                        PieceType.QUEEN: 'Q',
                        PieceType.KING: 'K',
                    }[piece.type]
                    
                    if piece.color == Color.BLACK:
                        piece_char = piece_char.lower()
                    
                    fen_row += piece_char
                else:
                    empty_count += 1
            
            if empty_count > 0:
                fen_row += str(empty_count)
            
            fen_rows.append(fen_row)
        
        return '/'.join(fen_rows)
    
    def move_piece(self, from_pos: str, to_pos: str) -> bool:
        """
        Move a piece from one position to another.
        
        Note: This is a basic move without validation.
        Phase 1.3 will add proper move validation.
        
        Args:
            from_pos: Starting position (e.g., "e2")
            to_pos: Destination position (e.g., "e4")
            
        Returns:
            bool: True if move was successful, False otherwise
            
        Example:
            >>> board = ChessBoard()
            >>> board.move_piece("e2", "e4")
            True
            >>> board.get_piece_at("e4").type
            <PieceType.PAWN: 'pawn'>
        """
        piece = self.get_piece_at(from_pos)
        if not piece:
            return False
        
        # Remove piece from destination if it exists (capture)
        target = self.get_piece_at(to_pos)
        if target:
            self.pieces.remove(target)
        
        # Move the piece
        piece.position = to_pos
        piece.move_count += 1
        
        # Record move in history
        self.move_history.append(f"{from_pos}-{to_pos}")
        
        return True
    
    def is_valid_position(self, position: str) -> bool:
        """
        Check if a position is valid on the board.
        
        Args:
            position: Position in algebraic notation
            
        Returns:
            bool: True if position is valid, False otherwise
        """
        if len(position) != 2:
            return False
        file, rank = position[0], position[1]
        return file in self.FILES and rank in self.RANKS
    
    def reset_board(self) -> None:
        """Reset the board to starting position"""
        self.pieces = []
        self.move_history = []
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_a1_moved = False
        self.white_rook_h1_moved = False
        self.black_rook_a8_moved = False
        self.black_rook_h8_moved = False
        self.setup_starting_position()


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Chess Mastery Hub - Phase 1.1: Board Representation")
    print("=" * 60)
    
    # Create a new board
    board = ChessBoard()
    
    # Display the starting position
    print("\n1. STARTING POSITION:")
    board.display()
    
    # Show material balance
    print("\n2. MATERIAL BALANCE (Starting Position):")
    balance = board.calculate_material_balance()
    print(f"   White material: {balance['white']} points")
    print(f"   Black material: {balance['black']} points")
    print(f"   Advantage: {balance['advantage']} ({balance['advantage_side'].upper()})")
    
    # Get pieces by color
    print("\n3. PIECE COUNT BY COLOR:")
    white_pieces = board.get_pieces_by_color(Color.WHITE)
    black_pieces = board.get_pieces_by_color(Color.BLACK)
    print(f"   White pieces: {len(white_pieces)}")
    print(f"   Black pieces: {len(black_pieces)}")
    
    # Get specific piece types
    print("\n4. SPECIFIC PIECE COUNTS:")
    white_pawns = board.get_pieces_by_type(PieceType.PAWN, Color.WHITE)
    white_knights = board.get_pieces_by_type(PieceType.KNIGHT, Color.WHITE)
    black_rooks = board.get_pieces_by_type(PieceType.ROOK, Color.BLACK)
    print(f"   White pawns: {len(white_pawns)}")
    print(f"   White knights: {len(white_knights)}")
    print(f"   Black rooks: {len(black_rooks)}")
    
    # Show piece details
    print("\n5. PIECE DETAILS:")
    e2_piece = board.get_piece_at("e2")
    print(f"   Piece at e2: {e2_piece}")
    print(f"   Symbol: {e2_piece.get_symbol()}")
    print(f"   Value: {e2_piece.value} points")
    
    # Make a move
    print("\n6. MAKING A MOVE (e2 to e4):")
    success = board.move_piece("e2", "e4")
    print(f"   Move successful: {success}")
    if success:
        print(f"   Piece at e4: {board.get_piece_at('e4')}")
        print(f"   Move history: {board.move_history}")
    
    # Display after move
    print("\n7. BOARD AFTER MOVE:")
    board.display()
    
    # Get FEN position
    print("\n8. FEN POSITION:")
    print(f"   {board.get_position_fen()}")
    
    print("\n" + "=" * 60)
    print("Phase 1.1 Complete! Board representation working.")
    print("=" * 60)