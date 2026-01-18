from django.db import models
from django.conf import settings
from polls.models import Poll, Option

User = settings.AUTH_USER_MODEL

#create your models here

class Vote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "poll"],
                name="unique_user_vote_per_poll"
            )
        ] # only one user vote per poll ensuring integrity and no mixups

    def __str__(self):
        return f"{self.user} → {self.poll}"
