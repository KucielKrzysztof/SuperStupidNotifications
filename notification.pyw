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
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)

class App:
    def __init__(self):
        self.exit_event = Event()
        self.notifications = []
        menu = (item('SUPER stupid Notifications', self.click), item('Close', self.exit_program))
        self.icon = Icon("name", Image.open("assets/icon.png"), "SUPER STUPID NOTIFICATIONS", menu=menu)
        pygame.init()

        #GUI SETUP
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.real_exit)
        self.root.geometry("1280x720")
        self.root.title("SUPER stupid Notifications")
        self.root.configure(bg='#282A36')
        self.root.iconbitmap('assets/icon.ico')
        self.frame2 = tk.Frame(self.root, bg='#282A36')
        self.frame = tk.Frame(self.root, bg='#282A36')

        self.main_label = tk.Label(self.root, text="SUPER STUPID NOTIFICATIONS", bg='#282A36', fg='#34b3b3', font=("Helvetica", 20))
        self.title_label = tk.Label(self.root, text="Title", bg='#282A36', fg='#FFFFFF')
        self.title_entry = tk.Entry(self.root, bg='#2d2f3d', fg='#FFFFFF', width=50)
        self.message_label = tk.Label(self.root, text="Message", bg='#282A36', fg='#FFFFFF')
        self.message_entry = tk.Text(self.root, bg='#2d2f3d', fg='#FFFFFF', width=70, height=10)
        self.hour_label = tk.Label(self.root, text="Input Time:", bg='#282A36', fg='#FFFFFF')
        self.minute_label = tk.Label(self.root, text="Hour: (0-23): Minute: (0-59)", bg='#282A36', fg='#FFFFFF')
        self.add_button = tk.Button(self.root, text="Add Notification", command=self.add_notification_gui,bg='#a8536c', fg='#FFFFFF',  height=1, width=15)
        self.close_button = tk.Button(self.root, text="Continue", command=self.root.destroy, bg='#34b3b3', fg='#FFFFFF',height=1, width=15)
        self.hour_entry = tk.Entry(self.frame2, bg='#2d2f3d', fg='#FFFFFF', width=8)
        self.minute_entry = tk.Entry(self.frame2, bg='#2d2f3d', fg='#FFFFFF', width=8)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL,  bg='#282A36')
        self.notification_listbox = tk.Listbox(self.frame, xscrollcommand=self.scrollbar.set, width=200, bg='#2d2f3d', fg='#FFFFFF')
        self.listbox_label = tk.Label(self.frame, text="This notifications will be added:", bg='#282A36', fg='#FFFFFF')


        #GUI DISPLAY
        self.main_label.pack(pady=(10, 0))
        self.title_label.pack()
        self.title_entry.pack()
        self.message_label.pack()
        self.message_entry.pack()
        self.hour_label.pack()
        self.minute_label.pack()
        self.frame2.pack()
        self.hour_entry.grid(row=0, column=0)
        self.minute_entry.grid(row=0, column=1)
        self.add_button.pack(pady=(5, 0))
        self.close_button.pack(pady=(10, 0))
        self.frame.pack()
        self.scrollbar.config(command=self.notification_listbox.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox_label.pack(pady=(50, 0))
        self.notification_listbox.pack(expand=True)


    def add_notification_gui(self):
        title = self.title_entry.get()
        message = self.message_entry.get("1.0","end-1c" )
        hour = int(self.hour_entry.get())
        minute = int(self.minute_entry.get())
        self.add_notification(title, message, hour, minute)
        notification_str = f"Title: {title} || Message: {message.replace('\n', ' ')}|| Hour: {hour}:{minute}"
        self.notification_listbox.insert(tk.END, notification_str)
        if self.notification_listbox.size() % 2 == 0:
            self.notification_listbox.itemconfig(tk.END, {'bg':'#41445a'})
        else:
            self.notification_listbox.itemconfig(tk.END, {'bg':'#303034'})
        

    def add_notification(self, title, message, hour, minute):
        new_notification = CustomNotification(title, message, hour, minute)
        self.notifications.append(new_notification)

    def show_notification(self, title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 0+48)

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def exit_program(self, icon, item):
        print("Exitting, whait a moment...")
        self.exit_event.set()
        icon.stop()

    def real_exit(self):
        self.exit_event.set()
        self.root.destroy()

    def click(self, icon, item):
        print("I literally do nothing.")

    def check_notifications(self):
        while not self.exit_event.is_set():
            current_time = datetime.datetime.now()
            for notification in self.notifications:
                if current_time.hour == notification.hour and current_time.minute == notification.minute:
                    self.play_sound("assets/alert.mp3")
                    self.show_notification(notification.title, notification.message)
                    self.notifications.remove(notification)

            time.sleep(10)

    def start_threads(self):
        notifications_thread = Thread(target=self.check_notifications)
        notifications_thread.start()
        icon_thread = Thread(target=self.icon.run)
        icon_thread.start()

    def main(self):
        self.start_threads()
        self.root.mainloop()



if __name__ == "__main__":
    app = App()
    app.main()
