import customtkinter as ctk
import threading
import time

class LoadingIndicator(ctk.CTkFrame):
    def __init__(self, master, text="Loading...", **kwargs):
        super().__init__(master, **kwargs)
        
        # Create and configure the loading animation
        self.dots = 0
        self.running = True
        self.base_text = text
        
        # Create loading label with dots animation
        self.label = ctk.CTkLabel(self, text=self.base_text)
        self.label.pack(padx=20, pady=20)
        
        # Start animation in a separate thread
        self.animation_thread = threading.Thread(target=self._animate)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def _animate(self):
        while self.running:
            self.dots = (self.dots + 1) % 4
            dots_text = "." * self.dots
            self.label.configure(text=f"{self.base_text}{dots_text}")
            time.sleep(0.5)
    
    def stop(self):
        self.running = False
        if self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1.0)
        self.destroy()
