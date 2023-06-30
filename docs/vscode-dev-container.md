# VSCode Dev container

[VSCode](https://code.visualstudio.com/) is a great editor, but due to the way projects are setup, getting richer editor integration requires some hoop-jumping. Because projects are run under Docker, VSCode doesn't simply have access to the Python virtual environment, and so many features stop working.

!!! warning

    The following steps require the official VSCode distribution, rather than offshoots like [VSCodium](https://vscodium.com/).

## Virutal environment integration

The VSCode integration with Docker requires the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension. This extension allows VSCode to install itself inside a container, and thus access its filesystem and virtual environments.

When opening a project with a dev container configuration, VSCode will prompt you whether you want to switch to it. To switch manually, open the command palette and select "Remote Containers - Reopen in Container". This will reload your VSCode window, build and then start the project containers. Once it's finished, you'll be presented with a regular-looking VSCode editor, but with the Python integration correctly installed and configured. Should you make any changes to the dev container configuration or `Dockerfile`, you'll want to use "Remote Containers - Rebuild and Reopen in Container" instead.

To install additional extensions into the container automatically, add its id to `remote.containers.defaultExtensions` in your vscode settings.

## Debugger

Now that VSCode has full access to your project and virtual environment, it's time for the main event: the debugger! VSCode's debugger allows you to set breakpoints and step through code, all on your running Django application.

These steps should be identical whether you're running a docker or vagrant project, however you will need the Python extension installed for this to work.

At the top of the "Run and Debug" tab should now be a green triangle. Click it to start debugging. This will start the Django development server in a new terminal tab showing the logs. For more about the debugger, [read the docs](https://code.visualstudio.com/Docs/editor/debugging).

## Limitations

Currently, the implementation isn't perfect. These are the known issues:

- Files in the root of the repository (eg `heroku.yml`) can't be edited. VSCode will show them, and allow you to edit them, but these changes are only made in the container, not on the host.
- Changes to the frontend require either rebuilding the container (see above) or using the `frontend` container as the entrypoint for the application, and having it handle static files.
