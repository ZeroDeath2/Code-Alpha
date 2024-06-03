import tkinter as tk
from time import localtime
from tkinter import messagebox
import pygetwindow as gw
import pyautogui
from PIL import Image
import threading
import datetime

class WhatsAppScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Tool")
        self.root.geometry("200x100")
        self.capture_button = tk.Button(root, text="Analyze", command=self.start_capture)
        self.capture_button.pack(padx=10, pady=10)
        self.stop_flag = False
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(padx=10, pady=10)

    def start_capture(self):
        self.stop_flag = False
        self.capture_thread = threading.Thread(target=self.capture_screenshot)
        self.capture_thread.start()

    def stop(self):
        self.stop_flag = True

    def save_image(self, current_y, images, window_width):
        final_image = Image.new('RGB', (window_width, current_y))
        current_y = 0
        for img in images:
            final_image.paste(img, (0, current_y))
            current_y += img.height
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        final_image.save(f"temp{now_str}.pdf","PDF")
        print(f"Scrolling screenshot saved as temp{now_str}.pdf")

    def capture_screenshot(self):
        whatsapp_windows = [w for w in gw.getWindowsWithTitle("WhatsApp") if w.visible]
        if not whatsapp_windows:
            root = tk.Tk()
            root.withdraw()  
            messagebox.showerror("Error", "WhatsApp window not found") 
            return

        whatsapp_window = whatsapp_windows[0]

        start_x = whatsapp_window.left
        start_y = whatsapp_window.top
        end_x = whatsapp_window.right
        end_y = whatsapp_window.bottom
        window_height = end_y - start_y
        window_width = end_x - start_x
        scroll_amount = int(window_height - 110)
        current_y = start_y
        images = []
        mouse_loc_to_scroll = (end_x - window_width // 10, start_y + 200)
        pyautogui.moveTo(*mouse_loc_to_scroll)

        try:
            while True:
                if self.stop_flag:
                    print("Capture stopped by user")
                    self.save_image(current_y, images, window_width)
                    break

                screenshot = pyautogui.screenshot(region=(start_x, start_y, window_width, window_height))
                images.append(screenshot)
                current_y += screenshot.height
                pyautogui.scroll(scroll_amount)

        except KeyboardInterrupt:
            print("Loop interrupted by user")
            self.save_image(current_y, images, window_width)

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppScreenshotApp(root)
    root.mainloop()
