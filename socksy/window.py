"""
Contains the main window for the client
"""

# Standard library imports
import datetime as dt
import threading
import tkinter as tk
from pathlib import Path

# Third-party Imports
import pyjson5
import socketio

# Local Imports
import socksy_client
from modules.chat_data import Message, User


class Root(tk.Tk):
    """
    Main object which handles all frames (current display of widgets) for window
    """

    def set_from_json(self, style: dict):
        class Style:
            pass
        self.style = Style()
        DEFAULT_STYLE = {
            "light_shades": "#1c1c1c",
            "light_accent": "white",
            "light_primary": "white",
            "dark_accent": "grey5",
            "dark_shades": "grey25",
            "width": 1000,
            "height": 600,
            "primary_font": ["consolas", 15, "normal"],
            "bold_font": ["consolas", 15, "bold"],
        }

        for key, val in DEFAULT_STYLE.items():
            DEFAULT_STYLE[key] = style.get(key, val)
            self.style.__setattr__(key, DEFAULT_STYLE[key])

        # self.style.__dict__.update(**DEFAULT_STYLE)

    def __init__(self, style, message_send_command, tick_interval: int = 200):

        tk.Tk.__init__(self)
        self.message_send_command = message_send_command
        self.tick_interval = tick_interval

        # set instance variables from JSon
        self.set_from_json(style)
        self.configure(bg=self.style.dark_shades)
        self.geometry(f"{self.style.width}x{self.style.height}")
        # self.resizable(0, 0)

        self.message_frame = MessageFrame(self, self.style)
        self.message_input_frame = MessageInputFrame(self, self.style, self.send_input_msg)

        # sticky = 'nwes' means that the widget will expand to fill the entire cell
        self.message_frame.grid(row=0, column=0, sticky='nwes', padx=10, pady=10)
        self.message_input_frame.grid(row=1, column=0, sticky='nwes', padx=10, pady=10)

        self.rowconfigure(0, weight=9)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.bind('<Return>', self.message_input_frame.enter_key_pressed)

        self.tick()  # Function that continually checks the queue for new messages

    def send_input_msg(self):
        message_content = self.message_input_frame.pop_entry_content()
        if message_content and not message_content.isspace():
            message = Message(message_content, socksy_client.CURRENT_USER, dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # XXX: Sending message to server here
            self.message_send_command(message.sender.name, message.content, message.sent_at)
            # self.message_frame.add_msg(message)

    def tick(self):
        if not socksy_client.MESSAGE_QUEUE.empty():
            message = socksy_client.MESSAGE_QUEUE.get(timeout=3)
            self.message_frame.add_msg(message)
        self.message_frame.update_msgs()
        self.after(self.tick_interval, self.tick)


class MessageFrame(tk.Frame):
    """ Frame that contains the list of messages

    Attributes:
        parent (tk.Tk): Parent object
        style (dict): Dictionary containing styling data for window e.g. colors, fonts
        refresh_command (function, optional): Function to be called when the message frame is refreshed. Defaults to None.
        msg_list (tk.Listbox): Listbox that contains the messages
        scrollbar (tk.Scrollbar): Scrollbar for the message listbox
        messsages (list[Message]): List of messages to be displayed in the message frame
        
    Methods:
        update_msgs: Clear the message frame and populate it based on current value of self.messages
        add_msg (Message): Add a message to the message frame. Adds to self.messages and updates the window.
        clear: Clear all currently displayed messages
    """

    def __init__(self, parent, style: dict, messages: list[Message] = [], refresh_command=None, **kwargs):
        self.parent = parent
        self.style = style
        tk.Frame.__init__(self, self.parent, bg=self.style.dark_shades, **kwargs)

        self.refresh_command = refresh_command

        self.msg_list = tk.Listbox(self,
                                   relief='flat',
                                   highlightthickness=0,
                                   bg=self.style.dark_shades,
                                   fg=self.style.light_primary,
                                   selectbackground=self.style.dark_shades,
                                   selectforeground=self.style.light_primary,
                                   font=self.style.primary_font)

        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.msg_list.yview)
        self.scrollbar.pack(side='right', fill='y')
        
        self.msg_list.config(yscrollcommand=self.scrollbar.set)
        self.msg_list.pack(side=tk.LEFT, fill="both", expand=True)

        self.messages = messages
        self.update_msgs()

    def update_msgs(self):
        """ Updates the messages in the message frame
        New single messages can be added with the add_msg method
        """
        self.clear()
        for msg in self.messages:
            self.add_entry(str(msg))

    def add_entry(self, entry: str):
        """ Adds a string to the message frame

        Args:
            entry (str): String to be added to the message frame
        """
        self.msg_list.insert(tk.END, entry)
        self.msg_list.yview_moveto(1)

    def add_msg(self, msg: Message):
        """ Adds a message to the message frame

        Args:
            msg (Message): Message to be added to the message frame
        """
        self.msg_list.insert(tk.END, str(msg))
        self.msg_list.yview_moveto(1)
        self.messages.append(msg)

    def clear(self):
        self.msg_list.delete(0, "end")


class MessageInputFrame(tk.Frame):

    def __init__(self, parent, style: dict, send_button_command):
        self.parent = parent
        self.send_button_command = send_button_command
        self.style = style
        tk.Frame.__init__(self, self.parent, bg=self.style.dark_accent)

        self.text = tk.StringVar()

        self.input_box = tk.Text(self,
                                 height=1,
                                 fg=self.style.light_accent,
                                 bg=self.style.dark_shades,
                                 insertbackground=self.style.light_primary,
                                 font=self.style.primary_font,
                                 highlightthickness=1)

        self.send_button = tk.Button(self,
                                     text='>',
                                     width=5,
                                     foreground=self.style.light_primary,
                                     background=self.style.dark_shades,
                                     command=self.send_button_press,
                                     font=self.style.bold_font,
                                     highlightthickness=1)
        self.input_box.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.send_button.grid(row=0, column=1, sticky='we', padx=10, pady=10)

        self.columnconfigure(0, weight=8)
        self.columnconfigure(1, weight=2)

    def enter_key_pressed(self, event):
        self.send_button_press()

    def send_button_press(self):
        self.send_button_command()

    def pop_entry_content(self) -> str:
        content = self.input_box.get("1.0", tk.END)
        self.input_box.delete("1.0", tk.END)
        return content
