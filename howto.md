# How To Contribute {-#howto}

1. If you already have a fork from previous contributions, you may want to synchronize it with the `labsyspharm` repository.
    * If your fork currently doesn't have any new changes from the live version, the easiest thing to do is delete the fork and re-fork. Go to your personal fork, click on the Settings tab, scroll all the way to the bottom and press "Delete Repository". Proceed to Step 2 to refork.
    * If your fork *does* deviate from the live version, you might want to rebase it: Follow the [Git rebase guide](https://git-scm.com/book/en/v2/Git-Branching-Rebasing), or get in touch with Artem or Jeremy for help.
2. Go to https://github.com/labsyspharm/mcmicro and press "Fork" in the top right corner.
3. In the Fork dialogue, select your personal GitHub account to fork the project to.
4. Edit the .md files to add content. For formatting reference, see https://bookdown.org/yihui/bookdown/markdown-syntax.html
5. If creating new .md files, add their filenames to `_bookdown.yml`.
6. When finished, navigate to your personal fork (usually https://github.com/YourUsername/mcmicro) and press "New pull request".
7. Review the changes and press "Create pull request" when ready.
8. Other teammates will review and comment on your changes. Once approved, the changes will appear on the live website.

## Commands to type for rebasing

This set of commands creates a local copy of your repo and sets up the upstream
```
git clone https://github.com/YourUsername/mcmicro.git
cd mcmicro
git remote add upstream https://github.com/labsyspharm/mcmicro.git
git remote -v
```

To rebase your own fork to match the upstream
```
git checkout master
git fetch --all
git rebase --ff-only upstream/master
git push origin master
```
