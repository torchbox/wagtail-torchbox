import json
import requests
from django.http import JsonResponse
from django.conf import settings

# Authentication token used to access all TBX meetings
ZOOM_TOKEN = getattr(settings, 'ZOOM_JWT_TOKEN')

class Event:
  def __init__(self, id=None, name=None, start_time=None, join_url=None, start_url=None, event_type=None):
    self.id = id
    self.name = name
    self.start_time = start_time
    self.join_url = join_url
    self.event_type = event_type

class ZoomMeetingEvent(Event):
  def __init__(self, id=None, name=None, start_time=None, join_url=None, start_url=None, event_type=None):
    self.id = id
    self.name = name
    self.start_time = start_time
    self.join_url = join_url
    self.event_type = event_type

  @staticmethod
  def from_response(data, event_type=None):
    """Create a zoom meeting from an API response"""
    # Check reponse is valid
    if data.status_code == 200:
      # Get JSON data
      data = data.json()
      # Create new Zoom Meetong
      return ZoomMeetingEvent(
        id=data.get('id'),
        name=data.get('topic'),
        start_time=data.get('start_time'),
        join_url=data.get('join_url'),
        event_type=event_type
      )

  @staticmethod
  def query_with_meeting_id(meeting_id):
    # Query Zoom API
    meeting = requests.get(f"https://api.zoom.us/v2/meetings/{meeting_id}", headers={
      "authorization": f"Bearer {ZOOM_TOKEN}"
    })
    # Convert to object
    return ZoomMeetingEvent.from_response(meeting, event_type='meeting')

  @staticmethod
  def query_with_webinar_id(meeting_id):
    # Query Zoom API
    meeting = requests.get(f"https://api.zoom.us/v2/webinars/{meeting_id}", headers={
      "authorization": f"Bearer {ZOOM_TOKEN}"
    })
    # Convert to object
    return ZoomMeetingEvent.from_response(meeting, event_type='webinar')

  def get_api_url(self):
    """Get the correct API url for this type of meeting."""
    if (self.event_type == 'meeting'):
      return f"https://api.zoom.us/v2/meetings/{self.id}"
    if (self.event_type == 'webinar'):
      return f"https://api.zoom.us/v2/webinars/{self.id}"

  def add_registrant(self, registrant):
    """Add a registrant to the meeting/webinar using Zoom API."""
    # Convert registrant to JSON data
    registrant_data = json.dumps(registrant.validated_data)

    # Send registrant data to Zoom
    api_url = self.get_api_url()
    registration = requests.post(f"{api_url}/registrants",
      headers={
        "authorization": f"Bearer {ZOOM_TOKEN}",
        "Content-Type": "application/json"
      },
      data = registrant_data
    )

    # Check result
    if registration.status_code == 200 or registration.status_code == 201:
      return JsonResponse({
        "status": "Succcess"
      })
    if registration.status_code == 415:
      return JsonResponse({
        "error": "Invalid registrant format"
      }, status=415)
    else:
      return JsonResponse({
        "error": "Unknown Error"
      }, status=registration.status_code)
