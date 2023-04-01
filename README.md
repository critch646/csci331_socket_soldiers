# Socksy - CSCI331 Team Socket Soliders Project

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This was created for Computer Science (CSCI) 311 (web development) at Vancouver Island University (VIU). It is a simple client/server application which allows users to chat with each other. Each client can communicate with a single running instance of the main server. The server is responsible for ensuring each user has a copy of the chat history.

This was created to be a replacement for the CSCI discord server, acting as a stand-alone application that could be owned and managed by the VIU CSCI department. Running it for this purpose would involve having the main server running on a VIU server. A copy of the client application would then be available on each CSCI student computer, and each user would be logged in with their CSCI account username. Since users need to be logged into a CSCI server to use this application, we can use their account username and avoid the need for separate user accounts.

## Authors
- [Ethan Posner](https://github.com/enprogames)
- [Zeke Critchlow](https://github.com/critch646)
- Brandon Stanton

## Technologies

This project is entirely written in Python. Since the school server requires Python 3.9, we have developed the application to work with this version.

### Socksy Server
- Flask: Acts as central server backend
- SocketIO: Facilitates server-client communications
- mysqlconnector: Facilitates server database communication. Stores chat history and user information. Can be replaced with any other database connector, but will require additional setup.

### Socksy Client

- SocketIO: Facilitates communication with central server
- TKinter: Graphical user interface

## Setup
1. Install [Python 3.9](https://www.python.org/downloads/)
2. Clone this repository: `git@github.com:critch646/csci331_socket_soldiers.git`
3. Create a virtual environment: `python -m venv venv --prompt socksy`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`



## Usage

By default, we are running the server on the "cub13" VIU CSCI server. You can change this by editing the `socksy_server.py` and `socksy_client.py` files.

1. Run the server: `python3 socksy/socksy_server.py`
2. Run the client (on the same machine or another CSCI student server): `python3 socksy/socksy_client.py`
3. Type a message and press enter to send it to the server. The server will then send it to all other connected clients.

## Contributing TODO: Update this section

All changes should be made on a fork of this repository, and then submitted as pull requests to be reviewed by the project maintainers. Below is a detailed list of steps that should help you stay out of trouble when contributing.

1. Move to development branch: `git checkout development`
2. Bring in any changes from upstream: `git pull upstream development --rebase`
    - Rebasing helps keep the commit history clean and linear, avoiding gross merge commits.
3. Create a new branch off of development: `git checkout -b <my-new-changes>`
4. Write code
5. Add changes and commit them:
    - `git add <files>`
    - `git commit -m "<commit message>"`
6. Make sure you're up to date: `git pull upstream development --rebase`
7. Push your changes to your fork: `git push origin <my-new-changes>`
8. Submit a pull request to the development branch of this repository.
    - Any new commits pushed to the `my-new-changes` branch will automatically be put into the merge request while it's open.
    - To change the last commit (if a small mistake was made and an entirely new commit isn't necessary), make your changes, stage them, then run `git amend --no-edit` to add your changes to the previous commit. You'll also have to do a force push after this with `git push origin <branch> -f`, so make sure you know exactly what you're doing!

- If you run into issues at any point, check out this choose your own adventure for resolving issues with git: [sethrobertson.github.io - On undoing, fixing, or removing commits in git](https://sethrobertson.github.io/GitFixUm/fixup.html).

## License
This repository is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). See [LICENSE](LICENSE) for more information.
