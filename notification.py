from plyer import notification
import datetime
import time
import ctypes
from pystray import Icon, MenuItem as item
from PIL import Image
from threading import Thread, Event
import pygame
#import tkinter as tk

class CustomNotification:
    def __init__(self, title, message, hour, minute):
        self.title = title
        self.message = message
        self.hour = hour
        self.minute = minute

def show_notification(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 1)

class App:
    def __init__(self):
        self.exit_event = Event()
        self.notifications = []
        menu = (item('SUPER stupid Notifications', self.click), item('Close', self.exit_program))
        self.icon = Icon("name", Image.open("assets/icon.png"), "SUPER stupid Notifications", menu=menu)
        pygame.init()

    def add_notification(self, title, message, hour, minute):
        #title = input("Title: ")
        #message = input("Message: ")
        #hour = int(input("Hour (0-23): "))
        #minute = int(input("Minute (0-59): "))
        new_notification = CustomNotification(title, message, hour, minute)
        self.notifications.append(new_notification)

    def show_notification(self, title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 1)

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def exit_program(self, icon, item):
        print("Exitting, whait a moment...")
        self.exit_event.set()
        icon.stop()

    def click(self, icon, item):
        print("I literally do nothing.")

    def check_notifications(self):
        while not self.exit_event.is_set():
            current_time = datetime.datetime.now()
            for notification in self.notifications:
                if current_time.hour == notification.hour and current_time.minute == notification.minute:
                    self.play_sound("assets/alert.mp3")
                    self.show_notification(notification.title, notification.message)
            time.sleep(10)

    def main(self):
        while True:
            self.add_notification(input("Title: "), input("Message: "), int(input("Hour (0-23): ")), int(input("Minute (0-59): ")))
            add_more = input("Do you want to add more notifications? (y/n): ")
            if add_more.lower() != 'y':
                break
        notifications_thread = Thread(target=self.check_notifications)
        notifications_thread.start()
        self.icon.run()

if __name__ == "__main__":
    app = App()
    app.main()
