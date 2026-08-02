# Installing and Configuring Git

## What to Teach
- Verify Git is installed on all student machines
- The three configuration levels: **system** (all users), **global** (current user), **local** (current repo)
- Local overrides global, global overrides system
- Minimum required config: `user.name` and `user.email` — these appear in every commit
- Setting `init.defaultBranch` to `main` avoids confusion with legacy `master` default

## Demo Steps
1. Run `git --version` — verify everyone has Git installed
2. Set `user.name` and `user.email` with `--global`
3. Set `init.defaultBranch main`
4. Set VS Code as the default editor
5. Run `git config --list` to verify all settings
6. Open `~/.gitconfig` to show where the settings are stored (it is just a text file)

## Key Points
- `user.name` and `user.email` are **not** authentication — they are just metadata attached to commits
- The email should match the one used on GitHub (for commit attribution)
- `--global` applies to all repos for the current user; `--local` applies to one repo only
- Setting the default editor prevents confusion when Git opens vim unexpectedly

## Common Student Questions
- **Q: What happens if I don't configure my name/email?**
  - A: Git will warn you or use system defaults. Commits will still work but may show incorrect author info.

- **Q: Can I change these later?**
  - A: Yes, at any time. It only affects future commits — past commits keep their original author.

- **Q: What is the difference between `--global` and `--local`?**
  - A: `--global` sets it for all repositories on your machine. `--local` sets it for just one repo (useful if you use a different email for work vs personal projects).

## Tips
- On Windows, Git is typically installed via Git for Windows (includes Git Bash)
- On macOS, Git comes with Xcode Command Line Tools (`xcode-select --install`)
- On Linux, install via package manager (`apt install git` / `yum install git`)
- If a student gets "vim" when committing, show them how to exit (`:wq`) and then set VS Code as the editor
