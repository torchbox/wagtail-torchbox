# Torchbox.com project conventions

## Git branching model

We follow a loose version of the [Git flow branching model](https://nvie.com/posts/a-successful-git-branching-model/).

- Make pull requests against: `master`
- The client QA branch is: `staging`

1. Make changes on a new branch, including a broad category and the ticket number if relevant e.g. `feature/123-extra-squiggles`, `fix/newsletter-signup`.
2. Push your branch to the remote.
3. Make pull requests at https://github.com/torchbox/wagtail-torchbox/pulls
4. Edit details as necessary.

If you need to preview work on `staging`, this can be merged and deployed manually without making a pull request. You can still make the pull request as above, but add a note to say that this is on `staging`, and not yet ready to be merged to `master`.

### Handling conflict on staging

If your commit includes migration files, and there is a migration conflict with `master` branch, the simplest solution would be to delete the migration files on your branch and re-generate them after rebasing your branch. However only delete migration files IF THEY ONLY EXISTS ON YOUR BRANCH, i.e. they have not been merged to staging, master or release branches yet.

Otherwise, if this is not an option, you can run `dj makemigrations –merge` to generate a merge migration file to resolve the conflict. Commit this file to the target branch with the conflict, e.g. `staging`, you don't have to add it to your feature branch.

Do not attempt to edit or rename an existing migration file on `staging` or `master`, as this will likely lead to further problems and conflicts.

## Deployment Cycle

Make sure `master` contains all the desired changes (and is pushed to the remote repository and has passed CI). Deploy to production (see [deployment documentation](deployment.md)).
