from locals import *
from gook import Gook


class Team:
    def __init__(self, bitmap, team_name, team_color, positions, names):
        self.gooks = list()
        for i in range(TEAM_LEN):
            self.gooks.append(Gook(bitmap, positions[i], team_color, names[i], GOOK_RES, GOOK_IMG))
        self.team_name = team_name

    def __str__(self):
        return self.team_name

    def get_gook(self, n):
        return self.gooks[n % len(self.gooks)] if self.gooks else None

    def get_gooks(self):
        return self.gooks

    def remove_gook(self, gook):
        self.gooks.remove(gook)

    def check_state(self):
        if not self.get_gooks():
            return False
        else:
            return True

