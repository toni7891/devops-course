# Merge Conflicts

## What to Teach
- A conflict occurs when two branches modify the **same lines** in the **same file**
- Git cannot automatically decide which change to keep — you must resolve it manually
- Conflict markers: `<<<<<<<`, `=======`, `>>>>>>>` show both versions
- Conflicts are **normal** — they are not errors, just a request for human decision

## Demo Steps
1. Create a deliberate conflict: same file, same line, different changes on two branches
2. Attempt the merge — show the conflict message
3. Open the file — walk through the conflict markers line by line
4. Show resolution in VS Code (Accept Current / Accept Incoming / Accept Both)
5. Stage the resolved file with `git add`
6. Complete the merge with `git commit`
7. Show `git merge --abort` as an escape hatch

## Key Points
- Conflict markers:
  - `<<<<<<< HEAD` = your current branch's version
  - `=======` = separator
  - `>>>>>>> branch-name` = incoming branch's version
- You must remove ALL conflict markers when resolving
- After resolving, `git add` + `git commit` to complete
- `git merge --abort` cancels the merge and returns to the previous state

## Common Student Questions
- **Q: How do I avoid merge conflicts?**
  - A: You can't always avoid them, but: keep commits small, merge frequently, communicate with your team about who is working on what.

- **Q: Can I just accept one side entirely?**
  - A: Yes. `git checkout --theirs <file>` accepts the incoming branch. `git checkout --ours <file>` keeps the current branch. But always verify the result.

- **Q: What if I mess up the resolution?**
  - A: `git merge --abort` before committing. If already committed, `git reset --hard HEAD~1` to undo the merge commit.

## Tips
- This is a hands-on demo — let students practice creating and resolving conflicts
- Show VS Code's merge editor — it makes conflicts much more visual
- Reassure students: merge conflicts feel scary at first but become routine with practice
