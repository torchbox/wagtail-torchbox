"""
Called by GitHub Action 'copy prod to staging' button is pressed.
This checks flightpath status
"""
import argparse
import os

import requests


def get_flightpath_args_from_env():
    """Get flightpath env var into an dict that can be used by post_to_flightpath()."""

    try:
        args = {
            "flightpath_auth_key": os.environ["FLIGHTPATH_AUTH_KEY"],
            "flightpath_url": os.environ["FLIGHTPATH_URL"],
        }

    except KeyError:
        raise KeyError(
            "You need the following environment variables to run flightpath: FLIGHTPATH_URL, FLIGHTPATH_AUTH_KEY. This should be set on GitHub secrets if running as GitHub Actions."
        )

    return args


def get_flightpath_job_status(flightpath_url, flightpath_auth_key, job_id):
    """
    Get job status from flightpath.
    You get the job_id from the response when posting to flightpath /copy.
    """
    response = requests.get(
        f"{flightpath_url}/status/{job_id}/",
        headers={
            "Authorization": f"Token {flightpath_auth_key}",
        },
    )
    response.raise_for_status()
    return response


if __name__ == "__main__":
    flightpath_args = get_flightpath_args_from_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--job_id", help="Flightpath job id")
    args = parser.parse_args()
    if not args.job_id:
        raise ValueError("Please specify flightpath job id with '--job_id'.")

    print("Get flightpath status...")
    response = get_flightpath_job_status(**flightpath_args, job_id=args.job_id)
    print(response.json()["log_output"])
