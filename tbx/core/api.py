from xml.etree import ElementTree

import requests


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
