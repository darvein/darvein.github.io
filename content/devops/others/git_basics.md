# Git cheatsheet

# Content

## Some snippets

- Check all .git in all current directory folders and get latest commit's date:
```bash
for i in $(ls -t -d */); do
  commit_date=$(git -C $i log -1 --format=%cd)
  echo "${commit_date} - ${i}"
done
```

## Need to order all of these

```bash
## Target file: DELETE_ME.txt
## Test Repo:  [git@github.com](mailto:git@github.com) :darvein/gathery.git

### look for DELETE_ME.txt file on all branches
$ git log --all -- DELETE_ME.txt  
commit a763f4b567d0641321756626583cce7fe96d94f1
Author: Dennis Ruiz < [darvein@gmail.com](mailto:darvein@gmail.com) >
Date:   Fri Apr 28 14:06:34 2017 -0400

    added delete.txt file from rel1 branch

commit c8475178bf4a8806856aecf7712c1e7aae9f7f94
Author: Dennis Ruiz < [darvein@gmail.com](mailto:darvein@gmail.com) >
Date:   Fri Apr 28 14:05:52 2017 -0400

    added delete file from dev

commit 5b7319bec8d5d908777645e0dad98e5dfc763445
Author: Dennis Ruiz < [darvein@gmail.com](mailto:darvein@gmail.com) >
Date:   Fri Apr 28 14:04:03 2017 -0400

    added delete file on master



### remove DELETE_ME.txt from all branches
$ git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch DELETE_ME.txt' --prune-empty --tag-name-filter cat -- --all
Rewrite 5b7319bec8d5d908777645e0dad98e5dfc763445 (3/8) (1 seconds passed, remaining 1 predicted)    rm 'DELETE_ME.txt'
Rewrite c8475178bf4a8806856aecf7712c1e7aae9f7f94 (7/8) (1 seconds passed, remaining 0 predicted)    rm 'DELETE_ME.txt'
Rewrite a763f4b567d0641321756626583cce7fe96d94f1 (7/8) (1 seconds passed, remaining 0 predicted)    rm 'DELETE_ME.txt'

Ref 'refs/heads/dev' was rewritten
Ref 'refs/heads/master' was rewritten
Ref 'refs/heads/rel-1.0' was rewritten
Ref 'refs/heads/rel-2.0' was rewritten
Ref 'refs/remotes/origin/master' was rewritten
Ref 'refs/remotes/origin/dev' was rewritten
WARNING: Ref 'refs/remotes/origin/master' is unchanged
Ref 'refs/remotes/origin/rel-1.0' was rewritten
Ref 'refs/remotes/origin/rel-2.0' was rewritten


### push changes to git server
git push origin --force --all
git push origin --force --tags


### cleaning orphan objects references (locally)
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now


### Verify any evidence of DELETE_ME.txt file
$ git log --all -- DELETE_ME.txt   | wc -l
       0
$ find . -name DELETE_ME.txt | wc -l
       0
       
       
### verifying by clonning the repo again
$ git clone  [git@github.com](mailto:git@github.com) :darvein/gathery.git gat2
$ cd gat2
$ git log --all -- DELETE_ME.txt   | wc -l
       0







# Git basic flow
git add -A .
git commit -m "ISSUE-666"
git push origin master

# git remote add <remote name> <remote url repository>
git remote add origin  [git@github.com](mailto:git@github.com) :darvein/foobar.git

# Reverting changes
git reset --hard/--soft [commit|branch|ref]
git checkout simplefile.txt

git branch -d nombre-del-branch
git branch -m old_branch new_branch

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
git diff > [description]-[issue-number]-[comment-number].patch 
git apply -v [patchname.patch]; rm [patchname.patch]

# Logs and diff
git log --pretty="%h on %ad by %ae => %s" --date=short origin/master
git log -- [author='darvein@gmail.com](mailto:author='darvein@gmail.com) ' --pretty=format:"%h%x09%an%x09%ad%x09%s"
git log --pretty=format:"%h%x09%an%x09%ad%x09%s" --author="Dennis Ruiz" ‚Äîall
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

# Tips
git log -Stext_to_search --source --all
git config core.filemode false

git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch NOMBRE_DE_LA_CARPETA_O_ARCHIVO" HEAD
rm -rf .git/refs/original/ && git reflog expire --all &&  git gc --aggressive --prune
git push -f origin master


# Git basic flow
git add -A .
git commit -m "ISSUE-666"
git push origin master

# git remote add <remote name> <remote url repository>
git remote add origin  [git@github.com](mailto:git@github.com) :darvein/foobar.git

# Reverting changes
git reset --hard/--soft [commit|branch|ref]
git checkout simplefile.txt

git branch -d nombre-del-branch
git branch -m old_branch new_branch

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
git diff > [description]-[issue-number]-[comment-number].patch 
git apply -v [patchname.patch]; rm [patchname.patch]

# Logs and diff
git log --pretty="%h on %ad by %ae => %s" --date=short origin/master
git log -- [author='darvein@gmail.com](mailto:author='darvein@gmail.com) ' --pretty=format:"%h%x09%an%x09%ad%x09%s"
git log --pretty=format:"%h%x09%an%x09%ad%x09%s" --author="Dennis Ruiz" ‚Äîall
git-log --graph --online
git log --name-status
git log --name-only
git log --stat
git log <nombre_de_un_branch>..<otro_branch>
git show --pretty="format:" --name-only [aqui el id de un commit]
git log --online --decorate --graph

# Tips
git log -Stext_to_search --source --all
git config core.filemode false

git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch NOMBRE_DE_LA_CARPETA_O_ARCHIVO" HEAD
rm -rf .git/refs/original/ && git reflog expire --all &&  git gc --aggressive --prune
git push -f origin master


############# Installing GIT Server ##############
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

```bash
#Create a new branch:
git checkout -b feature_branch_name
#Edit, add and commit your files.
#Push your branch to the remote repository:
git push -u origin feature_branch_name



git checkout -b aws_docker
git push -u origin aws_docker
```


### Tips

```bash
# Listing remote branches without cloning the repo
git ls-remote -q -h $REPOSITORY | awk '{print $2}' | sed 's/refs\/heads/origin/'
```
