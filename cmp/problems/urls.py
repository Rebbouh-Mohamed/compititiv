from django.urls import path
from .views import ContestProblemsView,GetProblemView,TestProblem

urlpatterns = [
    path('<int:contest_id>/problems/', ContestProblemsView.as_view(), name='contest_problems'),
    path('<int:problem_id>/', GetProblemView.as_view(), name='get_problem'),
    path('<str:problem_title>/', GetProblemView.as_view(), name='get_problem'),
    path('<int:problem_id>/test/', TestProblem.as_view(), name='test_solutoin'),
]