from django.urls import path
from .views import LeaderBoard

urlpatterns=[
    path("<int:contest_id>/",LeaderBoard.as_view(),name="leader_board"),
]