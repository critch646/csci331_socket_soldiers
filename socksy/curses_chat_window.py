import os
import curses
import datetime as dt

from modules.chat_data import User, Message


# initialize curses
stdscr = curses.initscr()
# curses.noecho()
curses.cbreak()
curses.curs_set(False)

if curses.has_colors():
    curses.start_color()
    curses.use_default_colors()
    # set up color pairs
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)

stdscr.keypad(True)


def close():
    curses.nocbreak()
    curses.echo()
    curses.curs_set(True)
    stdscr.keypad(False)
    curses.endwin()
    exit()


# define functions for drawing messages and users
def draw_messages(messages, height, width, scroll_pos):
    message_win = curses.newwin(height-2, width, 0, 0)
    message_win.scrollok(True)
    message_win.idlok(True)
    message_win.addstr(0, 0, "Messages", curses.A_BOLD)
    for i, message in enumerate(messages[-scroll_pos:]):
        message_win.addstr(i+1, 0, f"{message.content} ({message.sender}): {message.time_str()}")
    message_win.refresh()


def draw_users(users, height, width):
    user_win = curses.newwin(height-2, width, 0, width)
    user_win.addstr(0, 0, "Users", curses.A_BOLD)
    for i, user in enumerate(users):
        status = "online" if user.online else "offline"
        user_win.addstr(i+1, 0, f"{user.name} ({status})", curses.color_pair(2 if user.online else 1))
    user_win.refresh()


# define function for handling commands
def handle_command(command, user):
    global messages, users, scroll_pos
    if command.startswith(":msg"):
        message_text = command.split(" ", 1)[1]
        messages.append({"sender": user, "time": dt.datetime.now().strftime("%H:%M"), "text": message_text})
    elif command == ":exit":
        close()
        # curses.endwin()
    scroll_pos = 0
    stdscr.clear()


# set up initial state
user = os.getlogin()

user_dict = {
    'bob': User('Bob', dt.datetime.now()),
    'alice': User('Alice', dt.datetime.now())
}

users = list(user_dict.values())

messages = [
    Message("Hello world!", user_dict['alice'],    "10:33am"),
    Message("Hi Alice.",    user_dict['bob'],      "10:33am"),
    Message("How are you?", user_dict['alice'],    "10:33am"),
    Message("I'm good, thanks.", user_dict['bob'], "10:33am"),
    Message("bye", user_dict['bob'], "10:33am")
]

max_y, max_x = stdscr.getmaxyx()
messages_height = max_y - 1
messages_width = max_x // 2
users_height = max_y - 1
users_width = max_x // 2
scroll_pos = 0


try:
    # initialize screen content
    draw_messages(messages, messages_height, messages_width, scroll_pos)
    draw_users(users, users_height, users_width)
    stdscr.refresh()
    # main loop
    while True:
        # draw messages and users
        draw_messages(messages, messages_height, messages_width, scroll_pos)
        draw_users(users, users_height, users_width)
        stdscr.refresh()
        # get user input
        user_input = stdscr.getstr(max_y-1, 0, max_x-1).decode("utf-8")
        # handle scrolling
        if user_input == "k":
            if scroll_pos < len(messages) - messages_height:
                scroll_pos += 1
        elif user_input == "l":
            if scroll_pos > 0:
                scroll_pos -= 1
        # handle commands or messages
        elif user_input.startswith(":"):
            handle_command(user_input, user)
        elif user_input:
            messages.append({"sender": user, "time": dt.datetime.now().strftime("%H:%M"), "text": user_input})
            scroll_pos = 0
except KeyboardInterrupt:
    # clean up
    close()

    # os._exit(0)
