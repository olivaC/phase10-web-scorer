from django.contrib import admin

# Register your models here.
from game.models import Score, Game

admin.site.register(Score)
admin.site.register(Game)

