from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)

    def __str__(self):
        return f'User<{self.username}>'


class Session(models.Model):
    session_key = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Session<{self.session_key}>'
