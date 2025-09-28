import socket
import pickle
import threading

# Get your local IP address
server = socket.gethostbyname(socket.gethostname())
port = 5555

# Set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen()

print(f"🌐 Server started on {server}:{port}. Waiting for players...")

# Player data structure
players = {}
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 0, 255)]
positions = [(50, 50), (400, 50), (50, 400), (400, 400), (200, 200)]

lock = threading.Lock()


# Handle individual player connection
def threaded_client(conn, player_id):
    with lock:
        players[player_id] = {
            "x": positions[player_id][0],
            "y": positions[player_id][1],
            "color": colors[player_id % len(colors)],
            "name": f"Player {player_id}",
            "score": 0,
        }

    # Send initial state
    conn.send(pickle.dumps(players))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                break

            with lock:
                players[player_id].update(data)
                conn.sendall(pickle.dumps(players))
        except:
            break

    with lock:
        if player_id in players:
            print(f"❌ Player {player_id} disconnected.")
            del players[player_id]
    conn.close()


# Accept players and assign them threads
player_count = 0
while True:
    conn, addr = s.accept()
    print(f"✅ New connection from {addr} as Player {player_count}")
    thread = threading.Thread(target=threaded_client, args=(conn, player_count))
    thread.start()
    player_count += 1
