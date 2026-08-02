Quick commit and push. Do the following steps:

1. Run `git status` and `git diff --stat` to see what changed.
2. Stage all changed files with `git add -A`.
3. Generate a concise, descriptive commit message based on the actual changes (1-2 sentences, focus on the "why").
4. Commit using that message (include `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`).
5. Push to the current branch's remote (use `git push -u origin HEAD` if no upstream is set, otherwise `git push`).
6. Show the result: branch name, commit hash, and remote URL.

If $ARGUMENTS is provided, use it as the commit message instead of generating one.

Do NOT ask for confirmation — just do it quickly.
