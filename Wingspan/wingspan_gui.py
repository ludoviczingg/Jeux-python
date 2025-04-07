import tkinter as tk
from game_classes import Game

class WingspanApp(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Wingspan - Démo")
        self.geometry("800x600")
        self.game = game
        self.selected_bird = None

        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        tk.Label(self, text="Main du joueur", font=("Arial", 18)).pack(pady=10)

        self.hand_frame = tk.Frame(self)
        self.hand_frame.pack(pady=10)

        self.info_label = tk.Label(self, text="", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.play_button = tk.Button(self, text="Jouer l'oiseau sélectionné", command=self.play_selected_bird)
        self.play_button.pack(pady=10)

    def update_ui(self):
        for widget in self.hand_frame.winfo_children():
            widget.destroy()

        for bird in self.game.current_player.hand:
            btn = tk.Button(self.hand_frame, text=bird.name, width=20,
                            command=lambda b=bird: self.select_bird(b))
            btn.pack(side="left", padx=5)

        if self.selected_bird:
            self.info_label.config(text=f"Sélectionné : {self.selected_bird.name}")
        else:
            self.info_label.config(text="Aucun oiseau sélectionné")

    def select_bird(self, bird):
        self.selected_bird = bird
        self.update_ui()

    def play_selected_bird(self):
        if self.selected_bird:
            self.game.current_player.play_bird(self.selected_bird)
            self.selected_bird = None
            self.update_ui()
        else:
            self.info_label.config(text="Veuillez sélectionner un oiseau")

if __name__ == "__main__":
    game = Game(["Alice"])
    app = WingspanApp(game)
    app.mainloop()