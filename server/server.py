"""Server entrypoint. Run with: python -m server.server

This server loads questions via core.shared_logic.load_questions("data/questions.csv").
Simple line protocol (QUESTION/ANSWER/EVAL/SCORE).
"""

import socket
import threading
import sys
import random
from core.shared_logic import load_questions

HOST = "127.0.0.1"
PORT = 65432
QUESTIONS_PATH = "data/questions.csv"
# limit how many questions a single quiz session will present
MAX_QUESTIONS = 10


def send_line(conn, text):
    conn.sendall((text.rstrip('\n') + '\n').encode('utf-8'))


def handle_client(conn, addr, questions):
    print(f"Client connected: {addr}")
    try:
        f = conn.makefile('r', encoding='utf-8')
        score = 0
        # create a per-client shuffled sequence so each client gets a random order
        client_questions = list(questions)
        random.shuffle(client_questions)
        if len(client_questions) > MAX_QUESTIONS:
            client_questions = client_questions[:MAX_QUESTIONS]
        total = len(client_questions)
        for idx, q in enumerate(client_questions):
            # q has keys: question, A,B,C,D,answer
            qid = str(idx)
            # build options list from A..D, shuffle them and determine the new correct letter
            orig_opts = [q.get('A', ''), q.get('B', ''), q.get('C', ''), q.get('D', '')]
            # original correct answer letter -> text
            orig_correct_letter = q.get('answer', 'A').upper()
            orig_correct_text = q.get(orig_correct_letter, '')

            shuffled_opts = list(orig_opts)
            random.shuffle(shuffled_opts)
            # map shuffled options to letters A..D and find new correct letter
            letters = ['A', 'B', 'C', 'D']
            new_answer_letter = 'A'
            for i, text in enumerate(shuffled_opts):
                if text == orig_correct_text:
                    new_answer_letter = letters[i]
                    break

            opts = ','.join(shuffled_opts)
            # send question with shuffled options; client will display options in received order
            send_line(conn, f"QUESTION:{qid}|{q['question']}|{opts}")

            line = f.readline()
            if not line:
                print(f"Client {addr} disconnected mid-quiz")
                return
            line = line.strip()
            if not line.startswith('ANSWER:'):
                # malformed answer line; mark wrong but don't reveal correct answer
                send_line(conn, f"EVAL|WRONG|{line}")
                continue
            try:
                _, payload = line.split(':', 1)
                rid, given = payload.split('|', 1)
                rid = rid.strip(); given = given.strip()
            except Exception:
                # parsing failed; treat as wrong without revealing the answer
                send_line(conn, f"EVAL|WRONG|{line}")
                continue

            if rid != qid:
                # id mismatch — treat as wrong
                send_line(conn, f"EVAL|WRONG|{given}")
            else:
                # compare against new_answer_letter (from shuffled options)
                if given.upper() == new_answer_letter.upper():
                    score += 1
                    send_line(conn, f"EVAL|RIGHT|{given}")
                else:
                    send_line(conn, f"EVAL|WRONG|{given}")

        send_line(conn, f"SCORE|{score}/{total}")
        print(f"Client {addr} finished: {score}/{total}")
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        try:
            f.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


def main():
    # use absolute path resolution via shared_logic; also pass MAX_QUESTIONS to loader as safeguard
    questions = load_questions(QUESTIONS_PATH, max_questions=MAX_QUESTIONS)
    if not questions:
        print(f"No questions found at {QUESTIONS_PATH}; server exiting.")
        sys.exit(1)
    # keep the master question pool intact; each client will receive its own
    # shuffled subset when they connect
    print(f"Loaded {len(questions)} questions from {QUESTIONS_PATH} (max per-client {MAX_QUESTIONS})")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Quiz server listening on {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr, questions), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print('\nServer shutting down')


if __name__ == '__main__':
    main()
