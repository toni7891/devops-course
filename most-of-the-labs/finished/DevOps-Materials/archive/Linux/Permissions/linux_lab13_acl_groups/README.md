# Linux Lab 13 - ACL & Group Permissions Lab

Welcome to the hands-on ACL & Group Permissions Lab! In this lab you will create users and groups, and learn how to use Access Control Lists (ACL) to grant selective group-based access to files without changing ownership or making files world-readable.

## Installation Instructions

### Method 1: Download with curl (Recommended)

```bash
curl -L -o lab.tar.gz https://github.com/IITC-College/DevOps-Materials/releases/download/v13.0-acl/linux_lab13_acl_groups.tar.gz
tar -xzf lab.tar.gz
cd linux_lab13_acl_groups
```

> **Note:** If you get "not in gzip format" or a tiny download, the release may not be published yet. Use Method 2 or ask the instructor for the tarball.

### Method 2: From the repository (if release not yet published)

```bash
git clone https://github.com/IITC-College/DevOps-Jan26.git
cd DevOps-Jan26/Linux/Permissions/linux_lab13_acl_groups
```

## Instructor Setup (Required Before Lab)

**CRITICAL**: Before students start the lab, instructors must run the environment setup script:

```bash
sudo ./setup_environment.sh
```

This single script will:
- Create lab users (**batman**, **superman**) with locked passwords
- Create the lab group (**superheroes**)
- Add both users to the superheroes group
- Create the test file (`/tmp/heroes.txt`) with proper initial state
- Set file ownership and basic permissions to demonstrate ACL need

**Note**: Students may need to log out and back in (or run `newgrp superheroes`) for group membership to take effect.

## Lab Objective

In this lab you will actively **explore and master** Access Control Lists (ACL):

- **ACL Basics**: Understand how ACL extends beyond basic Unix permissions
- **getfacl**: Read and interpret ACL entries on files
- **setfacl**: Add and remove ACL entries to grant group-based access
- **Real-World Scenarios**: Learn when and why to use ACL instead of chmod/chown
- **Group Management**: Work with users who belong to shared groups
- **The ACL Mask**: Understand how the permission mask constrains ACL entries

## Important: What This Lab IS and ISN'T

- ❌ **NOT** just about groups (you learned that in Lab 12)
- ❌ **NOT** about using `chmod 777` to fix access issues
- ✅ **IS** about understanding ACL as a more flexible alternative to basic permissions
- ✅ **IS** about granting selective group-based access without changing file ownership
- ✅ **IS** about the principle of least privilege using modern Unix features

## How to Start?

1. Open the `start_here.txt` file - everything is there!
2. Read the instructions carefully
3. Follow the 10 steps in order

```bash
cat start_here.txt
```

## The 10 Steps

| Step | Topic | What You'll Learn |
|------|-------|------------------|
| 1 | Inspection | Understand the starting state and ACL notation |
| 2 | Group Verification | Confirm users belong to the superheroes group |
| 3 | Test Before ACL | Verify why batman/superman can't access the file |
| 4 | Add ACL Entry | Grant group-based access using setfacl -m |
| 5 | Test as batman | Verify batman can read/write with ACL |
| 6 | Test as superman | Verify all group members get ACL benefits |
| 7 | Inspect ACL | Deep dive into getfacl output and the mask |
| 8 | User ACL (optional) | Grant ACL to individual users, not just groups |
| 9 | Remove ACL | Reset file to basic permissions using setfacl -b |
| 10 | Verify Removal | Confirm access is denied after ACL removal |

## Key Concepts

### Basic Permissions vs ACL

**Basic Unix Permissions (chmod)**
```
drwxr-xr-x
user:group:others
```
- Only 3 categories of access (you, your group, everyone else)
- Limited flexibility when you need selective team access

**Access Control Lists (ACL)**
```
# file: document.txt
user::rw-
group::r--
group:developers:rw-    <-- Can grant rw to specific GROUP
group:managers:r--      <-- Can grant r to another GROUP
mask::rw-
other::---
```
- Unlimited entries for specific users OR groups
- Can grant access to multiple groups with different permissions
- Still respects the mask (permission ceiling)

### When to Use ACL

Use ACL when:
- Multiple teams/groups need different levels of access to the same file
- You don't want to change file ownership
- You don't want to use `chmod 777` to give group access
- You need more flexibility than basic permissions provide

### The '+' Sign

When a file has ACL entries, `ls -l` shows a '+' at the end:
```bash
-rw-r-----+ 1 root root 100 Mar 8 12:00 heroes.txt
                               ↑
                         This '+' means ACL entries exist
```

Use `getfacl` to see what those ACL entries are.

## Prerequisites

- Linux system with ACL support (most modern Linux distributions)
- `setfacl` and `getfacl` tools installed (usually pre-installed)
- Access to run `sudo` commands

Check prerequisites:
```bash
which setfacl
which getfacl
```

## Files in This Lab

```
linux_lab13_acl_groups/
├── README.md                  (this file)
├── start_here.txt             (10-step lab instructions)
├── setup_environment.sh        (instructor setup script)
├── .gitignore                 (git config)
└── my_answers.txt             (YOUR ANSWERS GO HERE)
```

## After You Finish

- Write all your answers in `my_answers.txt`
- Make sure you can explain each step to someone else
- Think about where you'd use ACL in a real-world system
  - Shared application logs
  - Shared configuration files
  - Team documentation repositories
  - Multi-team development environments

## Troubleshooting

### "setfacl: command not found"
Your system doesn't have ACL tools. Install them:
```bash
# Ubuntu/Debian
sudo apt-get install acl

# RHEL/CentOS/Fedora
sudo yum install acl
```

### "Permission denied" when running setfacl
You need `sudo` for files you don't own. Use:
```bash
sudo setfacl -m g:superheroes:rw /tmp/heroes.txt
```

### "Group 'superheroes' not found"
The instructor hasn't run the setup script yet. Ask them to run:
```bash
sudo ./setup_environment.sh
```

### ACL entries don't take effect immediately
Try logging out and back in, or use:
```bash
newgrp superheroes
```

## What's Next?

After mastering this lab:
- **Lab 14** (coming soon): SELinux and advanced security contexts
- Explore setfacl with default ACL on directories
- Learn about umask and ACL interaction

## For Instructors

### Lab Difficulty
- **Prerequisites**: Should have completed Lab 12 (Permissions Lab)
- **Estimated Time**: 45-60 minutes
- **Difficulty**: Intermediate (introduces new concepts: ACL, mask)

### Learning Outcomes
By the end of this lab, students should be able to:
- Explain the difference between basic permissions and ACL
- Use `getfacl` to inspect ACL entries on files
- Use `setfacl -m` to add ACL entries for groups
- Use `setfacl -b` to remove all ACL entries
- Understand the ACL mask and how it constrains permissions
- Choose when to use ACL vs basic permissions
- Troubleshoot group membership and ACL issues

### Grading Rubric
- ✅ All 10 steps completed without major errors
- ✅ All questions in `my_answers.txt` answered thoughtfully
- ✅ Demonstrates understanding of ACL concepts (not just rote completion)
- ✅ Can explain real-world use cases for ACL

---

**Linux Course** | **Day 2** | **ACL & Group Permissions Lab** | **Version: v13.0**
