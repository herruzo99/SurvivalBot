import yaml
from core.player import Player
from numpy import random


class GameEngine:
    sucesos = yaml.load(open("sucesos.yml", "r"), Loader=yaml.FullLoader)

    def __init__(self, players):
        if not isinstance(players, list):
            raise TypeError("players must be a list")
        self.players = players

    def game(self):
        final = []
        x = 1
        while len(self.players) > 1:
            final.append("Dia " + str(x))
            final.extend(self.turn())
            x += 1
        return final

    def turn(self):
        activos = self.players.copy()
        results = []
        while len(activos) != 0:
            pers = min(len(activos), random.randint(1, 4))
            players = random.choice(activos, pers, replace=False)
            activos_new = [x for x in activos if x not in players]
            activos = activos_new
            results.append(self.event(players))

        if len(self.players) == 1:
            results.append(str(self.players[0]) + " ha ganado.")
        elif len(self.players) == 0:
            results.append("nadie ha ganado, todos han muerto.")
        return results

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

            return phrase.format(players[0])

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
            return phrase.format(players[0], players[1])

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
            return phrase.format(players[0], players[1], players[2])
