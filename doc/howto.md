# How To Contribute {-#howto}

1. If you already have a fork from previous contributions, you may want to [synchronize it with the live version](#forksync).
2. Go to https://github.com/labsyspharm/mcmicro and press "Fork" in the top right corner.
3. In the Fork dialogue, select your personal GitHub account to fork the project to.
4. Edit the .md files to add content. For formatting reference, see https://bookdown.org/yihui/bookdown/markdown-syntax.html
5. If creating new .md files, add their filenames to `_bookdown.yml`.
6. When finished, navigate to your personal fork (usually https://github.com/YourUsername/mcmicro) and press "New pull request".
7. Review the changes and press "Create pull request" when ready.
8. Other teammates will review and comment on your changes. Once approved, the changes will appear on the live website.

## Synchronizing your fork with `labsyspharm` {-#forksync}

If you currently have no pending edits or open pull requests, the easiest thing to do is delete the fork and re-fork.
Go to your personal fork, click on the Settings tab, scroll all the way to the bottom and press "Delete Repository". **Note that this will delete any work-in-progress.** Proceed to step 2 above to re-fork `labsysparm`.

If the live version has been updated while you are partway through contributing new content, you have to rebase your personal fork to incorporate the update. This requires you to clone the repository to a local machine, apply the rebase, and then push changes to GitHub.

The following set of commands creates a local copy of your fork and sets up a pointer to the upstream repository (`labsyspharm` in this case). Replace `YourUsername` with your GitHub username.
``` {bash, eval=FALSE}
git clone https://github.com/YourUsername/mcmicro.git
cd mcmicro
git remote add upstream https://github.com/labsyspharm/mcmicro.git
git remote -v
```

The `git remote -v` command is there for verification. It should display `origin` pointing to your personal fork and `upstream` pointing to the `labsyspharm` fork.

To rebase your personal fork, thus incorporating changes from upstream, can be done with the following commands:
``` {bash, eval=FALSE}
git fetch --all
git rebase --ff-only upstream/master
git push origin master
```
