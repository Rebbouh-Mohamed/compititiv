from django.urls import path
from .views import SubmitCodeView
urlpatterns = [
    path('<int:problem_id>/submit/', SubmitCodeView.as_view(), name='submit_code'),
]
