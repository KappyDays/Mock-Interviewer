import tkinter as tk
from tkinter import filedialog
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("400x150")

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Add a button to load the MP3
        self.load_button = tk.Button(root, text="Load MP3", command=self.load_mp3)
        self.load_button.pack(pady=20)

        # Add a button to play the MP3
        self.play_button = tk.Button(root, text="Play MP3", command=self.play_music)
        self.play_button.pack(pady=20)

        self.filename = None

    def load_mp3(self):
        """Open a file dialog to select an MP3 file."""
        self.filename = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if self.filename:
            print(f"Loaded {self.filename}")

    def play_music(self):
        """Play the selected MP3 file."""
        if self.filename:
            pygame.mixer.music.load(self.filename)
            pygame.mixer.music.play()
            print("Playing Music")
        else:
            print("No file loaded")

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
