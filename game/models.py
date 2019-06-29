import uuid

from django.contrib.auth.models import User
from django.db import models
from game.choices import GAME_SETTINGS


class Player(models.Model):
    """Player model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class Score(models.Model):
    """Score model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    player = models.ForeignKey(Player, on_delete="CASCADE")
    phase = models.IntegerField()
    score = models.IntegerField()

    @property
    def phase_score(self):
        return "Phase {} - Score {}".format(self.phase, self.score)

    def __str__(self):
        return "{} {} {}".format(self.player.name, self.phase, self.score)


class Game(models.Model):
    """Game model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    game_type = models.CharField(max_length=150, choices=GAME_SETTINGS)
    players = models.ManyToManyField(Player)
