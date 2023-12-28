# Git tips

## Git general use cases
```bash
# remove commit from git
git revert --strategy resolve <commit>

# set upstream
git branch --set-upstream dev origin/remoteBranchName

# Merging
git merge -X theirs branchName
git merge -X yours branchName

# Stashing
git stash
git stash list
git stash pop
git stash apply stash@{0}

# Tagging
git tag nameTag <SHA-1>
git tag nameTag branchName
git tag nameTag other tag
git tag nameTag HEAD^

# Patchs
git diff > thediff.patch
git apply -v thediff.patch

# Git diff clean
 git diff -U0 | grep '^[+-]' | grep -Ev '^(--- a/|\+\+\+ b/)' | sed -r "s/^([^-+ ]*)[-+ ]/\\1/"

# Logs and diff
git log --pretty="%h on %ad by %ae => %s" --date=short origin/master
git log --author=darvein@gmail.com --pretty=format:"%h%x09%an%x09%ad%x09%s"
git log --pretty=format:"%h%x09%an%x09%ad%x09%s" --author="Dennis Ruiz"
git-log --graph --online
git log --name-status
git log --name-only
git log --stat
git log <nombre_de_un_branch>..<otro_branch>
git show --pretty="format:" --name-only [aqui el id de un commit]
git log --online --decorate --graph

# Using git subtree
git remote add -f -t master --no-tags gitgit  [https://github.com/git/git.git](https://github.com/git/git.git) 
git subtree add --squash --prefix=third_party/git gitgit/master
git subtree pull --squash --prefix=third_party/git gitgit/master
git subtree push --squash --prefix=third_party/git gitgit/master

# Search a text in all the branches
git log -Stext_to_search --source --all
git config core.filemode false

# Remove a directoryfrom the whole repo
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch NOMBRE_DE_LA_CARPETA_O_ARCHIVO" HEAD
rm -rf .git/refs/original/ && git reflog expire --all &&  git gc --aggressive --prune
git push -f origin master
```

## Setting up a git repo

```bash
sudo adduser git
sudo passwd git

sudo mkdir /srv/git
sudo chown git:git -R /srv/git

su git
ssh-keygen -t rsa
touch ~/.ssh/authorized_keys
chmod 644 ~/.ssh/authorized_keys

cd /srv/git
mkdir properties
cd properties; git init --bare
```

## Got a problem?

- People were using git `merge` and `rebase` to get changes from the parent branch into their feature/hotfix branches. Somehow commits can be lost because of this.

```bash
git checkout my-broken-branch
git restore --source=origin/master --staged --worktree -- FileThatIdidntTouch.java DirectoryIDidntTouch .fileIdidntTouch
git add -A .
git commit -m "Sync with origin/master remote branch"; git push origin my-broken-branch
```

- How to split up a repository?
```
 git filter-branch --prune-empty --subdirectory-filter here/this-directory-on-a-new-repo -- --all
```

- Can't push my commit. It was in github before but it somehow got removed/overwritten, the history is broken idk :cry:
```bash
cp -rf $PWD ../copy-backup
diff -Naur . ../copy-backup > diff.patch
patch -p2 < diff.patch
git status # confirm changes and commit
```

#### Github cli

```bash
gh auth login
export GITHUB_TOKEN=ghp_b000000000h

# Clone all git repos
gh repo list gh-org-screening --limit 9999 --json sshUrl | jq '.[]|.sshUrl' | xargs -n1 git clone

# List pull requests
gh pr list --state closed --limit 45 --repo acmeorg-admarket/acmeorg
```
