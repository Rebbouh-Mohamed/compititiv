from django.db import models
from contests.models import Contest
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Problem(models.Model):
    class LevelChoices(models.TextChoices):
        EASY = "easy", _("Easy")
        MID = "mid", _("Mid")
        HARD = "hard", _("Hard")
    title = models.CharField(max_length=200, unique=True)  # Unique title for easy identification
    description = models.TextField()
    input_description = models.TextField(default="")
    output_description = models.TextField(default="")
    contest = models.ForeignKey(
        Contest, on_delete=models.CASCADE, related_name="problems"
    )  # Problem belongs to a contest
    points = models.IntegerField(validators=[MinValueValidator(1)])  # Corrected field name for clarity
    level = models.CharField(
        max_length=10,
        choices=LevelChoices.choices,
        default=LevelChoices.EASY,  # Default to "easy"
    )

    class Meta:
        indexes = [
            models.Index(fields=["contest", "title"]),  # Improves query performance for contest-specific problems
        ]
    def save(self, *args, **kwargs):
        # Set points based on level before saving
        if self.level == self.LevelChoices.EASY:
            self.points = 5
        elif self.level == self.LevelChoices.MID:
            self.points = 10
        elif self.level == self.LevelChoices.HARD:
            self.points = 15
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="testcases")  # Link to Problem
    input_data = models.TextField()  # Input for the test case
    expected_output = models.TextField()  # Expected output for the test case
    class Meta:
        unique_together = ('problem', 'input_data')  # Ensures unique input per problem

    def __str__(self):
        return f"Test case for {self.problem.title}"
    
    
class SubmitCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submitcases")
    input_data = models.TextField()
    expected_output = models.TextField()

    class Meta:
        unique_together = ('problem', 'input_data')

    def __str__(self):
        return f"Submit case for {self.problem.title}"