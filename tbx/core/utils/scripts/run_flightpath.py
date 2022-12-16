"""
Called by GitHub Action 'copy prod to staging' button is pressed.
This calls flightpath to copy prod database and media to staging.
"""
import argparse
import os

import requests


def get_flightpath_args_from_env():
    """Get flightpath env var into an dict that can be used by post_to_flightpath()."""

    try:
        args = {
            "source": os.environ["HEROKU_APP_NAME_PRODUCTION"],
            "flightpath_auth_key": os.environ["FLIGHTPATH_AUTH_KEY"],
            "deployment_key": os.environ["DEPLOYMENT_KEY"],
            "flightpath_url": os.environ["FLIGHTPATH_URL"],
        }

    except KeyError:
        raise KeyError(
            "You need the following environment variables to run flightpath: FLIGHTPATH_URL, HEROKU_APP_NAME_PRODUCTION, FLIGHTPATH_AUTH_KEY, DEPLOYMENT_KEY. This should be set on GitHub secrets if running as GitHub Actions."
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
        f"{flightpath_url}/{source}/{destination}/",
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

    # To avoid accidentally running this script, a valid destination
    # has to be manually specified rather than fetched from env var.
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination", help="Destination Heroku app name")
    args = parser.parse_args()
    if not args.destination:
        raise ValueError("Please specify a destination with '--destination'.")
    elif args.destination == flightpath_args["source"]:
        # Don't accidentally run on prod!
        raise ValueError(
            "Destination cannot be the same as the source. Please specify a valid value for '--destination'."
        )

    # The following GitHub vars may not exist if this is
    # not called from GitHub Actions, e.g. from command or shell
    # https://docs.github.com/en/free-pro-team@latest/actions/reference/environment-variables#default-environment-variables
    repository = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")

    print("Running flightpath...")

    if run_id:
        print(f"from GitHub repository: {repository}, run_id: {run_id}.")

    response = post_to_flightpath(**flightpath_args, destination=args.destination)
    print(response.text)
