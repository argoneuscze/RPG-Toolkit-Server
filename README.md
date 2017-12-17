# RPG Toolkit (Server)

RPG Toolkit is a server-client application meant for easier management and online
running of various role-playing games such as D&D or GURPS. This repository
covers the server part of the project.

## Features

The core part of the server is a **Game**. A game encompasses a variety of rooms,
items found in said rooms, players, player characters, non-player characters, and a log
of interactions between player characters.

The gamemasters have full access to every aspect of the game, and are able to change
any part of it. The players only have access to the room their character is in,
and they may interact with their surroundings and move to other rooms.

The server will allow players and gamemasters (GMs) alike to connect to it using
a simple WebSocket protocol and identify as such using pre-determined passwords.

## License

This server is licensed under the [GNU AGPLv3 License](COPYING.md).
