#!/usr/bin/env python3
"""Simple terminal client for the quiz server (moved into client package).

Usage: python -m client.client
"""
import socket

HOST = '127.0.0.1'
PORT = 65432


def recv_line(sock: socket.socket) -> str:
    buf = []
    try:
        while True:
            ch = sock.recv(1)
            if not ch:
                return ''
            if ch == b'\n':
                break
            buf.append(ch)
        return b''.join(buf).decode('utf-8').rstrip('\r')
    except Exception:
        return ''


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    try:
        # optional welcome
        line = recv_line(sock)
        if line:
            print('Server:', line)
        name = input('Enter your name: ').strip() or 'player'
        sock.sendall((name + '\n').encode('utf-8'))

        while True:
            line = recv_line(sock)
            if not line:
                print('Connection closed by server')
                break
            if line.startswith('QUESTION:'):
                payload = line.split(':', 1)[1]
                try:
                    qid, qtext, opts = payload.split('|', 2)
                    print(f"\nQuestion [{qid}]: {qtext}")
                    print('Options:', opts)
                    ans = input('Answer (type letter or text): ').strip()
                    msg = f'ANSWER:{qid}|{ans}\n'
                    sock.sendall(msg.encode('utf-8'))
                except Exception as e:
                    print('Malformed QUESTION:', e)
            elif line.startswith('EVAL|'):
                print('EVAL:', line)
            elif line.startswith('SCORE|'):
                print('Final:', line)
                break
            else:
                print('Server:', line)

    except KeyboardInterrupt:
        print('\nCancelled by user')
    finally:
        try:
            sock.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
