import uuid

from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    """Game model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    name = models.CharField(unique=True, max_length=128, help_text="A unique game room name.")
    round = models.IntegerField(default=1, null=True, blank=True)
    players = models.ManyToManyField(User)
    start = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="host")

    def get_url(self):
        return "/game/{}".format(self.id)

    def __str__(self):
        return "Game: {}".format(self.name)


class Score(models.Model):
    """Score model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    player = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    phase = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    @property
    def phase_score(self):
        return "Phase {} - Score {}".format(self.phase, self.score)

    @property
    def phase_help(self):
        if self.phase == 1:
            return "1. 🇦🇦🇦 + 🇧 🇧 🇧"
        elif self.phase == 2:
            return "2. 🇦🇦🇦 + 🇦 🇧 🇨 🇩"
        elif self.phase == 3:
            return "3. 🇦🇦🇦🇦 + 🇦 🇧 🇨 🇩"
        elif self.phase == 4:
            return "4. 🇦 🇧 🇨 🇩 🇪 🇫 🇬 (7)"
        elif self.phase == 5:
            return "5. 🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 (8)"
        elif self.phase == 6:
            return "6. 🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 (9)"
        elif self.phase == 7:
            return "7. 🇦🇦🇦🇦 + 🇧 🇧 🇧 🇧"
        elif self.phase == 8:
            return "8. 💟💟💟💟💟💟💟 (7)"
        elif self.phase == 9:
            return "9. 🇦🇦🇦🇦🇦 + 🇧 🇧"
        else:
            return "10. 🇦🇦🇦🇦🇦 + 🇧 🇧 🇧"

    def __str__(self):
        return "{} {} {}".format(self.player.username, self.phase, self.score)
