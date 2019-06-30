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
        return "/game/{}".format(self.name)

    def __str__(self):
        return "Game: {}".format(self.name)


class Score(models.Model):
    """Score model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    player = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    phase = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete="CASCADE")

    @property
    def phase_score(self):
        return "Phase {} - Score {}".format(self.phase, self.score)

    def __str__(self):
        return "{} {} {}".format(self.player.username, self.phase, self.score)
