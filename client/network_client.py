

import threading
import traceback
from typing import Callable, Optional

from config.client_config import client_config
from core.network_utils import (
    close_socket_safely,
    create_socket_with_file,
    send_line as network_send_line,
)


class ClientNetwork:
    """TCP client that reads lines and dispatches events to callbacks.

    This class manages the network connection to the game server, handles
    incoming messages, and dispatches events to registered callbacks.

    Callbacks (all optional):
        on_question: Called when question is received (qidx, question, opts)
        on_leaderboard: Called when leaderboard is received (payload)
        on_eval: Called when answer evaluation is received (tag, given)
        on_name_ok: Called when player name is accepted
        on_name_taken: Called when player name is already taken
        on_score: Called when final score is received (payload)
        on_log: Called for logging messages (text)
        on_disconnect: Called when connection is lost
        on_error: Called for server-side errors (message)
        on_wait: Called when waiting in lobby
        on_start: Called when game starts
        on_server_paused: Called when server is paused (message)
        on_game_started: Called when trying to join started game (message)
        on_game_paused: Called when game is paused during play (message)

    Example:
        >>> client = ClientNetwork(host='127.0.0.1', port=65432)
        >>> client.on_question = lambda qidx, text, opts: print(f"Q{qidx}: {text}")
        >>> client.on_log = lambda msg: print(f"[LOG] {msg}")
        >>> if client.connect():
        ...     client.send_line("NAME|Player1")
        >>> client.disconnect()
    """

    def __init__(self, host: str = None, port: int = None):
        """Initialize client network handler.

        Args:
            host: Server hostname or IP address. Defaults to client_config.DEFAULT_HOST
            port: Server port number. Defaults to client_config.DEFAULT_PORT
        """
        self.host = host or client_config.DEFAULT_HOST
        self.port = int(port or client_config.DEFAULT_PORT)
        self.sock = None
        self._sockfile = None
        self.running = False
        self.receiver_thread = None

        # Callback hooks - all optional
        self.on_question: Optional[Callable] = None
        self.on_leaderboard: Optional[Callable] = None
        self.on_eval: Optional[Callable] = None
        self.on_name_ok: Optional[Callable] = None
        self.on_name_taken: Optional[Callable] = None
        self.on_score: Optional[Callable] = None
        self.on_log: Optional[Callable] = None
        self.on_disconnect: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_wait: Optional[Callable] = None
        self.on_start: Optional[Callable] = None
        self.on_server_paused: Optional[Callable] = None
        self.on_game_started: Optional[Callable] = None
        self.on_game_paused: Optional[Callable] = None

    def _log(self, text: str):
        """Internal logging method that calls on_log callback if set.

        Args:
            text: Log message to send
        """
        try:
            if self.on_log:
                self.on_log(text)
        except Exception:
            pass

    def send_line(self, line: str):
        """Send a line-delimited message to server.

        Args:
            line: Message to send (will be line-terminated automatically)

        Note:
            ANSWER messages are logged to console for debugging.
        """
        try:
            # Debug log for ANSWER messages to console only
            if line.startswith('ANSWER|') or line.startswith('ANSWER:'):
                # Support both ANSWER|<qidx>|<ans> and ANSWER:<qidx>|<ans>
                payload = line.split(':', 1)[1] if ':' in line else line.split('|', 1)[1]
                parts = payload.split('|')
                if len(parts) >= 2:
                    qidx = parts[0]
                    ans = parts[1]
                    try:
                        qdisp = int(qidx) if isinstance(qidx, str) and qidx.isdigit() else qidx
                    except Exception:
                        qdisp = qidx
                    print(f"[SEND] ANSWER qidx={qdisp}, answer={ans}")

            if self.sock:
                if not network_send_line(self.sock, line):
                    self._log("Failed to send message to server")
        except Exception:
            self._log("Error sending to server:\n" + traceback.format_exc())

    def connect(self):
        """Connect to server and start receiver thread.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if self.running:
            return True

        self.sock, self._sockfile = create_socket_with_file(
            self.host,
            self.port,
            timeout=5
        )

        if self.sock is None or self._sockfile is None:
            self._log(f'Failed to connect to {self.host}:{self.port}')
            self.running = False
            return False

        self.running = True
        # Start receiver thread
        self.receiver_thread = threading.Thread(target=self._receiver_loop, daemon=True)
        self.receiver_thread.start()
        self._log(f'Connected to {self.host}:{self.port}')
        return True

    def connect_with_timeout(self, timeout: float = 2.0):
        """Connect using a custom timeout.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            bool: True if connection successful, False otherwise

        Note:
            Starts the receiver thread on success, identical to connect().
        """
        if self.running:
            return True

        self.sock, self._sockfile = create_socket_with_file(
            self.host,
            self.port,
            timeout=float(timeout)
        )

        if self.sock is None or self._sockfile is None:
            self._log(f'Failed to connect to {self.host}:{self.port}')
            self.running = False
            return False

        self.running = True
        self.receiver_thread = threading.Thread(target=self._receiver_loop, daemon=True)
        self.receiver_thread.start()
        self._log(f'Connected to {self.host}:{self.port}')
        return True

    def disconnect(self):
        """Disconnect from server and cleanup resources."""
        self.running = False
        close_socket_safely(self.sock)
        self.sock = None
        self._sockfile = None

    def _safe_callback(self, callback: Optional[Callable], *args, **kwargs):
        """Safely invoke callback, suppressing exceptions.

        Args:
            callback: Callback function to invoke
            *args: Positional arguments for callback
            **kwargs: Keyword arguments for callback
        """
        if callback:
            try:
                callback(*args, **kwargs)
            except Exception:
                pass

    def _handle_server_paused(self, line: str) -> bool:
        """Handle SERVER_PAUSED message.

        Args:
            line: Raw message line from server

        Returns:
            bool: True to break receiver loop, False to continue
        """
        msg = line.split('|', 1)[1] if '|' in line else 'Server đang tạm ngưng, vui lòng đợi...'
        self._safe_callback(self.on_server_paused, msg)
        if not self.on_server_paused:
            self._log(f'SERVER: {msg}')
        return True

    def _handle_game_started(self, line: str) -> bool:
        """Handle GAME_STARTED message.

        Args:
            line: Raw message line from server

        Returns:
            bool: True to break receiver loop, False to continue
        """
        msg = line.split('|', 1)[1] if '|' in line else 'Game đã bắt đầu, không thể tham gia.'
        self._safe_callback(self.on_game_started, msg)
        if not self.on_game_started:
            self._log(f'SERVER: {msg}')
        return True

    def _handle_error(self, line: str) -> bool:
        """Handle ERROR message.

        Args:
            line: Raw message line from server

        Returns:
            bool: True to break receiver loop, False to continue
        """
        msg = line.split('|', 1)[1] if '|' in line else ''
        self._safe_callback(self.on_error, msg)
        return True

    def _handle_simple_message(self, message_type: str):
        """Handle simple messages like NAME_OK, NAME_TAKEN, WAIT, START.

        Args:
            message_type: Type of simple message (NAME_OK, NAME_TAKEN, WAIT, START)
        """
        callbacks = {
            'NAME_OK': self.on_name_ok,
            'NAME_TAKEN': self.on_name_taken,
            'WAIT': (self.on_wait, 'SERVER: WAIT'),
            'START': (self.on_start, 'SERVER: START')
        }

        callback_info = callbacks.get(message_type)
        if isinstance(callback_info, tuple):
            callback, fallback_msg = callback_info
            self._safe_callback(callback)
            if not callback:
                self._log(fallback_msg)
        else:
            self._safe_callback(callback_info)

    def _handle_game_paused(self, line: str):
        """Handle STOP or GAME_PAUSED message.

        Args:
            line: Raw message line from server
        """
        msg = line.split('|', 1)[1] if '|' in line else 'Game đã tạm dừng.'
        self._safe_callback(self.on_game_paused, msg)
        if not self.on_game_paused:
            self._log(f'SERVER: {msg}')

    def _parse_question(self, line: str) -> tuple:
        """Parse QUESTION message.

        Args:
            line: Raw message line from server

        Returns:
            tuple: (qidx, qtext, opts) - question index, text, and options list
        """
        sep = ':' if line.startswith('QUESTION:') else '|'
        payload = line.split(sep, 1)[1]
        parts = payload.split('|')

        qidx, qtext, opts = 0, '', []

        if len(parts) >= 2:
            raw_qidx = parts[0]
            qidx = int(raw_qidx) if raw_qidx.isdigit() else raw_qidx
            qtext = parts[1]

            if len(parts) >= 3:
                if ',' in parts[2] and len(parts) == 3:
                    opts = [o.strip() for o in parts[2].split(',') if o.strip()]
                else:
                    opts = [p.strip() for p in parts[2:]]

        return qidx, qtext, opts

    def _handle_question(self, line: str):
        """Handle QUESTION message.

        Args:
            line: Raw message line from server
        """
        qidx, qtext, opts = self._parse_question(line)
        try:
            print(f"[RECV] QUESTION qidx={qidx}, question={qtext}")
        except Exception:
            pass
        self._safe_callback(self.on_question, qidx, qtext, opts)

    def _handle_leaderboard(self, line: str):
        """Handle LEADERBOARD message.

        Args:
            line: Raw message line from server
        """
        payload = line.split('|', 1)[1]
        self._safe_callback(self.on_leaderboard, payload)

    def _handle_score(self, line: str):
        """Handle SCORE message.

        Args:
            line: Raw message line from server
        """
        payload = line.split('|', 1)[1] if '|' in line else ''
        self._safe_callback(self.on_score, payload)

    def _handle_eval(self, line: str):
        """Handle EVAL message.

        Args:
            line: Raw message line from server
        """
        parts = line.split('|')
        if len(parts) >= 3:
            tag, given = parts[1], parts[2]
            self._safe_callback(self.on_eval, tag, given)

    def _process_message(self, line: str) -> bool:
        """Process single message line.

        Args:
            line: Raw message line from server

        Returns:
            bool: True if receiver loop should break, False to continue
        """
        if line.startswith('SERVER_PAUSED|'):
            return self._handle_server_paused(line)

        if line.startswith('GAME_STARTED|'):
            return self._handle_game_started(line)

        if line.startswith('ERROR|'):
            return self._handle_error(line)

        if line in ('NAME_OK', 'NAME_TAKEN', 'WAIT', 'START'):
            self._handle_simple_message(line)
            return False

        if line == 'STOP' or line.startswith('GAME_PAUSED|'):
            self._handle_game_paused(line)
            return False

        if line.startswith('QUESTION:') or line.startswith('QUESTION|'):
            self._handle_question(line)
            return False

        if line.startswith('LEADERBOARD|'):
            self._handle_leaderboard(line)
            return False

        if line.startswith('SCORE|'):
            self._handle_score(line)
            return False

        if line.startswith('EVAL|'):
            self._handle_eval(line)
            return False

        self._log('SERVER: ' + line)
        return False

    def _receiver_loop(self):
        """Main receiver loop - reads and dispatches messages.

        Runs in a separate thread, continuously reading lines from the server
        and dispatching them to appropriate handlers until connection is lost
        or a terminal message is received.
        """
        try:
            for raw in self._sockfile:
                line = raw.rstrip('\n')
                if not line:
                    continue

                try:
                    should_break = self._process_message(line)
                    if should_break:
                        break
                except Exception:
                    self._log('Error handling line:\n' + traceback.format_exc())
        except Exception:
            self._log('Receiver thread error:\n' + traceback.format_exc())
        finally:
            self.running = False
            self._safe_callback(self.on_disconnect)
