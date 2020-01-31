class Team:
    def __init__(self, team_name, team_color, positions, names):
        self.gooks = list()
        for position, name in positions, names:
            self.gooks.append(Gook(position, team_color, name))
        self.team_name = team_name

    def get_gook(self, n):
        return self.gooks[n // len(self.gooks)] if self.gooks else None