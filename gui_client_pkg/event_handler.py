"""Networking and protocol handling for the Quiz GUI client.

Encapsulates a simple TCP client that reads line-delimited messages and invokes
callbacks provided by the UI (on_question, on_leaderboard, on_log, on_disconnect).
"""

# --- Imports ---
import socket
import threading
import traceback
from typing import Callable, Optional


class ClientNetwork:
    """Simple TCP client that reads lines and dispatches events to callbacks.

    Callbacks (all optional):
    - on_question(qidx, question, opts)
    - on_leaderboard(payload)
    - on_log(text)
    - on_disconnect()
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 65432):
        self.host = host
        self.port = int(port)
        self.sock = None
        self._sockfile = None
        self.running = False
        self.receiver_thread = None

        # callback hooks
        self.on_question: Optional[Callable] = None
        self.on_leaderboard: Optional[Callable] = None
        self.on_eval: Optional[Callable] = None
        self.on_log: Optional[Callable] = None
        self.on_disconnect: Optional[Callable] = None

    def _log(self, text: str):
        try:
            if self.on_log:
                self.on_log(text)
        except Exception:
            pass

    def send_line(self, line: str):
        try:
            # Debug log for ANSWER messages to console only
            if line.startswith('ANSWER|') or line.startswith('ANSWER:'):
                # support both ANSWER|<qidx>|<ans> and ANSWER:<qidx>|<ans>
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
                self.sock.sendall((line + "\n").encode('utf-8'))
        except Exception:
            self._log("Error sending to server:\n" + traceback.format_exc())

    def connect(self):
        if self.running:
            return True
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=5)
            # ensure blocking mode for makefile reads (avoid intermittent TimeoutError)
            try:
                self.sock.settimeout(None)
            except Exception:
                pass
            self._sockfile = self.sock.makefile('r', encoding='utf-8', newline='\n')
            self.running = True
            # start receiver thread
            self.receiver_thread = threading.Thread(target=self._receiver_loop, daemon=True)
            self.receiver_thread.start()
            self._log(f'Connected to {self.host}:{self.port}')
            return True
        except Exception:
            self._log('Failed to connect:\n' + traceback.format_exc())
            self.running = False
            return False

    def disconnect(self):
        try:
            self.running = False
            try:
                if self.sock:
                    self.sock.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                if self.sock:
                    self.sock.close()
            except Exception:
                pass
        finally:
            self.sock = None
            self._sockfile = None

    def _receiver_loop(self):
        try:
            for raw in self._sockfile:
                line = raw.rstrip('\n')
                if not line:
                    continue
                # dispatch to UI callbacks
                try:
                    # Accept QUESTION lines with either ':' or '|' after the word
                    if line.startswith('QUESTION:') or line.startswith('QUESTION|'):
                        # normalize payload after the separator
                        sep = ':' if line.startswith('QUESTION:') else '|'
                        payload = line.split(sep, 1)[1]
                        # payload expected formats:
                        #  - <qidx>|<question>|opt1,opt2,opt3
                        #  - <qidx>|<question>|opt1|opt2|opt3
                        parts = payload.split('|')
                        qidx = 0
                        qtext = ''
                        opts = []
                        try:
                            if len(parts) >= 2:
                                raw_qidx = parts[0]
                                try:
                                    qidx = int(raw_qidx) if raw_qidx.isdigit() else raw_qidx
                                except Exception:
                                    qidx = raw_qidx
                                qtext = parts[1]
                                # options may be a single comma-separated field or multiple pipe fields
                                if len(parts) >= 3:
                                    if ',' in parts[2] and len(parts) == 3:
                                        opts = [o.strip() for o in parts[2].split(',') if o.strip()]
                                    else:
                                        opts = [p.strip() for p in parts[2:]]
                        except Exception:
                            # fallback: leave opts empty
                            opts = []
                        try:
                            print(f"[RECV] QUESTION qidx={qidx}, question={qtext}")
                        except Exception:
                            pass
                        if self.on_question:
                            self.on_question(qidx, qtext, opts)
                        # do not log raw QUESTION lines to the general log (we display them in UI)
                        continue
                    if line.startswith('LEADERBOARD|'):
                        payload = line.split('|', 1)[1]
                        if self.on_leaderboard:
                            self.on_leaderboard(payload)
                        continue
                    if line.startswith('SCORE|'):
                        # SCORE|<points>/<total>
                        payload = line.split('|', 1)[1] if '|' in line else ''
                        try:
                            if self.on_score:
                                self.on_score(payload)
                        except Exception:
                            pass
                        continue
                    # EVAL messages: inform UI about correctness without logging raw payload
                    if line.startswith('EVAL|'):
                        # expected: EVAL|RIGHT|<given> or EVAL|WRONG|<given>
                        parts = line.split('|')
                        if len(parts) >= 3:
                            tag = parts[1]
                            given = parts[2]
                            if self.on_eval:
                                try:
                                    self.on_eval(tag, given)
                                except Exception:
                                    pass
                            continue
                    # fallback -- log unknown server messages
                    self._log('SERVER: ' + line)
                except Exception:
                    self._log('Error handling line:\n' + traceback.format_exc())
        except Exception:
            self._log('Receiver thread error:\n' + traceback.format_exc())
        finally:
            self.running = False
            if self.on_disconnect:
                try:
                    self.on_disconnect()
                except Exception:
                    pass
