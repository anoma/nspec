---
icon: material/git
tags:
    - GitHub
    - Git
---


# Git Branching Strategy

This guide outlines how to work with Git branches to add new features or fix
issues on the specification document. We expect you are familiar with the basics
of Git and GitHub. Overall, the strategy for contributing to the Anoma
specification is to branch off from the latest version's branch of the nspec
repository, add new features or fix issues, open a pull request for review, and
merge the changes into the latest version's branch. 

## Creating a New Version

### Finding the Current Version

To determine the current version of the Anoma spec:

- Check the `VERSION` file located in the repository's root.
- Contact an administrator for guidance on the appropriate branch for your work.

### Version Branching Strategy

For new versions:

1. **Create a New Branch**: Branch off from the latest version's branch when
   starting a new version. This is usually done by one of the maintainers.
   
2. **Naming Conventions**: Use the following pattern to name the new version branch:

   ```
   vX
   ```

### Merging Finalised Versions

1. Completed versions are merged into the `main` branch after thorough review.
   We expect each version's branch to pass all the CI checks before merging.
   
2. To merge a finalised version:

   - Open a pull request against the `main` branch.
   - Tag the pull request with the `vX` label.
   - Get approval from the maintainers.
   - Pass all the CI checks.
   - Merge the pull request.

## Adding New Features to the Current Version

The following steps outline how to add new features or fix issues to the current
version of the Anoma spec. However, if for some reason you need to work on a
different, possibly older version, the steps are similar.

1. **Fetch the Latest Changes**: One alternative is to fetch all changes from
   the remote repository as follows:

   ```bash
   git fetch --all
   ```

2. **Create a New Branch**:

   - Branch off from the current version's branch:

    ```bash
    git checkout vX # Replace vX with the current version
    git checkout -b your-name/issue-identifier
    ```

### Rebasing Your Work

Rebasing is crucial for incorporating the most recent changes from the base
branch. Follow these steps to rebase, although sometimes you can rebase
directly on GitHub, pushing the "Update branch (rebase)" button at the end of
the pull request.


#### Start the Rebase

- Switch to your working branch:

    ```bash
    git checkout your-name/issue-identifier
    ```

- Initiate the rebase onto the target branch (e.g., `vX`):

    ```bash
    git pull origin vX --rebase
    ```

#### Resolve Conflicts

- Git will halt the rebase for you to resolve any conflicts.
- After resolving each conflict, proceed with:
    ```bash
    git rebase --continue
    ```
- If you need to stop the rebase process, use:
    ```bash
    git rebase --abort
    ```
- If you need to some help, reach out to the maintainers.

#### Push Your Changes

- Once the rebase is finished, push the changes to the remote repository.

```bash
git push origin your-name/issue-identifier
```

- A force push may be required if the rebase altered the branch history:

```bash
git push origin your-name/issue-identifier --force-with-lease
```

## Important Notes

- Verify you are on the correct branch before making modifications.
- Regularly update your branch with pulls and rebases to reduce conflicts and
  stay sync.
- Ask for help if you encounter any issues you cannot fix as soon as possible.