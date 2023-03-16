import os
import datetime as dt
import threading
import tkinter as tk
from pathlib import Path

import pyjson5
import socketio

import getpass


from modules.chat_data import Message, User

socketio = socketio.Client()

@socketio.on('my_message')
def on_message(data):
    print('I received a message: ', data)

@socketio.event
def connect():
    print('I am connected!')


@socketio.event
def connect_error(data):
    print('Connection Error: ', data)


def socksy_emit_authenticate(username, password):
    socketio.emit('socksy_authenticate', data=(username, password))

@socketio.event
def disconnect():
    print('Disconnected')

@socketio.on('message')
def handle_message(data):
    print('received message: ', data)



# set up initial state
USERNAME = getpass.getuser() # Even Python suggest not using getlogin()
CURRENT_USER = User(USERNAME, dt.datetime.now())

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


class Root(tk.Tk):
    """
    Main object which handles all frames (current display of widgets) for window
    """

    def set_from_json(self, style: dict):
        DEFAULT_STYLE = {
            "fg": "white",
            "bg": "#263238",
            "width": 600,
            "height": 400,
            "message_frame_style": {
                "fg": "white",
                "bg": "#263238"
            },
            "message_input_box_style": {
                "fg": "white",
                "bg": "white",
                "input_box_style": {
                    "fg": "black",
                    "bg": "white"
                }
            }
        }
        for key, val in DEFAULT_STYLE.items():
            DEFAULT_STYLE[key] = style.get(key, val)

        self.__dict__.update(**DEFAULT_STYLE)

    def __init__(self, style):

        tk.Tk.__init__(self)

        # set instance variables from JSon
        self.set_from_json(style)
        self.configure(bg=self.bg)
        self.geometry(f"{self.width}x{self.height}")
        # self.resizable(0, 0)

        self.message_frame = MessageFrame(self, self.message_frame_style)
        self.message_input_frame = MessageInputFrame(self, self.message_input_box_style, self.send_input_msg)

        self.message_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.message_input_frame.pack(fill='x', expand=True, anchor='s', padx=10, pady=10)

        self.bind('<Return>', self.message_input_frame.enter_key_pressed)

    def send_input_msg(self):
        message_content = self.message_input_frame.retrieve_and_clear()
        if message_content and not message_content.isspace():
            message = Message(message_content, CURRENT_USER, dt.datetime.now())
            self.message_frame.add_msg(message)


class MessageFrame(tk.Frame):

    def set_from_json(self, style: dict):
        DEFAULT_STYLE = {
            "fg": "white",
            "bg": "#263238"
        }
        for key, val in DEFAULT_STYLE.items():
            DEFAULT_STYLE[key] = style.get(key, val)

        self.__dict__.update(**DEFAULT_STYLE)

    def __init__(self, parent, style: dict, messages: list[Message] = [], refresh_command=None):
        self.parent = parent
        self.set_from_json(style)
        tk.Frame.__init__(self, self.parent, bg=self.bg)

        self.refresh_command = refresh_command

        # display all flashcard sets for selection
        self.scrollable_item_selection = tk.Frame(self, width=400, height=600, bg='white')
        self.scrollable_canvas = tk.Canvas(self.scrollable_item_selection, bg=self.bg, highlightthickness=0, width=400)
        self.item_selection_scrollbar = tk.Scrollbar(self.scrollable_item_selection, orient='vertical',
                                                     command=self.scrollable_canvas.yview, bg=self.bg)

        # create a frame for the scrollable items to exist in and bind it to a command which changes their position as the scrollbar moves
        self.scrollable_items_frame = tk.Frame(self.scrollable_canvas, width=0, height=0, bg=self.bg)
        self.scrollable_items_frame.bind("<Configure>", lambda e: self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all")))

        # set up the scrolling canvas in the
        self.scrollable_canvas.create_window((0, 0), window=self.scrollable_items_frame, anchor="nw")
        self.scrollable_canvas.config(yscrollcommand=self.item_selection_scrollbar.set)

        self.msg_labels = []

        self.messages = messages
        self.update_msgs()

    def update_msgs(self):
        for msg in self.messages:
            self.add_msg(msg)

    def add_msg(self, msg: Message):
        msg_label = tk.Label(self,
                             text=str(msg),
                             foreground='white',
                             bg=self.bg,
                             font=('consolas', 15, 'normal')
                             )
        msg_label.grid(row=len(self.msg_labels), column=0, sticky=tk.W)
        self.msg_labels.append(msg_label)


class MessageInputFrame(tk.Frame):

    def set_from_json(self, style: dict):
        DEFAULT_STYLE = {
            "fg": "white",
            "bg": "white",
            "input_box_style": {
                "fg": "black",
                "bg": "white"
            }
        }
        for key, val in DEFAULT_STYLE.items():
            DEFAULT_STYLE[key] = style.get(key, val)

        self.__dict__.update(**DEFAULT_STYLE)

    def __init__(self, parent, style: dict, send_button_command):
        self.parent = parent
        self.send_button_command = send_button_command
        self.set_from_json(style)
        tk.Frame.__init__(self, self.parent, bg=self.bg)

        self.text = tk.StringVar()

        self.input_box = tk.Text(self, height=1, fg=self.input_box_style['fg'], bg=self.input_box_style['bg'],
                                 insertbackground=self.input_box_style['fg'],
                                 font=('consolas', 15, 'normal'))

        self.send_button = tk.Button(self, text='>', width=5, foreground='white', background='grey25', command=self.send_button_press,
                                     font=('consolas', 15, 'bold'))
        self.input_box.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        self.send_button.grid(row=0, column=1, sticky='e', padx=10, pady=10)

        self.columnconfigure(0, weight=8)
        self.columnconfigure(1, weight=2)

    def enter_key_pressed(self, event):
        self.send_button_press()

    def send_button_press(self):
        self.send_button_command()

    def retrieve_and_clear(self) -> str:
        content = self.input_box.get("1.0", tk.END)
        self.input_box.delete("1.0", tk.END)
        return content

def socketio_connect_thread(coonectionString: str):

    print('Attempting to connect socketio')
    socketio.connect(coonectionString)


if __name__ == '__main__':
    socketio_connection = threading.Thread(target=socketio_connect_thread, args='http://localhost:6000')
    socketio_connection.start()

    style_data = {}

    style_file = Path().cwd() / 'socksy' / 'tk_interface_style.json'
    if style_file.exists():
        print(f"File {style_file.name} exists. Using its style.")
        with open(style_file, 'r') as fp:
            style_data = pyjson5.decode_io(fp)
    root = Root(style_data)
    root.lift()
    root.message_frame.messages = messages
    root.message_frame.update_msgs()

    root.update()

    root.mainloop()


