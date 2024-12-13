from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now 
from django.core.validators import MinValueValidator
# Create your models here.
class Contest(models.Model):
    title = models.CharField(max_length=200, unique=True)  # Unique constraint for contest titles
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.ManyToManyField(
        User, related_name="contests", through="ContestParticipation"
    )  # Explicit through model for flexibility

    class Meta:
        indexes = [
            models.Index(fields=["start_time", "end_time"]),  # Improves query performance on time filtering
        ]

    def is_active(self):
        return self.start_time <= now() <= self.end_time

    def __str__(self):
        return self.title
class ContestParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    pionts=models.FloatField(validators=[MinValueValidator(0)],default=0)
    class Meta:
        unique_together = ("user", "contest")  # Prevent a user from joining the same contest multiple times
        indexes = [
            models.Index(fields=["user", "contest"]),  # Improves query performance for checking participation
        ]

    def __str__(self):
        return f"{self.user.username} in {self.contest.title}"
