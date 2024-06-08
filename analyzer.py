import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfMerger
import pygetwindow as gw
import pyautogui
from PIL import Image
import threading
import datetime
import os

class networkScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyzer")
        self.root.geometry("225x80")

        self.capture_button = tk.Button(root, text="Analyze", command=self.start_capture)
        self.capture_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_flag = False
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.version_label = tk.Label(root, text="Version 2.1.1a")
        self.version_label.grid(row=1, column=0, columnspan=2)

    def start_capture(self):
        self.stop_flag = False
        self.capture_thread = threading.Thread(target=self.capture_screenshot)
        self.capture_thread.start()
        self.files=[]

    def merge_files(self):
        if not self.files:
            messagebox.showerror("Error", "No files to merge")
            return
        merger = PdfMerger()
        for file in self.files[::-1]:
            merger.append(file)

        now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        merger.write(f"file_m_{now_str}.pdf")
        merger.close()
        print(f"Saved file_m_{now_str}.pdf")
        for file in self.files:
            os.remove(file)
        self.files = []

    def stop(self):
            self.stop_flag = True
            self.merge_files()

    def save_image(self, total_height, images, window_width):
        max_height = 65000
        for i in range(0, len(images), max_height):
            imgs = images[i:i+max_height]
            imgs=imgs[::-1]
            final_height = sum(img.height for img in imgs)
            final_image = Image.new('RGB', (window_width, final_height))
            current_y = 0
            now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            for img in imgs:
                final_image.paste(img, (0, current_y))
                current_y += img.height
            filename=f"file_{now_str}.pdf"
            self.files.append(filename)
            final_image.save(filename, "PDF")
            print(f"Saved {filename}")

    def capture_screenshot(self):
        network_windows = [w for w in gw.getWindowsWithTitle("Whatsapp") if w.visible]
        if not network_windows:
            messagebox.showerror("Error", "network window not found")
            return

        network_window = network_windows[0]
        start_x, start_y = network_window.left, network_window.top
        window_width = network_window.width
        window_height = network_window.height

        scroll_amount = window_height - 220
        total_height = 0
        images = []
        mouse_loc_to_scroll = (network_window.right - window_width // 10, start_y + 200)
        pyautogui.moveTo(*mouse_loc_to_scroll)

        try:
            while not self.stop_flag :
                if total_height < 64000:
                    screenshot = pyautogui.screenshot(region=(start_x, start_y, window_width, window_height))
                    images.append(screenshot)
                    total_height += screenshot.height
                    pyautogui.scroll(scroll_amount)
                    pyautogui.sleep(0.15)
                else:    
                    self.save_image(total_height, images, window_width)
                    total_height = 0
                    images = []
                    self.capture_screenshot()
            if images:  # Save remaining images if any
                self.save_image(total_height, images, window_width)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"An error occurred: {e}")
            if images: 
                self.save_image(total_height, images, window_width)

if __name__ == "__main__":
    root = tk.Tk()
    app = networkScreenshotApp(root)
    root.mainloop()
