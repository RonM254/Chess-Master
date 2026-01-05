"""
Chess Master Web Server
=======================
A pure Python HTTP server that powers the interactive web interface.
Zero dependencies - uses standard library 'http.server'.

Endpoints:
    GET /               : Serves src/index.html
    POST /api/new_game  : Resets the board
    POST /api/move      : Makes a move and returns new state
    POST /api/analyze   : Returns full position analysis
    POST /api/review    : Reviews a full game from move list
    POST /api/example   : Loads an example game

Usage:
    python src/web_server.py
"""

import sys
import json
import http.server
import socketserver
from pathlib import Path
from typing import Dict, Any

# Ensure we can import from src regardless of how this script is run
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.game_manager import GameManager
from src.chess_engine import Color

# Global game instance
game = GameManager()

class ChessRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handles HTTP requests for the Chess Master interface."""
    
    def do_GET(self):
        """Serve the index.html file."""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_path = Path(__file__).parent / 'index.html'
            with open(html_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Fallback for other static files if needed
            super().do_GET()

    def do_POST(self):
        """Handle API requests."""
        if self.path.startswith('/api/'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}
            
            response = self.handle_api(self.path, data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def handle_api(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch API calls to GameManager methods."""
        global game
        
        try:
            if path == '/api/new_game':
                game.reset_board()
                return self._get_game_state()
                
            elif path == '/api/move':
                from_pos = data.get('from')
                to_pos = data.get('to')
                
                success = game.make_move(from_pos, to_pos)
                state = self._get_game_state()
                state['success'] = success
                if not success:
                    state['error'] = "Invalid move"
                return state
                
            elif path == '/api/analyze':
                return {
                    'analysis': game.analyze_position(),
                    'best_moves': game.get_best_moves(3),
                    'tactics': self._get_tactics()
                }
                
            elif path == '/api/review':
                # Parse and review a full game
                moves_text = data.get('moves', '')
                return self._review_game(moves_text)
                
            elif path == '/api/example':
                # Reset and play a predefined example
                game.reset_board()
                return self._play_example(data.get('name', 'italian'))
                
            else:
                return {'error': 'Unknown endpoint'}
                
        except Exception as e:
            return {'error': str(e)}

    def _get_game_state(self) -> Dict[str, Any]:
        """Get the current board state and basic info."""
        return {
            'fen': game.get_board_fen(),
            'turn': 'white' if game.current_player == Color.WHITE else 'black',
            'legal_moves': [m.to_algebraic() for m in game.get_legal_moves()],
            'material': game.get_material_balance()
        }
        
    def _get_tactics(self) -> Dict[str, Any]:
        """Get current tactical opportunities."""
        return {
            'white_hanging': len(game.detect_hanging_pieces(Color.WHITE)),
            'black_hanging': len(game.detect_hanging_pieces(Color.BLACK)),
            'white_forks': len(game.detect_forks(Color.WHITE)),
            'black_forks': len(game.detect_forks(Color.BLACK))
        }

    def _review_game(self, moves_text: str) -> Dict[str, Any]:
        """
        Review a game from a text string of moves.
        Reset board, play all moves, and return analysis for each step.
        """
        game.reset_board()
        report = []
        
        # Simple parser: replace newlines with spaces, remove move numbers (1., 2.), split by space
        clean_text = moves_text.replace('\n', ' ')
        tokens = clean_text.split()
        
        # Filter out move numbers like "1." or "1..."
        moves = [t for t in tokens if not t[0].isdigit() and not t.endswith('.')]
        
        # We need a way to convert algebraic (e4) to from-to (e2-e4)
        # Our engine currently primarily takes from-to strings in make_move
        # BUT make_move expects "e2", "e4".
        # This is a limitation: our pure python engine doesn't have a full SAN parser yet.
        # For this prototype, we will assume the User inputs "e2e4" or "e2-e4" style moves
        # OR we extend this to support basic SAN if possible, but that's complex without a library.
        # Let's stick to the engine's preferred format for now or try to map it.
        
        # Actually, let's just assume the input is "e2e4" or "e2-e4" for now to be safe,
        # or update the frontend to send strict format.
        
        processed_moves = []
        for move_str in moves:
            # Basic cleanup
            move_str = move_str.replace('-', '').replace('x', '').replace('+', '').replace('#', '')
            # Try to grab last 4 chars if it looks like coordinate notation (e.g. Nge2e4 -> e2e4)
            # This is a hack; a real engine needs a SAN parser.
            # For this "Phase 1" project, we'll ask the user to use coordinate notation in the UI check.
            
            if len(move_str) >= 4:
                # heuristic: take last 4 characters usually works for coordinates
                # e.g. "e2e4"
                f, t = move_str[-4:-2], move_str[-2:]
                if game.make_move(f, t):
                    # Analyze after move
                    analysis = game.analyze_position()
                    processed_moves.append({
                        'move': f"{f}-{t}",
                        'success': True,
                        'score': analysis['total_score'],
                        'assessment': analysis['assessment']
                    })
                else:
                    processed_moves.append({'move': move_str, 'success': False, 'error': 'Illegal or invalid format'})
            else:
                 processed_moves.append({'move': move_str, 'success': False, 'error': 'Use coordinate format (e.g. e2e4)'})

        return {
            'report': processed_moves,
            'final_fen': game.get_board_fen(),
            'summary': game.get_game_summary()
        }

    def _play_example(self, name: str) -> Dict[str, Any]:
        """Play an example opening."""
        moves = []
        if name == 'italian':
            moves = [("e2", "e4"), ("e7", "e5"), ("g1", "f3"), ("b8", "c6"), ("f1", "c4")]
        elif name == 'french':
            moves = [("e2", "e4"), ("e6", "e6"), ("d2", "d4"), ("d7", "d5")]
        
        for f, t in moves:
            game.make_move(f, t)
            
        return self._get_game_state()


def main():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), ChessRequestHandler) as httpd:
        print(f"\\n♟️  Chess Master Web Server running at http://localhost:{PORT}")
        print(f"   Serving src/index.html")
        print("   Press Ctrl+C to stop\\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nStopping server...")
            httpd.server_close()

if __name__ == "__main__":
    main()
