# how to collaborate, GitHub project with team.
- only 1 will be the "Owner" all other fork his project and PR (Pull Request) to it - that way we dont need to pay GitHub.
- the repository must be "public" for not to pay.


## Terms:
* Remote		  == copy of the project in repository (=repo) like GitHub, GitLab, BitBucket. here use GitHub.
* Track 		  == local branch that knows which remote branch it corresponds. so can "git pull" "git push" "git status".
* "Collaborator"  & "Organization Member" == GitHub concept, users who have full access to remote, other than * "Owner". at old can only have 3 in free edition. today, GitHub change it a bit, we dont use that practice as GitHub use it to charge money.
* Fork	 	  == copy of the project from owner remote repo on GitHub to our GitHub repo.
* Clone   	  == our local copy on our own computer of the project.
					at GitHub we can only clone our own repository. if try to directly clone others - GitHub will automatically fork it and only then clone.
* Contributor's == anyone who fork the project, improve it and then update (push) to owners original project.
* PR(Pull request) == when "Contributor's" try to update (=push) to owner repo, the owner must approve that update first. that request for approval call PR.


## standard naming conventions:
short version:
### origin 	  == our own GitHub repo.
### upstream 	  == the owner GitHub repo.
long version:
* origin   	  == our own remote copy of the project on our GitHub. for contributor's its the fork.
* upstream 	  == the owner repository that we dont have access to (the original project that we fork from).
* note: if we only use single remote - the origin is our only "upstream".
but since we have 2 upstream: our own GitHub repo that was forked from owner GitHub repo - by convention naming is: "upstream" is the owner remote, and "origin" is our remote.

---
---
* one-time setup:
1. Fork repositrory with GitHub website GUI (copy from owner to our repo)
2. Clone our repo to local machine
```bash
git clone https://github.com/YOUR_USER/REPO_FORKED_NAME.git
cd REPO_FORKED_NAME
git remote -v
	# should show our remote only.
git remote add upstream https://github.com/OWNER/REPO.git
git remote -v
	# verify - now, should show both remotes (our remote(=origin) and owner(=upstream))
```

2. Must do each time before work - sync local with both remotes ("upstream" and "origin").
```bash
git fetch upstream
	# get owner's latest

git switch main
	# alternative command (exactly the same - older syntax):
	git checkout main

git rebase upstream/main # rebase without commit (cleaner history)
	# bring your local main up to date with owner. we have 2 options - with or without commit:
		# alternative command - will do the same (will create merge commit):
		git merge upstream/main
		# alternative same command (git pull = git fetch + git merge):
		git pull upstream main


git push origin main
	# update your fork on GitHub (will be ff merge - as local more update than origin)
	# we might need:
	git push origin main --force-with-lease
	# after rebase may need to push with "force" - as we mess with history
	# "--force-with-lease" is safer than "--force" — it refuses to push if someone else updated the branch remotely.
```

3. Push our local feature branch to origin (=our fork reository):
```bash
git switch -c feature/my-feature
	# alternative command (exactly the same - older syntax):
	git checkout -b feature/my-feature

# ... make code changes ...
# ... make code changes ...
# ... make code changes ...
# ... make code changes ...
# ... when we finish:

git add .
git commit -m "feat: describe change"
git push origin feature/my-feature
		# alternative command (if we didnt set the origin yet...):
		git push --set-upstream origin feature/my-feature
		# alternative command (exactly the same - shorter)
		git push -u origin feature/my-feature
```

4. PR = ask to merge our `origin` (=our fork) repo to `upstream` (=owner) repo
## PR (pool request) on GitHub:
Go to your fork → you'll see "Compare & pull request"
Target: OWNER/REPO ← YOUR_USER/REPO (branch my-feature)
Submit PR

---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---

5. hopefully you do not need that part:
* solve upstream conflicts (when owner updates remote, and has conflicts with our local):
* we have 3 options: "fetch & merge"/"pull" (called "back-merge") and "rebase" - they are the same with minor difference. usually experts use rebase as it more clean. but back-merge is safer and create more commits.

strategy to solve conflict:
1. abort merge to main
2. create new branch for merge
3. manually solve conflicts
4. only when we solve all conflicts, switch back to main and merge upstream updates to local main.
```bash # 1st way "rebase":
# 1st way rebase:
git fetch upstream
git rebase upstream/main

#### here we got "merge conflict error"!!! ####

git rebase --abort
git checkout -b branch_for_merge
git rebase upstream/main
#### manually fix conflicts......   ####

git add <file name>
git rebase --continue

git checkout main
git merge branch_for_merge
```
```bash # 2nd way "fetch & merge"
# 2nd way back-merge:
git fetch upstream
git merge upstream/main

#### here we got "merge conflict error"!!! ####

git merge --abort
git checkout -b branch_for_merge
git fetch upstream
git merge upstream/main

git status # See which files have conflicts

#### manually fix conflicts......   ####

git add <file name>
git commit
git checkout main
git merge branch_for_merge
```
```bash # 3rd way "pull":
# 3rd way back-merge pull(shortcut for fetch & merge):
git pull upstream main

#### here we got "merge conflict error"!!! ####

git merge --abort
git checkout -b branch_for_merge
git pull upstream main

#### manually fix conflicts......   ####

git add <file name>
git commit
git checkout main
git merge branch_for_merge
```