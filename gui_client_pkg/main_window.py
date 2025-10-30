"""Main window composition and UI glue code.

This module composes LogPanel, QuestionPanel and ClientNetwork.
It implements the join dialog and wiring between UI and network callbacks.
"""

# --- Imports ---
import tkinter as tk
from typing import Optional

from gui_client_pkg.log_panel import LogPanel
from gui_client_pkg.question_panel import QuestionPanel
from gui_client_pkg.event_handler import ClientNetwork
from tkinter import messagebox


class MainWindow:
    """Main application window that composes the UI and network client.

    Keep methods short and focused; network-to-UI callbacks are thin adaptors.
    """

    def __init__(self, master, host: str = '127.0.0.1', port: int = 10000):
        self.master = master
        self.host = host
        self.port = port
        self.current_qidx = None

        master.title('Quiz Game Client')
        master.configure(bg='#f3f7fa')

        # Header + player name
        header = tk.Label(master, text='Quiz Game Client', font=('Helvetica', 20, 'bold'), bg='#f3f7fa')
        header.pack(pady=(8, 4))
        self.name_label = tk.Label(master, text='', font=('Helvetica', 10), bg='#f3f7fa')
        self.name_label.pack(anchor='ne', padx=12)

        # Main frame
        main_frame = tk.Frame(master, bg='#f3f7fa')
        main_frame.pack(fill='both', expand=True, padx=12, pady=6)

        # Left: LogPanel
        # create left frame for log but do NOT show it by default (keeps UI clean)
        self.left_frame = tk.Frame(main_frame, bg='#ffffff')
        self.log = LogPanel(self.left_frame)

        # Right: QuestionPanel
        self.question_panel = QuestionPanel(main_frame)
        self.question_panel.set_on_answer(self._on_answer_clicked)

        # Bottom: status and reconnect
        bottom = tk.Frame(master, bg='#f3f7fa')
        bottom.pack(fill='x', padx=12, pady=(4, 12))
        self.status_var = tk.StringVar(value='Disconnected')
        status = tk.Label(bottom, textvariable=self.status_var, bg='#f3f7fa', anchor='w')
        status.pack(side='left')
        # toggle for showing/hiding the log panel (hidden by default)
        self.toggle_log_btn = tk.Button(bottom, text='Show Log', command=self._toggle_log)
        self.toggle_log_btn.pack(side='right', padx=(6, 6))

        # Networking client
        self.net = ClientNetwork(host=self.host, port=self.port)
        self.net.on_question = self._on_network_question
        self.net.on_leaderboard = self._on_network_leaderboard
        self.net.on_eval = getattr(self, '_on_network_eval', None)
        # score callback (will be called when server sends SCORE|...)
        self.net.on_score = getattr(self, '_on_network_score', None)
        self.net.on_log = self._on_network_log
        self.net.on_disconnect = self._on_network_disconnect

        # show join dialog soon after start
        self.master.after(100, self.show_join_dialog)
        master.protocol('WM_DELETE_WINDOW', self._on_close)

        # log hidden by default
        self._log_visible = False
        # Note: left_frame is not packed so the question panel fills the space

    # --- UI helpers and small adaptors ---
    def _on_network_log(self, text: str):
        self.log.append(text)

    def _on_network_question(self, qidx, qtext, opts):
        # schedule UI work on main thread
        self.master.after(0, lambda: self._show_question(qidx, qtext, opts))

    def _on_network_leaderboard(self, payload: str):
        self.master.after(0, lambda: self._show_leaderboard(payload))

    def _on_network_score(self, payload: str):
        # payload example: '3/5' -> points/total
        def show():
            try:
                # show a custom end-of-game panel with score and a Finish button
                # parse payload like '6/10'
                pts = payload.split('/', 1)[0] if '/' in payload else payload
                try:
                    pts_int = int(pts)
                except Exception:
                    pts_int = None

                dlg = tk.Toplevel(self.master)
                dlg.title('Kết thúc trò chơi')
                dlg.transient(self.master)
                dlg.grab_set()
                dlg.geometry('320x180')

                # Congratulatory message
                lbl_title = tk.Label(dlg, text='Chúc mừng!', font=('Helvetica', 16, 'bold'))
                lbl_title.pack(pady=(12, 6))

                score_text = f'Bạn đã đạt được: {pts}/10' if pts_int is not None else f'Điểm: {payload}'
                lbl_score = tk.Label(dlg, text=score_text, font=('Helvetica', 14))
                lbl_score.pack(pady=(6, 12))

                # optional details/log
                try:
                    self.log.append(f'Score received: {payload}')
                except Exception:
                    pass

                def finish():
                    try:
                        dlg.grab_release()
                    except Exception:
                        pass
                    try:
                        dlg.destroy()
                    except Exception:
                        pass
                    # close the main window / exit the quiz
                    try:
                        self._on_close()
                    except Exception:
                        pass

                btn = tk.Button(dlg, text='Hoàn thành', width=12, command=finish)
                btn.pack(pady=(8, 12))
                # center and wait
                try:
                    dlg.update_idletasks()
                    x = self.master.winfo_rootx() + (self.master.winfo_width() - dlg.winfo_width()) // 2
                    y = self.master.winfo_rooty() + (self.master.winfo_height() - dlg.winfo_height()) // 2
                    dlg.geometry(f'+{x}+{y}')
                except Exception:
                    pass
            except Exception:
                pass

        self.master.after(0, show)

    def _on_network_disconnect(self):
        self.master.after(0, self._handle_disconnect)

    def _on_network_eval(self, tag: str, given: str):
        # tag is RIGHT or WRONG, given is the letter the client sent (or SKIP)
        def show():
            try:
                self.log.append(f'SERVER: EVAL|{tag}|{given}')
                try:
                    self.question_panel.show_eval(tag, given)
                except Exception:
                    pass
            except Exception:
                pass

        self.master.after(0, show)

    # --- UI actions invoked by network callbacks ---
    def _show_question(self, qidx, qtext, opts):
        self.question_panel.display_question(qidx, qtext, opts)
        self.question_panel.start_countdown(15)
        # store current question id so answer messages include it
        try:
            self.current_qidx = int(qidx) if isinstance(qidx, (int, str)) and str(qidx).isdigit() else qidx
        except Exception:
            self.current_qidx = qidx
        self._set_status('Question received')

    def _show_leaderboard(self, payload: str):
        # payload example name1:3;name2:2 or comma separated; show as log
        items = [p for p in payload.replace(';', ',').split(',') if p.strip()]
        lines = ['Leaderboard:'] + [it.replace(':', ' - ') for it in items]
        self.log.append('\n'.join(lines))

    def _handle_disconnect(self):
        self._set_status('Disconnected')
        try:
            if hasattr(self, 'reconnect_btn'):
                self.reconnect_btn.config(state=tk.NORMAL)
        except Exception:
            pass
        self.log.append('Disconnected from server')
        self.question_panel.stop_countdown()

    def _set_status(self, text: str):
        try:
            self.status_var.set(text)
        except Exception:
            pass

    # --- Log show/hide helpers ---
    def _toggle_log(self):
        if getattr(self, '_log_visible', False):
            self._hide_log()
        else:
            self._show_log()

    def _show_log(self):
        try:
            # pack the left frame so the LogPanel becomes visible
            # show the log as a fixed-width side panel so it doesn't collapse
            try:
                # set a reasonable fixed width for the log column and prevent
                # geometry propagation so the inner widget doesn't shrink the frame
                self.left_frame.config(width=320)
                self.left_frame.pack_propagate(False)
            except Exception:
                pass
            # pack left column vertically only; question panel keeps filling the
            # remaining horizontal space (it is packed on the right with expand=True)
            self.left_frame.pack(side='left', fill='y', padx=(0, 8))
            self._log_visible = True
            try:
                self.toggle_log_btn.config(text='Hide Log')
            except Exception:
                pass
        except Exception:
            pass

    def _hide_log(self):
        try:
            self.left_frame.pack_forget()
            self._log_visible = False
            try:
                self.toggle_log_btn.config(text='Show Log')
            except Exception:
                pass
        except Exception:
            pass

    # --- User-initiated actions ---
    def _on_answer_clicked(self, letter: str):
        # send answer via network client
        if not self.net.running:
            self.log.append('Not connected; cannot send answer')
            return
        # send ANSWER with qid (numeric qidx when available)
        qid = self.current_qidx if self.current_qidx is not None else self.question_panel.question_label.cget("text")
        # handle timeout case: QuestionPanel passes empty string on timeout
        send_letter = letter if letter else 'SKIP'
        try:
            self.net.send_line(f'ANSWER:{qid}|{send_letter}')
        except Exception:
            self.log.append('Failed to send answer')
            return
        if send_letter == 'SKIP':
            self.log.append('No answer (timed out) — turn skipped')
        else:
            self.log.append(f'You answered: {letter}')
        # ensure countdown is stopped (QuestionPanel also stops it when clicked)
        try:
            self.question_panel.stop_countdown()
        except Exception:
            pass

    def reconnect(self):
        if self.net.running:
            self.log.append('Already connected')
            return
        self._set_status('Connecting...')
        if hasattr(self, 'reconnect_btn'):
            try:
                self.reconnect_btn.config(state=tk.DISABLED)
            except Exception:
                pass
        ok = self.net.connect()
        if ok:
            self._set_status(f'Connected to {self.host}:{self.port}')
            if hasattr(self, 'reconnect_btn'):
                try:
                    self.reconnect_btn.config(state=tk.DISABLED)
                except Exception:
                    pass
        else:
            self._set_status('Disconnected')
            if hasattr(self, 'reconnect_btn'):
                try:
                    self.reconnect_btn.config(state=tk.NORMAL)
                except Exception:
                    pass

    # --- Join dialog ---
    def show_join_dialog(self):
        dlg = tk.Toplevel(self.master)
        dlg.title('Join Quiz')
        dlg.transient(self.master)
        dlg.grab_set()
        dlg.geometry('320x140')

        tk.Label(dlg, text='Enter your player name:', font=('Helvetica', 11)).pack(pady=(12, 6))
        name_var = tk.StringVar()
        entry = tk.Entry(dlg, textvariable=name_var, font=('Helvetica', 12))
        entry.pack(padx=12, fill='x')
        entry.focus()

        btn_frame = tk.Frame(dlg)
        btn_frame.pack(pady=12)
        join_btn = tk.Button(btn_frame, text='Join', state=tk.DISABLED, width=10)
        cancel_btn = tk.Button(btn_frame, text='Cancel', width=10, command=lambda: self._close_join(dlg))
        join_btn.pack(side='left', padx=6)
        cancel_btn.pack(side='right', padx=6)

        def on_change(*_):
            v = name_var.get().strip()
            join_btn.config(state=(tk.NORMAL if v else tk.DISABLED))

        name_var.trace_add('write', on_change)

        def do_join():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning('Name required', 'Please enter a player name.')
                return
            self.name_label.config(text=f'Player: {name}')
            dlg.grab_release()
            dlg.destroy()
            # connect and send NAME
            if self.net.connect():
                self.net.send_line(f'NAME|{name}')
                self._set_status(f'Connected to {self.host}:{self.port}')

        join_btn.config(command=do_join)
        dlg.bind('<Return>', lambda e: do_join())
        dlg.bind('<Escape>', lambda e: (dlg.grab_release(), dlg.destroy()))

    def _close_join(self, dlg):
        dlg.grab_release()
        dlg.destroy()

    def _on_close(self):
        """Handle window close: disconnect network and destroy main window."""
        try:
            # attempt graceful disconnect of network client
            try:
                if hasattr(self, 'net') and self.net:
                    try:
                        self.net.disconnect()
                    except Exception:
                        pass
            except Exception:
                pass
        finally:
            try:
                self.master.destroy()
            except Exception:
                pass


def run(host: Optional[str] = None, port: Optional[int] = None):
    root = tk.Tk()
    root.geometry('900x560')
    mw = MainWindow(root, host=host or '127.0.0.1', port=port or 65432)
    root.mainloop()
if __name__ == '__main__':
    run()
