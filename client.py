import threading
import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatRoomApp:
    def __init__(self, master):
        self.master = master
        master.title("Chat Room")

        # Entry for entering name
        self.name_label = tk.Label(master, text="Enter your name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        self.name_button = tk.Button(master, text="Submit", command=self.connect_to_server)
        self.name_button.pack()

    def connect_to_server(self):
        name = self.name_entry.get()
        if name:
            # Remove name input elements
            self.name_label.destroy()
            self.name_entry.destroy()
            self.name_button.destroy()
            self.name = name
            try:
                self.initialize_chatroom()
                self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.client.connect(('127.0.0.1', 56789))
                self.client.send(name.encode('utf-8'))
                rthread = threading.Thread(target=self.client_receive)
                rthread.start()
            except Exception as e:
                messagebox.showerror("Error", f"Error connecting to server: {e}")
                self.master.destroy()
    def client_receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == "Ping?":
                    self.client.send(self.name.encode('utf-8'))
                else:
                    self.display_message(message)
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
                self.client.close()
                break
    def initialize_chatroom(self):
        self.spacer = tk.Frame(self.master, height=10)
        self.spacer.pack(side=tk.TOP)
        self.message_frame = tk.Frame(self.master)
        self.message_frame.pack(side=tk.TOP, fill=tk.X,padx=10)

        # Entry for typing messages
        self.message_entry = tk.Entry(self.message_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Button to send messages
        self.send_button = tk.Button(self.message_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT,pady=5)

        self.spacer = tk.Frame(self.master, height=10)
        self.spacer.pack(side=tk.TOP)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.master, state='disabled')
        self.chat_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        welcome_message = "Welcome, " + self.name + "!"
        self.display_message(welcome_message)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.message_entry.delete(0, tk.END)  # Clear the message entry
            full_message = f'{self.name}: {message}'
            self.client.send(full_message.encode('utf-8'))

    def display_message(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.configure(state='disabled')
        # Scroll to the bottom
        self.chat_display.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatRoomApp(root)
    root.mainloop()

