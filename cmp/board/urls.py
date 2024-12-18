from django.urls import path
from .views import LeaderBoard

urlpatterns=[
    path("",LeaderBoard.as_view(),name="leader_board"),
]