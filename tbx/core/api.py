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

            job["title"] = node.find("vacancyname").text
            job["description"] = node.find("vacancydescription").text
            job["department"] = node.find("department").text
            job["location"] = node.find("city").text
            job["link"] = node.find("link").text

            jobs.append(job)

        return jobs

    def get_job_count(self, url=None):
        """
        Get the number of jobs listed on the current XML feed
        """
        if not url:
            return None

        resp = requests.get(url, timeout=3)

        try:
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
