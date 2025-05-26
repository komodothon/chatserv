# 🗨️ Private Python Chat Server

A simple yet powerful multi-client chat system built with Python, perfect for family and friends. Hosted on your own Oracle Cloud (OCI) VM, it acts like your personal WhatsApp — only more private, and fully in your control.

---

## 🧠 Concept

Unlike basic tools like `nc` (netcat) which allow point-to-point connections, this system builds a true **group chat server** that:

- Accepts **multiple clients**
- **Broadcasts** messages to all other connected clients
- Uses **TCP sockets** for reliable delivery
- Handles each client using **Python threading**

This makes it behave like a private chat room — available 24/7 to just your inner circle.

---

## ⚙️ Working Principle

### Roles

- **Server**: Listens for connections, receives messages, and broadcasts to all.
- **Clients**: Connect to the server, send messages, and receive messages from others.

### Data Flow Diagram


### Under the Hood

- Server binds to a host and port using TCP.
- Each incoming client is handled in its own thread.
- When a message is received from any client:
  - Server broadcasts it to **all other clients**.

---

## ✅ Core Goals

| Feature                 | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| Private Chat Server    | Runs on your Oracle Cloud VM (OCI)                                          |
| Multiple Clients        | Connect from Ubuntu, Arch, Android (Termux), Windows, etc.                 |
| Access Control          | Only known users (family, friends) can connect                             |
| Always-On               | The server runs 24/7 on your public VM                                     |
| Simple Clients          | Start with terminal-based clients, later add GUI or mobile apps            |
| Upgradeable             | Add features like login, encryption, web chat, etc.                         |

---

## 🏗️ Phase-by-Phase Breakdown

### 🧱 Phase 1: Basic Functioning (Local Test)

- **Server**
  - Listens on a port and accepts TCP clients
  - Broadcasts messages to all others
- **Client**
  - Connects to the server
  - Sends and receives messages

✅ _You already have this working!_

---

### 🌍 Phase 2: Move to Cloud (OCI VM)

1. Copy `chat_server.py` to your OCI VM.
2. Run it with:

```bash
python3 chat_server.py
```

### Phase 3: Secure the Server (Access Control)
  Create a users.json or .env-based password file

  On connection, clients send username + password
  
  Server authenticates users

  Optional Enhancements:

  - ✅ IP whitelisting (e.g., only your home IP)

  - ✅ Encrypt communication (using TLS sockets)

### 🧼 Phase 4: Polish It
Prefix messages with usernames: [Joshna] Hello

Add timestamps

Colored terminal output (e.g., using colorama)

Auto-reconnect on network failure

### 🧑‍💻 Phase 5: Build Custom Client
Terminal client → GUI (with Tkinter or PyQt)

Android app (Termux, Kivy, or React Native)

Web client (Flask + WebSockets or socket.io)

🔐 Privacy First
This chat server can be built to respect your privacy:

🔒 No third-party logging

💾 Optional message deletion after 1-2 days

✉️ You control who joins and what is stored

You own it. You host it. You decide what to keep.

