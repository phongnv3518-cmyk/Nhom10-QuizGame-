import threading
from queue import Queue, Empty
from typing import Dict, List, Optional, Tuple


class UILogger:
    """Thread-safe logger and state store for a server dashboard.

    Responsibilities:
    - Stream log lines to a UI via a queue.
    - Track active players with statuses: waiting, in_quiz, done.
    - Track scoreboard entries per player: score, total, status.
    - Track statistics: online count, total started, finished count,
      high/low score, completion ratio.
    """

    def __init__(self) -> None:
        self._log_queue: Queue[str] = Queue()
        self._lock = threading.Lock()
        self._active_players: Dict[str, str] = {}  # name -> status
        self._scoreboard: Dict[str, Dict[str, int | str]] = {}  # name -> {score,total,status}
        self._started_names: set[str] = set()
        self._finished_names: set[str] = set()
        self._server_running: bool = False  # Start with False, teacher must press START
        self._shutdown_requested: bool = False
        
        # Callback for broadcasting stop (dependency injection to avoid circular import)
        self._broadcast_stop_callback = None
     
        self._game_state: str = 'NOT_STARTED'
        self._waiting_room: set[str] = set()  # Players waiting for START button

    def send_log(self, message: str) -> None:
        try:
            print(message)
        except Exception:
            pass
        try:
            self._log_queue.put_nowait(message)
        except Exception:
            pass

    def log(self, text: str) -> None:
        self.send_log(text)

    def drain_logs(self, max_items: int = 1000) -> List[str]:
        items: List[str] = []
        for _ in range(max_items):
            try:
                items.append(self._log_queue.get_nowait())
            except Empty:
                break
        return items

    def update_active_players(self, names: List[str]) -> None:
        with self._lock:
            current = {n: self._active_players.get(n, 'waiting') for n in names}
            self._active_players = current

    def add_active_player(self, name: str, status: str = 'waiting') -> None:
        with self._lock:
            self._active_players[name] = status

    def remove_active_player(self, name: str) -> None:
        with self._lock:
            if name in self._active_players:
                del self._active_players[name]

    def set_player_status(self, name: str, status: str) -> None:
        with self._lock:
            self._active_players[name] = status

    def get_active_players_with_status(self) -> List[Tuple[str, str]]:
        with self._lock:
            return sorted(self._active_players.items(), key=lambda x: x[0])

    def set_active_names(self, names: List[str]) -> None:
        self.update_active_players(names)

    def add_active_name(self, name: str) -> None:
        self.add_active_player(name, 'waiting')

    def remove_active_name(self, name: str) -> None:
        self.remove_active_player(name)

    def get_active_names(self) -> List[str]:
        return [n for n, _ in self.get_active_players_with_status()]

    def update_scoreboard(self, name: str, score: int, total: int, status: str = 'done') -> None:
        with self._lock:
            self._scoreboard[name] = {'score': int(score), 'total': int(total), 'status': status}
            self._finished_names.add(name)

    def get_scoreboard_rows(self) -> List[Dict[str, int | str]]:
        with self._lock:
            rows = [{'name': n, **d} for n, d in self._scoreboard.items()]
        rows.sort(key=lambda r: (r.get('score', 0), -r.get('total', 1)), reverse=True)
        return rows

    def record_score(self, points: int) -> None:
        pass

    def get_score_extremes(self) -> Tuple[Optional[int], Optional[int]]:
        rows = self.get_scoreboard_rows()
        if not rows:
            return None, None
        scores = [int(r['score']) for r in rows]
        return max(scores), min(scores)

    def get_top_player(self) -> Tuple[Optional[str], Optional[int]]:
        rows = self.get_scoreboard_rows()
        if not rows:
            return None, None
        top = rows[0]
        return str(top.get('name', '')) if top.get('name') is not None else None, int(top.get('score', 0))

    def mark_started(self, name: str) -> None:
        with self._lock:
            self._started_names.add(name)

    def mark_finished(self, name: str) -> None:
        with self._lock:
            self._finished_names.add(name)

    def get_statistics(self) -> Dict[str, int | float | None]:
        with self._lock:
            online = len(self._active_players)
            total_started = len(self._started_names)
            total_finished = len(self._finished_names)
            server_running = self._server_running
        high, low = self.get_score_extremes()
        top_name, top_score = self.get_top_player()
        completion = 0.0
        if total_started > 0:
            completion = round((total_finished / total_started) * 100.0, 1)
        return {
            'online': online,
            'total_started': total_started,
            'high_score': high,
            'low_score': low,
            'completion_rate': completion,
            'top_player': top_name,
            'top_score': top_score,
            'server_running': server_running,
        }

    def reset_scores_and_names(self, name_registry=None) -> None:
        """Reset scoreboard and clear all registered names.
        
        Args:
            name_registry: Optional NameRegistry instance to clear names from
        """
        with self._lock:
            self._scoreboard.clear()
            self._finished_names.clear()
            self._active_players.clear()
            self._started_names.clear()
        
        self.send_log('Server remains RUNNING after reset - clients can still join')
        
        # Clear name registry if provided
        if name_registry is not None:
            try:
                name_registry.clear_all()
                self.send_log('All active names cleared due to score reset.')
            except Exception as e:
                self.send_log(f'Error clearing name registry: {e}')
        
        self.send_log('Scoreboard and names have been reset by operator')
    
    def reset_scores(self) -> None:
        """Legacy method - kept for compatibility."""
        with self._lock:
            self._scoreboard.clear()
            self._finished_names.clear()
        self.send_log('Scoreboard has been reset by operator')

    def set_server_running(self, running: bool) -> None:
        """Handle START/STOP button clicks from dashboard.
        
        Game State Transitions:
        ----------------------
        START button (running=True):
            NOT_STARTED → STARTED
            - Release all waiting room players to quiz
            - Clear waiting room (no longer accepting new players)
            - Enable quiz question delivery
            
        STOP button (running=False):
            STARTED → NOT_STARTED
            - Broadcast stop signal to all connected clients
            - Reset to waiting room mode
            - Allow new players to join again
            
        Anti-spam Protection:
        --------------------
        - START when STARTED → Ignored ("already running")
        - STOP when NOT_STARTED → Ignored ("not started yet")
        - Dashboard buttons auto-disable based on state
        """
        with self._lock:
            old_state = self._game_state
            
            if running:
                # ─────────────────────────────────────────────────────────────
                # START BUTTON PRESSED
                # ─────────────────────────────────────────────────────────────
                if self._game_state == 'NOT_STARTED':
                    self._game_state = 'STARTED'
                    self.send_log('Game STARTED - Waiting room players now playing')
                    
                    # Release all waiting players to active quiz
                    for name in self._waiting_room:
                        self._active_players[name] = 'in_quiz'
                    self._waiting_room.clear()
                    
                elif self._game_state == 'STARTED':
                    # Anti-spam: Ignore duplicate START clicks
                    self.send_log('Cannot START - Game already running')
                    return
                    
            else:
                # ─────────────────────────────────────────────────────────────
                # STOP BUTTON PRESSED
                # ─────────────────────────────────────────────────────────────
                if self._game_state == 'STARTED':
                    self._game_state = 'NOT_STARTED'
                    self.send_log('Game STOPPED - Reset to waiting room mode')
                    
                elif self._game_state == 'NOT_STARTED':
                    # Anti-spam: Ignore STOP when not running
                    self.send_log('Cannot STOP - Game not started yet')
                    return
            
            self._server_running = bool(running)
        
        if not running:
            # Use registered callback instead of dynamic import (avoids deadlock)
            if self._broadcast_stop_callback:
                try:
                    self.send_log('Broadcasting STOP to all connected clients')
                    self._broadcast_stop_callback()
                except Exception as e:
                    self.send_log(f'Warning: Could not broadcast stop: {e}')
        
        self.send_log(f'State transition: {old_state} → {self._game_state}')

    def get_game_state(self) -> str:
        with self._lock:
            return self._game_state
    
    def add_to_waiting_room(self, name: str) -> bool:
        """Add player to waiting room (only works in NOT_STARTED state).
        
        Returns:
            True: Player added to waiting room successfully
            False: Waiting room unavailable (game already STARTED)
            
        Behavior by State:
            NOT_STARTED: Accept player → waiting room
            STARTED: Reject player (late join blocked)
        """
        with self._lock:
            if self._game_state != 'NOT_STARTED':
                return False  # Waiting room only exists in NOT_STARTED state
            self._waiting_room.add(name)
            self._active_players[name] = 'waiting'
            return True
    
    def is_waiting_room_available(self) -> bool:
        """Check if waiting room accepts new players.
        
        Returns:
            True: NOT_STARTED state (waiting room open)
            False: STARTED state (late join blocked)
        """
        with self._lock:
            return self._game_state == 'NOT_STARTED'

    def is_server_running(self) -> bool:
        with self._lock:
            return self._server_running

    def request_shutdown(self) -> None:
        with self._lock:
            self._shutdown_requested = True
        self.send_log('Shutdown requested from GUI')

    def is_shutdown_requested(self) -> bool:
        with self._lock:
            return self._shutdown_requested
    
    def register_broadcast_stop_callback(self, callback) -> None:
        """Register callback for broadcasting STOP to clients (dependency injection)."""
        self._broadcast_stop_callback = callback


ui_logger = UILogger()
