from django.db import models
from problems.models import Problem
# Create your models here.
class DefaultCode(models.Model):
    LANGUAGE_CHOICES = [
        ('C', 'C'),
        ('CPP', 'C++'),
        ('CS', 'C#'),
        ('JAVA', 'Java'),
        ('JS', 'JavaScript'),
        ('PY', 'Python'),
        ('GO', 'Go'),
    ]

    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)  # Language choice
    code_snippet = models.TextField()  # Default code snippet
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="default_codes")  # Foreign key to Problem

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language', 'problem'], name='unique_language_problem')
        ]

    def __str__(self):
        return f"{self.language} Code for {self.problem.title}"