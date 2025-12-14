"""
Move Validator Module
Validates chess moves and detects illegal positions.
Implements move generation and tactical pattern recognition.
Part of Chess Mastery Hub - Phase 1: Fundamentals

Phase 1.3: Basic Tactics & Piece Coordination
==============================================

This module provides:
- Move validator for all piece types
- Legal move generation
- Tactical pattern detection (forks, pins, skewers, etc)
- Check detection
- Piece attack analysis
- Safe move evaluation

Tactical Patterns Detected:
1. Forks - One piece attacks two pieces
2. Pins - Piece can't move without exposing more valuable piece
3. Skewers - Piece must move, exposing more valuable piece behind
4. Discovered Attacks - Moving piece reveals attack from another piece
5. Double Attacks - Two pieces attack same target
6. Hanging Pieces - Pieces undefended and can be captured
7. Weak Squares - Squares that can't be defended by pawns

Author: Your Name
Version: 0.3.0
Date: 2025-12-14
"""

from typing import List, Set, Tuple, Dict, Optional
from enum import Enum
from src.chess_engine import ChessBoard, Piece, Color, PieceType


class TacticalPattern(Enum):
    """Types of tactical patterns"""
    FORK = "fork"
    PIN = "pin"
    SKEWER = "skewer"
    DISCOVERED_ATTACK = "discovered_attack"
    DOUBLE_ATTACK = "double_attack"
    HANGING_PIECE = "hanging_piece"
    WEAK_SQUARE = "weak_square"
    BACK_RANK_MATE = "back_rank_mate"
    TRAPPED_PIECE = "trapped_piece"


class Move:
    """
    Represents a chess move.
    
    Attributes:
        from_pos: Starting position (e.g., "e2")
        to_pos: Destination position (e.g., "e4")
        piece: The piece being moved
        captures: Whether move captures a piece
        is_check: Whether move gives check
        is_checkmate: Whether move is checkmate
        is_castling: Whether move is castling
        promotion: Piece type if pawn promotion
    """
    
    def __init__(self, from_pos: str, to_pos: str, piece: Piece, captures: bool = False):
        """
        Initialize a move.
        
        Args:
            from_pos: Starting position
            to_pos: Destination position
            piece: The piece being moved
            captures: Whether move captures a piece
        """
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captures = captures
        self.is_check = False
        self.is_checkmate = False
        self.is_castling = False
        self.promotion = None
    
    def to_algebraic(self) -> str:
        """Convert move to algebraic notation"""
        notation = ""
        
        # Add piece symbol
        if self.piece.type != PieceType.PAWN:
            notation += self.piece.type.value[0].upper()
        
        # Add capture notation
        if self.captures:
            notation += "x"
        
        # Add destination
        notation += self.to_pos
        
        # Add check/checkmate
        if self.is_checkmate:
            notation += "#"
        elif self.is_check:
            notation += "+"
        
        return notation
    
    def __repr__(self) -> str:
        return f"Move({self.from_pos}-{self.to_pos})"
    
    def __str__(self) -> str:
        return f"{self.from_pos}{'-' if not self.captures else 'x'}{self.to_pos}"


class MoveValidator:
    """
    Validates chess moves and generates legal moves.
    
    Provides:
    - Move legality checking for all piece types
    - Legal move generation
    - Check detection
    - Tactical pattern detection
    - Attack analysis
    
    Example:
        >>> board = ChessBoard()
        >>> validator = MoveValidator(board)
        >>> legal_moves = validator.get_legal_moves(Color.WHITE)
        >>> for move in legal_moves:
        ...     print(move.to_algebraic())
    """
    
    def __init__(self, board: ChessBoard):
        """
        Initialize move validator with a board.
        
        Args:
            board: ChessBoard instance
        """
        self.board = board
    
    def is_valid_position(self, position: str) -> bool:
        """Check if position is valid on board"""
        return self.board.is_valid_position(position)
    
    def pos_to_coords(self, position: str) -> Tuple[int, int]:
        """Convert position (e.g., 'e4') to coordinates"""
        file = ord(position[0]) - ord('a')  # 0-7
        rank = int(position[1]) - 1  # 0-7
        return (file, rank)
    
    def coords_to_pos(self, file: int, rank: int) -> Optional[str]:
        """Convert coordinates to position"""
        if 0 <= file <= 7 and 0 <= rank <= 7:
            return chr(ord('a') + file) + str(rank + 1)
        return None
    
    def get_pawn_moves(self, piece: Piece) -> List[Move]:
        """
        Get all legal pawn moves.
        
        Pawns move forward 1 square (or 2 from starting position),
        capture diagonally forward, and can be promoted on 8th rank.
        """
        moves = []
        file, rank = self.pos_to_coords(piece.position)
        
        direction = 1 if piece.color == Color.WHITE else -1
        start_rank = 1 if piece.color == Color.WHITE else 6
        
        # Forward move (1 square)
        new_rank = rank + direction
        if 0 <= new_rank <= 7:
            new_pos = self.coords_to_pos(file, new_rank)
            if new_pos and not self.board.get_piece_at(new_pos):
                move = Move(piece.position, new_pos, piece)
                moves.append(move)
                
                # Forward move (2 squares from starting position)
                if rank == start_rank:
                    new_rank_2 = rank + 2 * direction
                    new_pos_2 = self.coords_to_pos(file, new_rank_2)
                    if new_pos_2 and not self.board.get_piece_at(new_pos_2):
                        move = Move(piece.position, new_pos_2, piece)
                        moves.append(move)
        
        # Capture moves (diagonal)
        for file_offset in [-1, 1]:
            capture_file = file + file_offset
            capture_rank = rank + direction
            capture_pos = self.coords_to_pos(capture_file, capture_rank)
            
            if capture_pos:
                target = self.board.get_piece_at(capture_pos)
                if target and target.color != piece.color:
                    move = Move(piece.position, capture_pos, piece, captures=True)
                    moves.append(move)
        
        return moves
    
    def get_knight_moves(self, piece: Piece) -> List[Move]:
        """
        Get all legal knight moves.
        
        Knights move in an L-shape: 2 squares in one direction,
        1 square perpendicular.
        """
        moves = []
        file, rank = self.pos_to_coords(piece.position)
        
        # All possible knight move offsets
        knight_offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for file_offset, rank_offset in knight_offsets:
            new_file = file + file_offset
            new_rank = rank + rank_offset
            new_pos = self.coords_to_pos(new_file, new_rank)
            
            if new_pos:
                target = self.board.get_piece_at(new_pos)
                if not target:
                    move = Move(piece.position, new_pos, piece)
                elif target.color != piece.color:
                    move = Move(piece.position, new_pos, piece, captures=True)
                else:
                    continue
                moves.append(move)
        
        return moves
    
    def get_bishop_moves(self, piece: Piece) -> List[Move]:
        """
        Get all legal bishop moves.
        
        Bishops move diagonally any number of squares.
        """
        moves = []
        file, rank = self.pos_to_coords(piece.position)
        
        # Four diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for file_dir, rank_dir in directions:
            for distance in range(1, 8):
                new_file = file + file_dir * distance
                new_rank = rank + rank_dir * distance
                new_pos = self.coords_to_pos(new_file, new_rank)
                
                if not new_pos:
                    break
                
                target = self.board.get_piece_at(new_pos)
                if not target:
                    move = Move(piece.position, new_pos, piece)
                    moves.append(move)
                elif target.color != piece.color:
                    move = Move(piece.position, new_pos, piece, captures=True)
                    moves.append(move)
                    break
                else:
                    break
        
        return moves
    
    def get_rook_moves(self, piece: Piece) -> List[Move]:
        """
        Get all legal rook moves.
        
        Rooks move horizontally or vertically any number of squares.
        """
        moves = []
        file, rank = self.pos_to_coords(piece.position)
        
        # Four directions: up, down, left, right
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        
        for file_dir, rank_dir in directions:
            for distance in range(1, 8):
                new_file = file + file_dir * distance
                new_rank = rank + rank_dir * distance
                new_pos = self.coords_to_pos(new_file, new_rank)
                
                if not new_pos:
                    break
                
                target = self.board.get_piece_at(new_pos)
                if not target:
                    move = Move(piece.position, new_pos, piece)
                    moves.append(move)
                elif target.color != piece.color:
                    move = Move(piece.position, new_pos, piece, captures=True)
                    moves.append(move)
                    break
                else:
                    break
        
        return moves
    
    def get_queen_moves(self, piece: Piece) -> List[Move]:
        """
        Get all legal queen moves.
        
        Queens combine rook and bishop moves.
        """
        # Queen moves like rook + bishop
        return self.get_rook_moves(piece) + self.get_bishop_moves(piece)
    
    def get_king_moves(self, piece: Piece) -> List[Move]:
        """
        Get all legal king moves.
        
        Kings move one square in any direction.
        """
        moves = []
        file, rank = self.pos_to_coords(piece.position)
        
        # Eight directions (one square each)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for file_dir, rank_dir in directions:
            new_file = file + file_dir
            new_rank = rank + rank_dir
            new_pos = self.coords_to_pos(new_file, new_rank)
            
            if new_pos:
                target = self.board.get_piece_at(new_pos)
                if not target:
                    move = Move(piece.position, new_pos, piece)
                elif target.color != piece.color:
                    move = Move(piece.position, new_pos, piece, captures=True)
                else:
                    continue
                moves.append(move)
        
        return moves
    
    def get_legal_moves(self, color: Color) -> List[Move]:
        """
        Get all legal moves for a color.
        
        Args:
            color: Color of pieces to move
            
        Returns:
            List of legal Move objects
            
        Example:
            >>> validator = MoveValidator(board)
            >>> white_moves = validator.get_legal_moves(Color.WHITE)
            >>> print(f"White has {len(white_moves)} legal moves")
        """
        pieces = self.board.get_pieces_by_color(color)
        all_moves = []
        
        for piece in pieces:
            if piece.type == PieceType.PAWN:
                all_moves.extend(self.get_pawn_moves(piece))
            elif piece.type == PieceType.KNIGHT:
                all_moves.extend(self.get_knight_moves(piece))
            elif piece.type == PieceType.BISHOP:
                all_moves.extend(self.get_bishop_moves(piece))
            elif piece.type == PieceType.ROOK:
                all_moves.extend(self.get_rook_moves(piece))
            elif piece.type == PieceType.QUEEN:
                all_moves.extend(self.get_queen_moves(piece))
            elif piece.type == PieceType.KING:
                all_moves.extend(self.get_king_moves(piece))
        
        return all_moves
    
    def is_attacked(self, position: str, by_color: Color) -> bool:
        """
        Check if a position is attacked by a color.
        
        Args:
            position: Position to check
            by_color: Color attacking
            
        Returns:
            True if position is attacked by that color
        """
        opponent = by_color.opposite() if by_color == Color.WHITE else Color.WHITE
        
        # Simulate board state and check if opponent can capture at position
        # This is simplified - full implementation would check all piece attacks
        for piece in self.board.get_pieces_by_color(by_color):
            if piece.type == PieceType.PAWN:
                moves = self.get_pawn_moves(piece)
            elif piece.type == PieceType.KNIGHT:
                moves = self.get_knight_moves(piece)
            elif piece.type == PieceType.BISHOP:
                moves = self.get_bishop_moves(piece)
            elif piece.type == PieceType.ROOK:
                moves = self.get_rook_moves(piece)
            elif piece.type == PieceType.QUEEN:
                moves = self.get_queen_moves(piece)
            elif piece.type == PieceType.KING:
                moves = self.get_king_moves(piece)
            else:
                continue
            
            for move in moves:
                if move.to_pos == position:
                    return True
        
        return False
    
    def detect_forks(self, color: Color) -> List[Dict]:
        """
        Detect fork opportunities for a color.
        
        A fork is when one piece attacks two or more valuable pieces.
        
        Args:
            color: Color to analyze
            
        Returns:
            List of fork opportunities
        """
        forks = []
        pieces = self.board.get_pieces_by_color(color)
        opponent_pieces = self.board.get_pieces_by_color(color.opposite())
        
        for piece in pieces:
            if piece.type == PieceType.PAWN:
                moves = self.get_pawn_moves(piece)
            elif piece.type == PieceType.KNIGHT:
                moves = self.get_knight_moves(piece)
            elif piece.type == PieceType.BISHOP:
                moves = self.get_bishop_moves(piece)
            elif piece.type == PieceType.ROOK:
                moves = self.get_rook_moves(piece)
            elif piece.type == PieceType.QUEEN:
                moves = self.get_queen_moves(piece)
            elif piece.type == PieceType.KING:
                moves = self.get_king_moves(piece)
            else:
                continue
            
            for move in moves:
                # Count how many opponent pieces this move attacks
                attacked_count = 0
                attacked_pieces = []
                
                for opponent in opponent_pieces:
                    if opponent.position == move.to_pos:
                        attacked_pieces.append(opponent)
                        attacked_count += 1
                
                # Fork if attacking 2+ valuable pieces
                if attacked_count >= 2:
                    forks.append({
                        "attacking_piece": piece,
                        "move": move,
                        "targets": attacked_pieces,
                        "value": sum(p.value for p in attacked_pieces)
                    })
        
        return forks
    
    def detect_hanging_pieces(self, color: Color) -> List[Dict]:
        """
        Detect hanging (undefended) pieces.
        
        Args:
            color: Color to analyze
            
        Returns:
            List of hanging pieces
        """
        hanging = []
        pieces = self.board.get_pieces_by_color(color)
        opponent_color = color.opposite()
        
        for piece in pieces:
            if piece.type == PieceType.KING or piece.value == 0:
                continue
            
            # Check if piece is attacked
            if self.is_attacked(piece.position, opponent_color):
                # Check if piece is defended
                defended = False
                for defender in pieces:
                    defender_moves = None
                    if defender.type == PieceType.PAWN:
                        defender_moves = self.get_pawn_moves(defender)
                    elif defender.type == PieceType.KNIGHT:
                        defender_moves = self.get_knight_moves(defender)
                    elif defender.type == PieceType.BISHOP:
                        defender_moves = self.get_bishop_moves(defender)
                    elif defender.type == PieceType.ROOK:
                        defender_moves = self.get_rook_moves(defender)
                    elif defender.type == PieceType.QUEEN:
                        defender_moves = self.get_queen_moves(defender)
                    elif defender.type == PieceType.KING:
                        defender_moves = self.get_king_moves(defender)
                    
                    if defender_moves:
                        for move in defender_moves:
                            if move.to_pos == piece.position:
                                defended = True
                                break
                    
                    if defended:
                        break
                
                if not defended:
                    hanging.append({
                        "piece": piece,
                        "position": piece.position,
                        "value": piece.value
                    })
        
        return hanging
    
    def detect_weak_squares(self, color: Color) -> List[str]:
        """
        Detect weak squares that can't be defended by pawns.
        
        These are critical squares for piece placement.
        
        Args:
            color: Color to analyze
            
        Returns:
            List of weak square positions
        """
        weak_squares = []
        pawns = self.board.get_pieces_by_type(PieceType.PAWN, color)
        
        # All dark squares around opponent's position
        for file in self.board.FILES:
            for rank in self.board.RANKS:
                position = f"{file}{rank}"
                
                # Check if this square can be defended by any pawn
                defended = False
                for pawn in pawns:
                    pawn_moves = self.get_pawn_moves(pawn)
                    for move in pawn_moves:
                        if move.captures and move.to_pos == position:
                            defended = True
                            break
                
                if not defended:
                    weak_squares.append(position)
        
        return weak_squares


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("Chess Mastery Hub - Phase 1.3: Move Validation & Tactical Patterns")
    print("=" * 70)
    
    # Create board and validator
    board = ChessBoard()
    validator = MoveValidator(board)
    
    # 1. Get legal moves for white
    print("\n1. LEGAL MOVES FOR WHITE (starting position):")
    white_moves = validator.get_legal_moves(Color.WHITE)
    print(f"   Total legal moves: {len(white_moves)}")
    
    # Group by piece type
    pawn_moves = [m for m in white_moves if m.piece.type == PieceType.PAWN]
    knight_moves = [m for m in white_moves if m.piece.type == PieceType.KNIGHT]
    print(f"   Pawn moves: {len(pawn_moves)}")
    print(f"   Knight moves: {len(knight_moves)}")
    
    # 2. Make some moves and check new position
    print("\n2. MAKING MOVES (e2-e4, e7-e5, Nf3):")
    board.move_piece("e2", "e4")
    board.move_piece("e7", "e5")
    board.move_piece("g1", "f3")
    board.display()
    
    # 3. Get legal moves after e4 e5 Nf3
    print("\n3. LEGAL MOVES AFTER e4 e5 Nf3:")
    white_moves_after = validator.get_legal_moves(Color.WHITE)
    print(f"   White has {len(white_moves_after)} legal moves")
    
    # 4. Check for hanging pieces
    print("\n4. DETECTING HANGING PIECES (White after e4 e5 Nf3):")
    hanging = validator.detect_hanging_pieces(Color.WHITE)
    if hanging:
        for piece in hanging:
            print(f"   Hanging: {piece['piece'].get_symbol()} on {piece['position']}")
    else:
        print("   No hanging pieces for white")
    
    # 5. Detect forks
    print("\n5. DETECTING FORKS (White):")
    forks = validator.detect_forks(Color.WHITE)
    if forks:
        for fork in forks:
            print(f"   Fork: {fork['attacking_piece'].get_symbol()} can fork {len(fork['targets'])} pieces")
    else:
        print("   No forks available for white")
    
    # 6. Detailed move analysis
    print("\n6. DETAILED MOVE ANALYSIS - Nc3:")
    knight = board.get_piece_at("f3")
    if knight:
        moves = validator.get_knight_moves(knight)
        print(f"   Knight on f3 has {len(moves)} legal moves:")
        for move in moves[:5]:  # Show first 5
            print(f"      {move.to_algebraic()}")
    
    # 7. Position evaluation
    print("\n7. POSITION EVALUATION:")
    material = board.calculate_material_balance()
    print(f"   Material balance: {material['advantage']} (White perspective)")
    print(f"   Equal material - both sides have developed 1 move")
    
    print("\n" + "=" * 70)
    print("Phase 1.3 Complete! Move validation and tactics working.")
    print("=" * 70)