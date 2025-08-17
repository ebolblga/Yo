# Development Guide
Simply [fork the repo](#forking-the-repo) and make a [pull requst](#making-a-pull-request-pr) when you're done.

## Forking the repository
Fork this Github repo and clone your fork locally. Then make changes to a local branch to the fork.

See [Creating a pull request from a fork](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)

## Making a pull request (PR)
### PR checklist
A quick list of things to keep in mind as you're making changes:
- As you make changes
  - Make your changes in a forked repo (instead of making a branch on the main repo)
  - [Sign your commits](#signing-off-commits) as you go
  - Rebase from master instead of using `git pull` on your PR branch
- When you make the PR
  - Make a pull request from the forked repo you made
  - Ensure the title of the PR matches semantic release conventions (e.g. start with `feat:` or `fix:` or `ci:` or `chore:` or `docs:`).
  - Ensure you leave a release note for any user facing changes in the PR.
  - Try to keep PRs smaller. This makes them easier to review.

### Good practices to keep in mind
- Fill in the description based on the default template configured when you first open the PR
  - What this PR does/why it's need it
  - Which issue(s) this PR fixes
  - Does this PR introduce a user-facing change
- Add `WIP:` to PR name if more work needs to be done prior to review

### Signing off commits
> :warning: Warning: using the default integrations with IDEs like VSCode or IntelliJ will not sign commits.

Use [git signoffs](https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification) to sign your commits.

Then, you can sign off commits with the `-s` flag:
```
git commit -s -m "My first commit"
```

### Incorporating upstream changes from master
Use `git rebase [master]` instead of `git merge` : `git pull -r`.

Note that this means if you are midway through working through a PR and rebase, you'll have to force push:
`git push --force-with-lease origin [branch name]`
