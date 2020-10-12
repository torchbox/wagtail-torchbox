# import requests
# from django.db import models


# ZOOM_ALL_USERS = "https://api.zoom.us/v2/users/"

# def get_all_meetings():
#   requests.get(f"https://api.zoom.us/v2/users/meetings/"")

# class ZoomMeetingsField(models.CharField):
#   def __init__(self, *args, meetings=None, **kwargs):
#         ICON_CHOICES = [
#           ("76361471699", "Nathan Horrigan's Zoom Meeting 0"),
#           ("76361471679", "Nathan Horrigan's Zoom Meeting 1"),
#           ("76361471629", "Nathan Horrigan's Zoom Meeting 2"),
#         ]

#         # Hacks, Because init called multiple times (IDK why!?)
#         kwargs["max_length"] = 255
#         kwargs["choices"] = ICON_CHOICES

#         # Initialize core CharField
#         super().__init__(*args, **kwargs)
#     # def __init__(self, *args, pack=None, **kwargs):
#     #     # Build icon cache
#     #     IconPackBuilder.build()

#     #     # Get icons from pack
#     #     ICON_CHOICES = []
#     #     if pack is not None:
#     #         # Select icons from icon pack
#     #         icons = IconPackBuilder.get_pack(pack)

#     #         # Create choice list from icons
#     #         ICON_CHOICES = [
#     #             (f"{pack}-{icon.name}", icon.name) for icon in icons.values()
#     #         ]

#     #     # Hacks, Because init called multiple times (IDK why!?)
#     #     kwargs["max_length"] = 255
#     #     kwargs["choices"] = ICON_CHOICES

#     #     # Initialize core CharField
#     #     super().__init__(*args, **kwargs)
