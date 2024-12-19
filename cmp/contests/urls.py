from django.urls import path
from .views import JoinContestView,ContestParticipantsView,UpContestOrComingUpContestView,UserCreationView

urlpatterns = [
    path('<int:contest_id>/join/', JoinContestView.as_view(), name='join_contest'),
    path('participants/', ContestParticipantsView.as_view(), name='contest_participants'),
    path('upcontest/',UpContestOrComingUpContestView.as_view(),name='up_contest'),
    path('user/creat/',UserCreationView.as_view(),name='creat_user'),

]
