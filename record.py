import tkinter as tk
import threading

import cv2
import pyautogui
import pyaudio
import wave
from datetime import datetime
import numpy as np
import os
import subprocess


class ScreenRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("屏幕录制")
        self.root.geometry("250x250")

        self.is_recording = False

        self.start_button = tk.Button(self.root, text="开始录制", width=10, command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="停止录制", width=10, command=self.stop_recording)
        self.stop_button.pack(pady=5)
        self.stop_button.config(state=tk.DISABLED)

        self.open_folder_button = tk.Button(self.root, text="打开文件夹", width=10, command=self.open_folder)
        self.open_folder_button.pack(pady=5)

        self.open_folder_button = tk.Button(self.root, text="关于", width=10, command=self.about)
        self.open_folder_button.pack(pady=5)

        self.root.mainloop()

    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        now = datetime.now()
        folder_name = now.strftime("%Y%m%d_%H%M%S")
        os.makedirs("videos/" + folder_name)

        threading.Thread(target=self.record_screen, args=(folder_name,)).start()
        threading.Thread(target=self.record_audio, args=(folder_name,)).start()

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def open_folder(self):
        folder_path = os.path.abspath("videos")
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')

    def record_screen(self, folder_name):
        screen_width, screen_height = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = 30  # 帧速率
        output_filename = f"videos/{folder_name}/screen.mp4"
        out = cv2.VideoWriter(output_filename, fourcc, fps, (screen_width, screen_height))

        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

        out.release()

    def record_audio(self, folder_name):
        output_filename = f"videos/{folder_name}/audio.wav"
        fps = 30  # 帧速率
        fs = fps * 1024  # 采样率

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16, channels=2, rate=fs, input=True, frames_per_buffer=1024)

        frames = []
        while self.is_recording:
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def about(self):
        about_window = tk.Toplevel()
        about_window.title("关于")
        about_window.geometry("300x150")

        # 显示应用程序名称、版本号和开发者信息
        app_name_label = tk.Label(about_window, text="屏幕录制")
        app_name_label.pack(pady=10)

        version_label = tk.Label(about_window, text="版本号：0.2")
        version_label.pack()

        developer_label = tk.Label(about_window, text="开发者：pigeons2023")
        developer_label.pack()

if __name__ == "__main__":
    ScreenRecorder()
