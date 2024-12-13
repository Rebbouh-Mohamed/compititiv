from django.urls import path
from .views import GetDefaultCode

urlpatterns = [
    path('<int:problem_id>/<str:language>/', GetDefaultCode.as_view(), name='get_default_code'),
]