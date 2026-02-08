from django.conf import settings
from django.db import models
User = settings.AUTH_USER_MODEL


# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    createdby = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_polls"
    )

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Option(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="options"
    )
    text = models.CharField(max_length=255)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["poll", "text"],
                name="unique_option_per_poll"
            )
        ] # unique options per poll 
    def __str__(self):
        return f"{self.text} ({self.poll.title})"
