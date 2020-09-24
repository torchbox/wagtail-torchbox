from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from .views import EventsRegisterView

urlpatterns = [
    path('api/events/<str:meeting_type>/<int:meeting_id>/register/', csrf_exempt(EventsRegisterView)),
]
