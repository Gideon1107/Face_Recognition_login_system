import os.path
import datetime
import pickle
import subprocess

import tkinter as tk
import tkinter.messagebox as tkmb
import cv2
from PIL import Image, ImageTk
import face_recognition

import util
# from test import test


current_user = ''

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x520+160+100")

        self.main_window.title("Face Recognition Login System")

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login, fg='green')
        self.login_button_main_window.place(x=750, y=320)


        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)
        note_label = tk.Label(self.main_window, text="Note: Look into the camera before clicking the \n'Register' button")
        note_label.config(font=("sans-serif bold", 10), justify="center")
        note_label.place(x=750, y=450)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        global current_user
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(",")[1][:-3]
        current_user = name

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box("Oops....", "Unknown user. Please register new user or try again.")

        else:
            util.msg_box("Success", f"Welcome back {name.title()}")
            self.current_user_dashboard()
            with open(self.log_path, 'a') as f:
                f.write(f"Username: {name} | Login-TIme: {datetime.datetime.now()} \n")
                f.close()

        os.remove(unknown_img_path)


    def current_user_dashboard(self):
        # self.main_window.destroy()
        self.user_dashboard = tk.Tk()
        self.user_dashboard.geometry("1000x520+180+120")
        self.user_dashboard.title("User Dashboard")

        self.dashboard_label = util.get_text_label(self.user_dashboard, 'Welcome to your Dashboard')
        self.dashboard_label.place(x=345, y=120)

        self.logout_button = util.get_button(self.user_dashboard, 'Logout', 'black', self.logout, fg='red')
        self.logout_button.place(x=345, y=300)

        self.user_dashboard.mainloop()


    def logout(self):
        global current_user
        util.msg_box(f'Logout successful!', f'Goodbye {current_user.title()}!.')
        with open(self.log_path, 'a') as f:
            f.write(f"Username: {current_user} | Logout-TIme: {datetime.datetime.now()} \n")
            f.close()
        self.user_dashboard.destroy()
        # self.main_window.destroy()

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1000x520+180+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Continue', 'green', self.accept_register_new_user, fg='green')
        self.accept_button_register_new_user_window.place(x=750, y=330)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user, fg='red')
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Enter Username:')
        self.text_label_register_new_user.place(x=745, y=120)


    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box('Success!', 'User was registered successfully !')
        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
