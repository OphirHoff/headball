# Headball

A Python-based recreation of the popular "Headball2" game using UDP sockets for real-time multiplayer functionality.

## Description

Headball is a multiplayer game where two players control characters that hit a ball into their opponent's goal. This version implements the game in Python, utilizing UDP sockets to facilitate real-time player communication and synchronization over a network.

## Features

- Real-time multiplayer using UDP sockets
- Physics-based ball movement and player interaction
- Simple 2D graphics for game visualization
- Server-clients matchmaking architecture for online gameplay

## Technologies Used

- **Python 3.10.11**
- **UDP sockets**
- **Pygame** (for graphics and game mechanics)
- **Multithreading** (for server-clients communication)

## Installation

### Prerequisites

1. Python 3.x installed on your system.
2. Pygame library (can be installed using `pip install pygame`).

### Clone the repository

```bash
git clone https://github.com/ophirhoff/headball.git
cd headball
```


## Usage
### Setting up the network
Inside `server.py` change the `ip` variable to server's local IP address (currently `127.0.0.1`).

### Starting the Server
```
py server.py
```

### Starting the Client
```
py client.py
```

From there, follow the game intuitive GUI and most importantly - have fun!

## Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request with a description of the changes. Ensure that any new features or bug fixes are accompanied by appropriate tests.
