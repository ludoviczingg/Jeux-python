from bird_loader import load_birds_from_excel
from bird import Bird

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def play_bird(self, bird):
        if bird in self.hand:
            self.hand.remove(bird)
            print(f"{self.name} a joué {bird.name}")
        else:
            print("Oiseau non disponible")

class Game:
    def __init__(self, player_names):
        print("init game :")
        self.players = [Player(name) for name in player_names]
        self.current_player = self.players[0]
        self.bird_deck = load_birds_from_excel("Wingspan/wingspan/wingspan.xlsx")
        print(self.bird_deck)
        
        oiseau=self.bird_deck.pop()
        print(type(oiseau))
        print(oiseau.common_name)

        
        #self.init_birds()

    def distribute_initial_hand(self):    
        
        self.current_player.hand = self.bird_deck[:3]
        print(self.current_player)