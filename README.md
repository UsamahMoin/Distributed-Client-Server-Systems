# Distributed Client-Server System

This project implements a distributed client-server system where multiple clients can interact with servers to perform various tasks. The servers handle client requests, process events, and communicate with each other to maintain system synchronization.

## Project Structure

The project consists of the following files:
- `client.py`
- `server.py`
- `server_fns.py`
- `Sync.py`

### File Descriptions

#### client.py
This file contains the client implementation that connects to the servers, sends requests, and processes responses. Clients simulate actions and send them to the server for processing.

#### server.py
This file contains the server implementation that handles client requests and processes events. The server also communicates with other servers to ensure synchronization across the distributed system.

#### server_fns.py
This file contains the functions used by the server to handle client requests, process events, and maintain the state of the server.

#### Sync.py
This file is responsible for synchronizing events across different servers in the distributed system. It ensures that all servers are up-to-date with the latest state and events.

## How to Run

To run the project, follow these steps:

1. **Ensure you have Python installed on your system.**

2. **Run each server instance in separate terminal windows or tabs:**
   ```bash
   python server.py --port <port_number>
