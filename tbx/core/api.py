import logging
from xml.etree import ElementTree

import requests

logger = logging.getLogger(__name__)


class PeopleHRFeed(object):
    """
    Pulls from PeopleHR RSS feed.
    """

    def get_jobs(self, *args, url=None, **kwargs):
        if not url:
            return []

        resp = requests.get(url)
        resp.raise_for_status()

        jobs = []
        xml_root = ElementTree.fromstring(resp.content)

        for node in xml_root.iter("item"):
            job = {}

            # Provide a generic fallback content if the job creator forgets to include it
            try:
                job["title"] = node.find("vacancyname").text
            except AttributeError:
                job["title"] = "Role to be Announced"

            try:
                job["description"] = node.find("vacancydescription").text
            except AttributeError:
                job["description"] = "This role is currently being considered and will be announced shortly."

            try:
                job["link"] = node.find("link").text
            except AttributeError:
                job["link"] = "mailto://recruitment@torchbox.com"

            try:
                job["department"] = node.find("department").text
            except AttributeError:
                job["department"] = "TBC"

            # Not all postings include all location fields: ensure any provided are used
            location = []
            for location_key in ["city", "country"]:
                try:
                    location.append(node.find(location_key).text)
                except AttributeError:
                    pass
            job["location"] = ", ".join(location)

            jobs.append(job)

        return jobs

    def get_job_count(self, url=None):
        """
        Get the number of jobs listed on the current XML feed
        """
        if not url:
            return None

        try:
            resp = requests.get(url, timeout=3)

            resp.raise_for_status()
            xml_root = ElementTree.fromstring(resp.content)
            return len(xml_root.findall("channel/item"))
        except requests.exceptions.RequestException:
            logger.exception(f"Could not get People HR jobs feed from {url}")
            return None
        except requests.exceptions.Timeout:
            logger.exception(f"Timed out getting People HR jobs feed from {url}")
            return None
        except ElementTree.ParseError:
            logger.exception(f"Could not parse People HR jobs feed from {url}")
            return None
