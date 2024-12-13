from django.db import models
from django.contrib.auth.models import User
from problems.models import Problem
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    language=models.TextField(max_length=10)
    percentage=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(100)],default=0)
    class Meta:
        unique_together = ("user", "problem")  # Ensures one submission per problem per user
        ordering = ["-submitted_at"]  # Latest submissions appear first
        indexes = [
            models.Index(fields=["user", "problem"]),  # Improves query performance for user-problem pairs
            models.Index(fields=["problem", "submitted_at"]),  # Improves query performance for problem submissions
        ]

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"