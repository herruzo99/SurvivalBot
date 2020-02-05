import yaml
from core.player import Player
from numpy import random
from typing import List


def format_str(frase: str, players: List[Player]):
    return "- " + frase.format(*players)


class GameEngine:
    sucesos = yaml.load(open("core/sucesos.yml", "r"), Loader=yaml.FullLoader)

    def __init__(self, players: List[Player]):
        if not isinstance(players, list):
            raise TypeError("players must be a list")
        self.players = players
        self.text = None
        self.day = 1

    def turn(self):
        self.text = []

        activos = self.players.copy()
        while len(activos) != 0:
            probability = [0.5, 0.3, 0.2]
            possible_num = [1, 2, 3]
            pers = min(len(activos), random.choice(possible_num, p=probability))
            players = random.choice(activos, pers, replace=False)
            activos_new = [x for x in activos if x not in players]
            activos = activos_new
            self.text.append(self.event(players))

        self.text.sort()
        if len(self.players) <= 1:
            return False
        return True

    def event(self, players):
        total_players = len(players)
        events = self.sucesos[str(total_players) + "pers"]
        secret_num = random.randint(0, 101)
        if total_players == 1:
            if secret_num < 60:
                phrase = str(random.choice(events["muerte"]))
                for player in players:
                    self.players.remove(player)
            else:
                phrase = str(random.choice(events["miscelania"]))

            return format_str(phrase, players)

        elif total_players == 2:
            if secret_num < 20:
                phrase = str(random.choice(events["muerte"]))
                for player in players:
                    self.players.remove(player)
            elif secret_num < 60:
                phrase = str(random.choice(events["asesinato"]))
                self.players.remove(players[1])
            else:
                phrase = str(random.choice(events["miscelania"]))
            return format_str(phrase, players)

        else:
            if secret_num < 20:
                phrase = str(random.choice(events["muerte"]))
                for player in players:
                    self.players.remove(player)
            elif secret_num < 60:
                assasin = events["asesinato"]
                if secret_num < 40:
                    phrase = str(random.choice(assasin["individual"]))
                    self.players.remove(players[1])
                    self.players.remove(players[2])
                else:
                    phrase = str(random.choice(assasin["doble"]))
                    self.players.remove(players[2])
            else:
                phrase = str(random.choice(events["miscelania"]))
            return format_str(phrase, players)

    def get_log(self):
        if self.text is None:
            raise ValueError("Turn 1 isn't initiated")
        self.text.insert(0, "Día {}".format(self.day))
        self.day += 1
        return self.text

    def get_end(self):
        if len(self.players) == 1:
            return str(self.players[0]) + " ha ganado."
        if len(self.players) == 0:
            return "Nadie ha ganado, todos han muerto."
