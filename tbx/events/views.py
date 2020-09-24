import json
from django.http import JsonResponse
from .serializers import RegistrantSerializer
from .events import ZoomMeetingEvent

def EventsRegisterView(request, meeting_type=None, meeting_id=None):
    # Validate the form data
    registrant = RegistrantSerializer(data=request.POST)
    if registrant.is_valid():
      # Pass validated form to Zoom API
      if meeting_type == "meeting":
        meeting = ZoomMeetingEvent.query_with_meeting_id(meeting_id)
      if meeting_type == "webinar":
        meeting = ZoomMeetingEvent.query_with_webinar_id(meeting_id)
      if meeting:
        return meeting.add_registrant(registrant)

    return JsonResponse({
      "error": "Invalid meeting type"
    }, status=415)
