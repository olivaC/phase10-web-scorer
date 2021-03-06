# Generated by Django 2.1.5 on 2019-06-30 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='A unique game room name.', max_length=128, unique=True)),
                ('round', models.IntegerField(blank=True, default=1, null=True)),
                ('start', models.BooleanField(default=False)),
                ('finish', models.BooleanField(default=False)),
                ('host', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_user', to=settings.AUTH_USER_MODEL)),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phase', models.IntegerField(default=1)),
                ('score', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete='CASCADE', to='game.Game')),
                ('player', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
