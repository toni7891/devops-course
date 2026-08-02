# Linux Scenario Lab - Managing a Shared Project Server

Welcome to your first real-world DevOps scenario lab!

## Installation Instructions

### Method 1: Download with curl (Recommended)

```bash
curl -L -o lab.tar.gz https://github.com/IITC-College/DevOps-Materials/releases/download/v1.1-scenario/linux_scenario_shared_server.tar.gz
tar -xzf lab.tar.gz
cd linux_scenario_shared_server
```

> **Note:** If you get "not in gzip format" or a tiny download, the release may not be published yet. Use Method 2 or ask the instructor for the tarball.

### Method 2: From the repository (if release not yet published)

```bash
git clone https://github.com/IITC-College/DevOps-Jan26.git
cd DevOps-Jan26/Linux/real-world-scenarios/linux_scenario_shared_server
```

## Instructor Setup (Required Before Lab)

**IMPORTANT**: Before students start the lab, instructors must run the environment setup script:

```bash
sudo ./setup_environment.sh
```

This script will:
- Create `/opt/project/` with a realistic project directory structure
- Populate source code files (Python stubs)
- Generate realistic log files (`app.log`, `access.log`, `deploy.log`)
- Create configuration files and operational scripts
- Set initial ownership to `root:root`

**Note**: The script does NOT create users or groups. Students create them as part of the exercises.

**Before Level 3**: After students complete Level 1 and Level 2, run the permissions bug script:

```bash
sudo ./set_level_permissions.sh
```

This introduces the Level 3 challenge bug:
- Creates a dummy group `it`
- Moves `dev2` into `it`, removes from `devteam`

Students must diagnose why `dev2` can no longer collaborate with the team and fix it.

### Cleanup After Lab

To remove all lab resources (users, groups, directories):

```bash
sudo ./cleanup_lab.sh
```

## Lab Objective

You are a DevOps engineer joining a new team. A fresh Linux server has been set up for the development team, and it's your job to prepare it for work.

In this lab you will:

- **Create users and groups** for the development team
- **Set ownership and permissions** on a shared project directory
- **Analyze production logs** using pipes and filters
- **Save reports** using output redirection
- **Search for files** across the project
- **Configure admin access** for the DevOps engineer
- **Debug a permissions issue** reported by a team member

## Important: Hints Only!

This lab does NOT give you the exact commands. Instead, you will receive **hints** that guide you toward the right solution. You must:

- Think about which command to use
- Look up command options if needed
- Use knowledge from previous labs

This is how real DevOps work looks — you often need to figure things out yourself!

## The Team

| User | Role            |
|------|-----------------|
| dev1 | Developer       |
| dev2 | Developer       |
| ops1 | DevOps Engineer |

## How to Start?

1. Open the `start_here.txt` file - this is where to begin!
2. Read the story and instructions carefully
3. Follow the exercises step by step through the clue files

```bash
cat start_here.txt
```

## Exercise Overview

### Level 1: Building the Team — Users, Groups, Navigation
- **Exercise 1** (Parts 1-2): Create the team users and verify they exist
- **Exercise 2** (Parts 3-5): Create the development group and add team members
- **Exercise 3** (Part 6): Explore the pre-built project structure

### Level 2: Securing the Server — Permissions, Log Analysis
- **Exercise 1** (Parts 7-9): Set ownership and permissions, test access
- **Exercise 2** (Parts 10-12): Analyze application logs with pipes and grep
- **Exercise 3** (Parts 13-14): Save reports with redirection, search for files

### Level 3: Operations & Debugging — Admin Access, Troubleshooting
- **Exercise 1** (Parts 15-16): Configure admin privileges and test them
- **Exercise 2** (Challenge): Debug why a team member can't write to the project
- **Exercise 3**: Summary, reflection, and bonus exploration

## Topics Covered

| Topic              | Parts     |
|--------------------|-----------|
| Navigation         | 6, 9      |
| Files & Folders    | 6, 10     |
| Users & Groups     | 1-5       |
| Permissions        | 7-9, 16   |
| Pipes              | 11-12     |
| Redirection        | 10, 13    |

## Commands Reference

### Users & Groups
- Creating users (look up: `adduser`)
- Creating groups (look up: `groupadd`)
- Modifying users (look up: `usermod`)
- Checking user info (look up: `id`, `groups`)
- System files: `/etc/passwd`, `/etc/group`

### Permissions
- Changing ownership (look up: `chown`, `chgrp`)
- Changing permissions (look up: `chmod`)
- Viewing permissions (look up: `ls -l`)
- Switching users (look up: `su`)

### Pipes & Redirection
- Pipe output: `|`
- Redirect output: `>` (overwrite), `>>` (append)
- Filter text: `grep`
- Count lines: `wc -l`
- Search files: `find`

## Important Tips

1. **Read the hints carefully** — they contain all the information you need
2. **Check your work** — after each step, verify the result before moving on
3. **Use `man` pages** — if you're unsure about a command, try `man <command>`
4. **Permission denied is information** — it tells you what needs to be fixed
5. **Think before typing** — planning your command saves time

## Lab Submission

After completing all exercises:

1. Create a file called `my_answers.txt` in the lab directory
2. Write short answers to each exercise question
3. Include the commands you used
4. Save the file

## Help

If you get stuck:

1. Re-read the current hint — the answer is in there
2. Try `man <command>` for detailed help on any command
3. Check previous labs for similar exercises
4. Ask your instructor for guidance

## Good Luck!

This lab simulates a real DevOps task. Take your time, think through each step, and remember — figuring things out is part of the job!

---

**Linux Course**
**Scenario Lab: Managing a Shared Project Server**
**Version**: v1.1
