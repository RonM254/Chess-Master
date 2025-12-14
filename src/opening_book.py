"""
Opening Book Module
Stores and retrieves chess openings by move sequence.
Built with dictionaries for fast lookup and educational organization.
Part of Chess Mastery Hub - Phase 1: Fundamentals

Phase 1.2: Opening Principles & Common Openings
===============================================

This module provides:
- OpeningBook class with curated opening database
- 4 fundamental openings for 1200-rated players
- Opening lookup by name or initial moves
- Key ideas and principles for each opening
- Move sequences in algebraic notation
- Integration with ChessBoard for position analysis

Openings Included:
1. Italian Game (1.e4 e5 2.Nf3 Nc6 3.Bc4)
2. Ruy Lopez / Spanish Opening (1.e4 e5 2.Nf3 Nc6 3.Bb5)
3. French Defense (1.e4 e6)
4. Scandinavian Defense (1.e4 d5)

Author: Your Name
Version: 0.2.0
Date: 2025-12-14
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class OpeningDifficulty(Enum):
    """Difficulty level for openings"""
    BEGINNER = "1000-1200"
    INTERMEDIATE = "1200-1500"
    ADVANCED = "1500-1800"
    EXPERT = "1800+"


class OpeningType(Enum):
    """Type of opening based on first move"""
    OPEN_GAME = "1.e4 e5"  # Italian, Spanish, Scotch
    SEMI_OPEN = "1.e4 c5 / 1.e4 e6 / 1.e4 d5"  # Sicilian, French, Scandinavian
    CLOSED_GAME = "1.d4"  # Queen's Gambit, Slav, Indian
    SEMI_CLOSED = "1.c4 / 1.Nf3"  # English, Reti


class Opening:
    """
    Represents a single chess opening.
    
    Attributes:
        name: Name of the opening (str)
        moves: Move sequence in algebraic notation (str)
        fen: FEN position after main line (str)
        difficulty: Difficulty level (OpeningDifficulty)
        key_ideas: List of key strategic ideas (List[str])
        variations: Alternative continuations (Dict[str, str])
        tactics: Common tactical patterns in opening (List[str])
        target_elo_min: Minimum rating to study (int)
        target_elo_max: Maximum rating before advanced prep (int)
    """
    
    def __init__(
        self,
        name: str,
        moves: str,
        fen: str,
        difficulty: OpeningDifficulty,
        key_ideas: List[str],
        variations: Dict[str, str] = None,
        tactics: List[str] = None,
        target_elo_min: int = 1000,
        target_elo_max: int = 2000
    ):
        """
        Initialize an opening.
        
        Args:
            name: Opening name
            moves: Move sequence in algebraic notation
            fen: FEN position after main line
            difficulty: Difficulty level
            key_ideas: List of key strategic ideas
            variations: Optional alternative lines
            tactics: Optional common tactical patterns
            target_elo_min: Minimum rating (default 1000)
            target_elo_max: Maximum rating (default 2000)
        """
        self.name = name
        self.moves = moves
        self.fen = fen
        self.difficulty = difficulty
        self.key_ideas = key_ideas
        self.variations = variations or {}
        self.tactics = tactics or []
        self.target_elo_min = target_elo_min
        self.target_elo_max = target_elo_max
    
    def to_dict(self) -> Dict:
        """Convert opening to dictionary"""
        return {
            "name": self.name,
            "moves": self.moves,
            "fen": self.fen,
            "difficulty": self.difficulty.value,
            "key_ideas": self.key_ideas,
            "variations": self.variations,
            "tactics": self.tactics,
            "target_elo_min": self.target_elo_min,
            "target_elo_max": self.target_elo_max
        }
    
    def __repr__(self) -> str:
        return f"Opening({self.name})"
    
    def __str__(self) -> str:
        return f"{self.name}: {self.moves}"


class OpeningBook:
    """
    Chess opening database for 1200-rated players.
    
    Provides structured access to fundamental openings that will:
    - Improve positional understanding
    - Teach sound opening principles
    - Avoid memorizing too much theory
    - Focus on playable lines
    
    The openings are chosen to be:
    1. Easy to understand and remember
    2. Sound with excellent winning records
    3. Playable at all levels
    4. Relevant to intermediate players
    
    Example:
        >>> book = OpeningBook()
        >>> italian = book.get_opening_by_name("Italian Game")
        >>> print(italian.moves)
        1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.c3 Nf6 5.d4
        >>> ideas = book.get_opening_ideas("Italian Game")
        >>> for idea in ideas:
        ...     print(f"- {idea}")
    """
    
    def __init__(self):
        """Initialize the opening book with fundamental openings"""
        self.openings: Dict[str, Opening] = {}
        self._init_openings()
    
    def _init_openings(self) -> None:
        """Initialize all openings in the database"""
        
        # 1. ITALIAN GAME - Best first opening for 1200 players
        italian = Opening(
            name="Italian Game",
            moves="1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.c3 Nf6 5.d4",
            fen="r1bqk1nr/pppp1ppp/2n2n2/2b1p1B1/2BpP3/2P2N2/PP3PPP/RN1QK2R w KQkq - 0 5",
            difficulty=OpeningDifficulty.BEGINNER,
            key_ideas=[
                "Control center with e4 pawn",
                "Attack f7 square with Bc4",
                "Develop knights before bishops",
                "Prepare d4 advance",
                "Castle early for king safety",
                "Maintain piece coordination"
            ],
            variations={
                "Giuoco Piano": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.d3",
                "Two Knights Defense": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Nf6",
                "Fried Liver": "1.e4 e5 2.Nf3 Nc6 3.Bc4 Nf6 4.Ng5 d5 5.exd5 Na5"
            },
            tactics=[
                "Fork: Knight fork on d5/f6",
                "Pin: Bishop pins knight to king",
                "Skewer: Rook after castling",
                "Weak f7 square: Target throughout opening"
            ],
            target_elo_min=1000,
            target_elo_max=1800
        )
        self.openings["Italian Game"] = italian
        
        # 2. RUY LOPEZ (SPANISH OPENING) - Most popular opening
        spanish = Opening(
            name="Ruy Lopez / Spanish Opening",
            moves="1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.0-0 Be7 6.Re1",
            fen="r1bqk2r/pppp1ppp/2n2n2/4p3/B3P3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 0 6",
            difficulty=OpeningDifficulty.INTERMEDIATE,
            key_ideas=[
                "Pin knight to king with Bb5",
                "Flexible middlegame plans",
                "Exchange on c6 weakens pawn structure",
                "Maintain pressure on e5",
                "Support d4 break",
                "White has slight but long-term advantage"
            ],
            variations={
                "Open Defense": "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.0-0 Be7 6.Re1 b5 7.Bb3 d6",
                "Closed Defense": "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.0-0 Be7 6.Re1 b5 7.Bb3 0-0",
                "Berlin Defense": "1.e4 e5 2.Nf3 Nc6 3.Bb5 Nf6"
            },
            tactics=[
                "Pin on c6 knight",
                "Tactical blow with d5/d4",
                "Back rank tactics after castling",
                "X-ray tactics on e5 pawn"
            ],
            target_elo_min=1200,
            target_elo_max=2200
        )
        self.openings["Ruy Lopez"] = spanish
        self.openings["Spanish Opening"] = spanish  # Alias
        
        # 3. FRENCH DEFENSE - Solid, strategic
        french = Opening(
            name="French Defense",
            moves="1.e4 e6 2.d4 d5 3.Nc3 Nf6 4.Bg5 Be7 5.e5 Nfd7 6.Bxe7 Qxe7",
            fen="r1bqk1nr/ppppqppp/2n1p3/3pP3/3P4/2N2N2/PPP2PPP/R1BQKB1R w KQkq - 0 7",
            difficulty=OpeningDifficulty.INTERMEDIATE,
            key_ideas=[
                "Solid pawn structure (e6, d5)",
                "Black accepts space disadvantage",
                "Play for piece activity and counterattack",
                "f6-e5 pawn break is key plan",
                "Fianchetto bishop on a6 or g7",
                "Requires patience but very playable"
            ],
            variations={
                "Winawer Variation": "1.e4 e6 2.d4 d5 3.Nc3 Bb4",
                "Classical Variation": "1.e4 e6 2.d4 d5 3.Nc3 Nf6 4.Bg5 Be7",
                "Tarrasch Variation": "1.e4 e6 2.d4 d5 3.Nd2"
            },
            tactics=[
                "Knight fork on e4",
                "Pin on c6 knight",
                "Weak c6 square",
                "Counter-attack on white king"
            ],
            target_elo_min=1200,
            target_elo_max=2000
        )
        self.openings["French Defense"] = french
        
        # 4. SCANDINAVIAN DEFENSE - Fighting
        scandinavian = Opening(
            name="Scandinavian Defense",
            moves="1.e4 d5 2.exd5 Qxd5 3.Nc3 Qa5 4.d4 Nf6 5.Nf3 c6 6.Bc4 Bg4",
            fen="r1b1kbnr/pp1p1ppp/2p2n2/q7/2BPb3/2N2N2/PPP2PPP/R1BQK2R w KQkq - 0 7",
            difficulty=OpeningDifficulty.INTERMEDIATE,
            key_ideas=[
                "Immediate center confrontation",
                "Black gambits center for piece activity",
                "Queen actively placed on a5/d5",
                "White has space advantage",
                "Black has tactical opportunities",
                "Forcing, tactical chess"
            ],
            variations={
                "Main Line": "1.e4 d5 2.exd5 Qxd5 3.Nc3 Qa5 4.d4 Nf6",
                "Quiet Variation": "1.e4 d5 2.exd5 Qxd5 3.Nc3 Qd6",
                "Mieses Variation": "1.e4 d5 2.exd5 Qxd5 3.Nc3 Qd8"
            },
            tactics=[
                "Queen harassment tactics",
                "Central breaks with d4/c4",
                "Knight forks",
                "Pins and tactical shots"
            ],
            target_elo_min=1100,
            target_elo_max=1600
        )
        self.openings["Scandinavian Defense"] = scandinavian
    
    def get_opening_by_name(self, name: str) -> Optional[Opening]:
        """
        Get opening by exact name.
        
        Args:
            name: Opening name (e.g., "Italian Game")
            
        Returns:
            Opening object if found, None otherwise
            
        Example:
            >>> book = OpeningBook()
            >>> italian = book.get_opening_by_name("Italian Game")
            >>> print(italian.moves)
            1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.c3 Nf6 5.d4
        """
        return self.openings.get(name)
    
    def get_all_openings(self) -> Dict[str, Opening]:
        """
        Get all openings in the book.
        
        Returns:
            Dictionary of all openings
            
        Example:
            >>> book = OpeningBook()
            >>> all_openings = book.get_all_openings()
            >>> for name in all_openings:
            ...     print(name)
        """
        return self.openings.copy()
    
    def get_opening_names(self) -> List[str]:
        """
        Get list of all opening names.
        
        Returns:
            List of opening names
        """
        return list(self.openings.keys())
    
    def get_openings_by_difficulty(self, difficulty: OpeningDifficulty) -> List[Opening]:
        """
        Get all openings at a specific difficulty level.
        
        Args:
            difficulty: OpeningDifficulty enum value
            
        Returns:
            List of Opening objects at that difficulty
            
        Example:
            >>> book = OpeningBook()
            >>> beginner = book.get_openings_by_difficulty(OpeningDifficulty.BEGINNER)
            >>> for opening in beginner:
            ...     print(opening.name)
        """
        return [
            opening for opening in self.openings.values()
            if opening.difficulty == difficulty
        ]
    
    def get_openings_by_elo_range(self, elo: int) -> List[Opening]:
        """
        Get appropriate openings for a player's rating.
        
        Args:
            elo: Player's Elo rating (e.g., 1200)
            
        Returns:
            List of appropriate Opening objects
            
        Example:
            >>> book = OpeningBook()
            >>> appropriate = book.get_openings_by_elo_range(1200)
            >>> for opening in appropriate:
            ...     print(opening.name)
        """
        return [
            opening for opening in self.openings.values()
            if opening.target_elo_min <= elo <= opening.target_elo_max
        ]
    
    def get_opening_ideas(self, opening_name: str) -> Optional[List[str]]:
        """
        Get key ideas for an opening.
        
        Args:
            opening_name: Name of the opening
            
        Returns:
            List of key ideas or None if opening not found
            
        Example:
            >>> book = OpeningBook()
            >>> ideas = book.get_opening_ideas("Italian Game")
            >>> for idea in ideas:
            ...     print(f"- {idea}")
        """
        opening = self.get_opening_by_name(opening_name)
        if opening:
            return opening.key_ideas
        return None
    
    def get_opening_tactics(self, opening_name: str) -> Optional[List[str]]:
        """
        Get common tactical patterns in an opening.
        
        Args:
            opening_name: Name of the opening
            
        Returns:
            List of tactical patterns or None
        """
        opening = self.get_opening_by_name(opening_name)
        if opening:
            return opening.tactics
        return None
    
    def get_universal_principles(self) -> Dict[str, str]:
        """
        Get universal opening principles for all openings.
        
        These principles apply to ANY opening and are essential
        for 1200-rated players to master.
        
        Returns:
            Dictionary of principle names and descriptions
            
        Example:
            >>> book = OpeningBook()
            >>> principles = book.get_universal_principles()
            >>> for principle, description in principles.items():
            ...     print(f"{principle}: {description}")
        """
        return {
            "Control the Center": (
                "Place pawns on e4, d4, e5, d5. Control central squares with pieces. "
                "The center is the battlefield - whoever controls it controls the game."
            ),
            "Develop Pieces Rapidly": (
                "Move knights before bishops. Get all minor pieces out. Don't move same piece twice. "
                "Development advantage wins games at 1200+."
            ),
            "Castle Early": (
                "Castle by move 10-12. Gets king to safety. Connects rooks. "
                "Uncastled king in the center = checkmated king."
            ),
            "Piece Coordination": (
                "Pieces should support each other. Before attacking, make sure all pieces are connected. "
                "One piece against many pieces = lost piece."
            ),
            "Avoid Greed": (
                "Don't grab material that leaves your pieces hanging. Don't move same piece twice for pawn. "
                "Solid advantage > immediate material gain."
            ),
            "King Safety First": (
                "Protect the king above all else. Move king away from center early. "
                "A mated king loses everything - defend it!"
            ),
            "Pawn Structure": (
                "Avoid creating weaknesses. Don't push pawns without reason. "
                "Bad pawn structure = permanent positional disadvantage."
            ),
            "Piece Activity": (
                "Active pieces > material count. A rook on 7th rank > extra pawn. "
                "Create threats and keep attacking."
            )
        }
    
    def get_opening_recommendations(self, elo: int, experience: str = "beginner") -> Dict[str, str]:
        """
        Get personalized opening recommendations based on rating and experience.
        
        Args:
            elo: Player's Elo rating
            experience: "beginner", "intermediate", or "advanced"
            
        Returns:
            Dictionary with recommendation and reasoning
            
        Example:
            >>> book = OpeningBook()
            >>> rec = book.get_opening_recommendations(1200)
            >>> print(rec["recommendation"])
        """
        recommendations = {
            "beginner": {
                "recommendation": "Italian Game",
                "reasoning": (
                    "Simple, intuitive, sound. Attack f7, develop quickly, castle early. "
                    "No heavy theory. Great 60%+ winning record at all levels."
                ),
                "alternate": "Scandinavian Defense (for variety)"
            },
            "intermediate": {
                "recommendation": "Ruy Lopez",
                "reasoning": (
                    "Most popular opening ever. Slight edge but playable for both sides. "
                    "Teaches long-term positional understanding. Flexible middlegame plans."
                ),
                "alternate": "French Defense (for positional chess)"
            },
            "advanced": {
                "recommendation": "Mix all four",
                "reasoning": (
                    "Play different openings. Understand principles in many positions. "
                    "Flexible repertoire beats one boring opening."
                ),
                "alternate": "Study theory for specific variations"
            }
        }
        
        return recommendations.get(experience, recommendations["beginner"])
    
    def analyze_opening_fit(self, opening_name: str, elo: int) -> Dict[str, any]:
        """
        Analyze if an opening is appropriate for a player's rating.
        
        Args:
            opening_name: Name of opening to analyze
            elo: Player's Elo rating
            
        Returns:
            Dictionary with fit analysis
        """
        opening = self.get_opening_by_name(opening_name)
        if not opening:
            return {"fit": "OPENING_NOT_FOUND", "message": f"Opening '{opening_name}' not found"}
        
        if elo < opening.target_elo_min:
            fit = "TOO_ADVANCED"
            message = f"Study fundamentals first (target: {opening.target_elo_min}+ rating)"
        elif elo > opening.target_elo_max:
            fit = "TOO_SIMPLE"
            message = f"Consider more complex openings for your rating ({elo}+)"
        else:
            fit = "PERFECT_FIT"
            message = f"Ideal opening for {elo} rating"
        
        return {
            "opening": opening_name,
            "player_elo": elo,
            "fit": fit,
            "message": message,
            "target_range": f"{opening.target_elo_min}-{opening.target_elo_max}",
            "difficulty": opening.difficulty.value
        }


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("Chess Mastery Hub - Phase 1.2: Opening Principles & Common Openings")
    print("=" * 70)
    
    # Create opening book
    book = OpeningBook()
    
    # 1. Show all openings
    print("\n1. ALL OPENINGS IN THE BOOK:")
    for name in book.get_opening_names():
        opening = book.get_opening_by_name(name)
        print(f"   ✓ {name}: {opening.moves[:40]}...")
    
    # 2. Show openings by difficulty
    print("\n2. OPENINGS BY DIFFICULTY:")
    for difficulty in OpeningDifficulty:
        openings = book.get_openings_by_difficulty(difficulty)
        print(f"   {difficulty.value}: {len(openings)} opening(s)")
        for opening in openings:
            print(f"      - {opening.name}")
    
    # 3. Detailed opening analysis
    print("\n3. DETAILED ANALYSIS - ITALIAN GAME:")
    italian = book.get_opening_by_name("Italian Game")
    print(f"   Name: {italian.name}")
    print(f"   Moves: {italian.moves}")
    print(f"   Difficulty: {italian.difficulty.value}")
    print(f"   Key Ideas:")
    for i, idea in enumerate(italian.key_ideas, 1):
        print(f"      {i}. {idea}")
    print(f"   Common Tactics:")
    for i, tactic in enumerate(italian.tactics, 1):
        print(f"      {i}. {tactic}")
    print(f"   FEN: {italian.fen[:50]}...")
    
    # 4. Recommendations for player
    print("\n4. OPENING RECOMMENDATIONS FOR 1200-RATED PLAYER:")
    rec = book.get_opening_recommendations(1200)
    print(f"   Recommended: {rec['recommendation']}")
    print(f"   Why: {rec['reasoning']}")
    print(f"   Alternative: {rec['alternate']}")
    
    # 5. Check opening fit
    print("\n5. OPENING FIT ANALYSIS:")
    fits = [
        book.analyze_opening_fit("Italian Game", 1200),
        book.analyze_opening_fit("Ruy Lopez", 1200),
        book.analyze_opening_fit("Scandinavian Defense", 1150)
    ]
    for fit in fits:
        print(f"   {fit['opening']}: {fit['fit']} ({fit['message']})")
    
    # 6. Universal principles
    print("\n6. UNIVERSAL OPENING PRINCIPLES:")
    principles = book.get_universal_principles()
    for principle, description in principles.items():
        print(f"   • {principle}:")
        print(f"     {description[:80]}...")
    
    # 7. Get ideas for specific opening
    print("\n7. KEY IDEAS - RUY LOPEZ:")
    ideas = book.get_opening_ideas("Ruy Lopez")
    if ideas:
        for i, idea in enumerate(ideas, 1):
            print(f"   {i}. {idea}")
    
    # 8. Openings for player's rating
    print("\n8. OPENINGS APPROPRIATE FOR 1200 RATING:")
    appropriate = book.get_openings_by_elo_range(1200)
    for opening in appropriate:
        print(f"   ✓ {opening.name} ({opening.difficulty.value})")
    
    print("\n" + "=" * 70)
    print("Phase 1.2 Complete! Opening book fully functional.")
    print("=" * 70)