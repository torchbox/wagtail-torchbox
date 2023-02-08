"""
Called by GitHub Action 'copy prod to staging' button is pressed.
This calls flightpath to copy prod database and media to staging.
"""
import os

import requests


def get_flightpath_args_from_env():
    """Get flightpath env var into an dict that can be used by post_to_flightpath()."""

    try:
        args = {
            "source": os.environ["HEROKU_APP_NAME_PRODUCTION"],
            "destination": os.environ["HEROKU_APP_NAME_STAGING"],
            "flightpath_auth_key": os.environ["FLIGHTPATH_AUTH_KEY"],
            "deployment_key": os.environ["DEPLOYMENT_KEY"],
            "flightpath_url": os.environ["FLIGHTPATH_URL"],
        }

    except KeyError:
        raise KeyError(
            "You need the following environment variables to run flightpath: FLIGHTPATH_URL, HEROKU_APP_NAME_PRODUCTION, HEROKU_APP_NAME_STAGING, FLIGHTPATH_AUTH_KEY, DEPLOYMENT_KEY. This should be set on GitHub secrets if running as GitHub Actions."
        )

    return args


def post_to_flightpath(
    flightpath_url, flightpath_auth_key, source, destination, deployment_key
):
    """
    Util method that wraps around a request call to flightpath.
    This may be used by run_flightpath.py command line call or imported to be used by code.
    """

    response = requests.post(
        f"{flightpath_url}/copy/{source}/{destination}/",
        data={
            "source_key": deployment_key,
            "destination_key": deployment_key,
            "copy_media": True,
            "from_backup": True,
            "create_snapshot": True,
        },
        headers={
            "Authorization": f"Token {flightpath_auth_key}",
        },
    )

    response.raise_for_status()

    return response


# If this run_flightpath.py is run as a script on the command line or GitHub Actions
if __name__ == "__main__":
    flightpath_args = get_flightpath_args_from_env()

    # The following GitHub vars may not exist if this is
    # not called from GitHub Actions, e.g. from command or shell
    # https://docs.github.com/en/free-pro-team@latest/actions/reference/environment-variables#default-environment-variables
    repository = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")

    print(
        f"Running flightpath... copying from '{flightpath_args['source']}' to '{flightpath_args['destination']}'"
    )
    if run_id:
        print(f"from GitHub repository: {repository}, run_id: {run_id}.")

    response = post_to_flightpath(**flightpath_args)

    print(
        f"Request sent to {response.url}. Check status by going to flightpath /status/job_id."
    )
    print(response.text)

    # Get status and set it as env var for use with /status to check progress
    job_id = response.json()["job_id"]
    print(f"Job id: {job_id}")
