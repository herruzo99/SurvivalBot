class Player:
    def __init__(self, name, strength=None, vitality=None, resistance=None, agility=None, luck=None, intelligence=None,
                 willpower=None):
        if strength is not None:
            self.strength = strength
        else:
            self.strength = 50
        if vitality is not None:
            self.vitality = vitality
        else:
            self.vitality = 50
        if resistance is not None:
            self.resistance = resistance
        else:
            self.resistance = 50
        if agility is not None:
            self.agility = agility
        else:
            self.agility = 50
        if luck is not None:
            self.luck = luck
        else:
            self.luck = 50
        if intelligence is not None:
            self.intelligence = intelligence
        else:
            self.intelligence = 50

        self.name = name
        self.won_games = 0

    def __str__(self):
        return self.name
