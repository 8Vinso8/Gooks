class Team:
    def __init__(self, team_name, team_color, positions):
        self.gooks = list()
        for position in positions:
            self.gooks.append(Gook(position, team_color))
        self.team_name = team_name

    def get_gook(self, n):
        return self.gooks[n // len(self.gooks)] if self.gooks else None