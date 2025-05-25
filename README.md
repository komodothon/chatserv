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

