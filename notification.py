from plyer import notification
import datetime
import time
import ctypes
from pystray import Icon, MenuItem as item
from PIL import Image
from threading import Thread, Event
import pygame
import tkinter as tk

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

        #GUI SETUP
        self.root = tk.Tk()
        self.root.geometry("1280x720")
        self.root.title("SUPER stupid Notifications")
        self.root.configure(bg='#282A36')
        self.root.iconbitmap('assets/icon.ico')

        self.title_label = tk.Label(self.root, text="Title", bg='#282A36', fg='#FFFFFF')
        self.title_entry = tk.Entry(self.root, bg='#2d2f3d', fg='#FFFFFF')
        self.message_label = tk.Label(self.root, text="Message", bg='#282A36', fg='#FFFFFF')
        self.message_entry = tk.Entry(self.root, bg='#2d2f3d', fg='#FFFFFF')
        self.hour_label = tk.Label(self.root, text="Hour", bg='#282A36', fg='#FFFFFF')
        self.hour_entry = tk.Entry(self.root, bg='#2d2f3d', fg='#FFFFFF')
        self.minute_label = tk.Label(self.root, text="Minute", bg='#282A36', fg='#FFFFFF')
        self.minute_entry = tk.Entry(self.root, bg='#2d2f3d', fg='#FFFFFF')
        self.add_button = tk.Button(self.root, text="Add Notification", command=self.add_notification_gui,bg='#a8536c', fg='#FFFFFF')
        self.close_button = tk.Button(self.root, text="Continue", command=self.root.destroy, bg='#34b3b3', fg='#FFFFFF')

        self.frame = tk.Frame(self.root, bg='#282A36')
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL,  bg='#282A36')
        self.notification_listbox = tk.Listbox(self.frame, xscrollcommand=self.scrollbar.set, width=200, bg='#2d2f3d', fg='#FFFFFF')
        self.listbox_label = tk.Label(self.frame, text="This notifications will be added:", bg='#282A36', fg='#FFFFFF')
        #GUI DISPLAY
        self.title_label.pack()
        self.title_entry.pack()
        self.message_label.pack()
        self.message_entry.pack()
        self.hour_label.pack()
        self.hour_entry.pack()
        self.minute_label.pack()
        self.minute_entry.pack()
        self.add_button.pack(pady=(5, 0))
        self.close_button.pack(pady=(10, 0))
        self.frame.pack()
        self.scrollbar.config(command=self.notification_listbox.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox_label.pack(pady=(50, 0))
        self.notification_listbox.pack(expand=True)


    def add_notification_gui(self):
        title = self.title_entry.get()
        message = self.message_entry.get()
        hour = int(self.hour_entry.get())
        minute = int(self.minute_entry.get())
        self.add_notification(title, message, hour, minute)
        notification_str = f"Title: {title}, Message: {message}, Hour: {hour}:{minute}"
        self.notification_listbox.insert(tk.END, notification_str)
        

    def add_notification(self, title, message, hour, minute):
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
            time.sleep(60)

    def main(self):
        self.root.mainloop()
        notifications_thread = Thread(target=self.check_notifications)
        notifications_thread.start()
        self.icon.run()

if __name__ == "__main__":
    app = App()
    app.main()
