#!/usr/bin/env python3
"""Headless auto client for testing (moved into client package).

Usage: python -m client.auto_client --name Bot1 --choice A
"""
import socket
import time
import random
import argparse

HOST = '127.0.0.1'
PORT = 65432


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', '-n', default=f'bot{random.randint(100,999)}')
    p.add_argument('--choice', '-c', choices=['A', 'B', 'C', 'D'], default=None)
    args = p.parse_args()
    name = args.name
    forced_choice = args.choice

    try:
        sock = socket.create_connection((HOST, PORT), timeout=5)
        try:
            sock.settimeout(None)
        except Exception:
            pass
        f = sock.makefile('r', encoding='utf-8', newline='\n')
    except Exception as e:
        print(f"[{name}] Could not connect: {e}")
        return

    try:
        sock.sendall((f'NAME|{name}\n').encode('utf-8'))
        print(f"[{name}] Connected and sent NAME")

        for raw in f:
            line = raw.rstrip('\n')
            if not line:
                continue
            print(f"[{name}] RECV: {line}")
            if line.startswith('QUESTION:'):
                parts = line.split('|')
                try:
                    qidx = parts[1]
                except Exception:
                    qidx = '0'
                delay = random.uniform(0.3, 1.5)
                time.sleep(delay)
                if forced_choice:
                    choice = forced_choice
                else:
                    choice = random.choice(['A', 'B', 'C', 'D'])
                msg = f'ANSWER:{qidx}|{choice}\n'
                try:
                    sock.sendall(msg.encode('utf-8'))
                    print(f"[{name}] SENT: {msg.strip()}")
                except Exception as e:
                    print(f"[{name}] Error sending answer: {e}")
            if 'GAME OVER' in line or line.startswith('RESULT|'):
                print(f"[{name}] Game over detected, exiting.")
                break

    except Exception as e:
        print(f"[{name}] Receiver error: {e}")
    finally:
        try:
            sock.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
