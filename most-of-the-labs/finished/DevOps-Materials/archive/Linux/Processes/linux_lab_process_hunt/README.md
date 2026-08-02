# Linux Lab – Process Hunt (Find & Fix)

A hands-on, 10-step lab for mastering process discovery and termination. You'll learn to find processes, understand their relationships, monitor resources, and decide when (and how) to stop them.

## Overview

This lab merges two concepts into a cohesive troubleshooting workflow:

1. **Finding & monitoring processes** (Steps 1–4)
   - List processes with `ps` and `ps aux`
   - Filter by name with `grep`
   - View process trees with `pstree`
   - Monitor resources in real-time with `top`

2. **Controlling & stopping processes** (Steps 5–7)
   - Use `kill` to send signals (SIGTERM – graceful)
   - Understand when signals work and when they don't
   - Use `kill -9` (SIGKILL) as a last resort
   - Learn the risks of force-killing

3. **Real-world troubleshooting** (Steps 8–10)
   - Handle multiple related processes
   - Diagnose complex scenarios
   - Choose the right strategy
   - Execute the fix safely

## How This Lab Works

Each of the 10 steps has:
- **SETUP script** – Run before starting (creates processes to hunt)
- **Step clue file** – Read to see the task
- **CLEANUP script** – Run after finishing (removes test processes)

Example workflow for Step 1 (from the lab root directory):

```bash
./scripts/setup_step1.sh    # Start test processes
cat clues/step1.txt         # Read the task
# ... do the exercise ...
./scripts/cleanup_step1.sh  # Clean up

cat clues/step2.txt         # Move to Step 2
```

## Direct Entry

Start the lab:

```bash
cat clues/step1.txt
```

(Extract the lab if needed, then `cd linux_lab_process_hunt` first.)

## Prerequisites

- Linux system with standard utilities:
  - `ps` (list processes)
  - `top` (monitor processes)
  - `kill` (send signals)
  - `grep` (filter)
  - `pstree` (optional, but recommended)
- Bash shell
- No sudo needed (you'll manage your own background processes)

## Duration

60–90 minutes (10 steps, ~6–9 min each)

## Learning Objectives

After this lab you will be able to:

- **List and search** processes using `ps`, `ps aux`, and `grep`
- **Understand process relationships** (parent PPID, child processes)
- **Monitor resource usage** with `top` and identify heavy processes
- **Gracefully stop** processes using `kill` (SIGTERM signal 15)
- **Force-kill** stubborn processes using `kill -9` (SIGKILL signal 9)
- **Diagnose real-world scenarios** with multiple processes and competing signals
- **Choose the right strategy** (gentle vs force, target vs parent)
- **Understand the trade-offs** (data loss, corruption, orphaned processes)
- **Troubleshoot** stuck or runaway processes on a real Linux system

## Lab Structure

| Step | Focus | Time | Key Concept |
|------|-------|------|-------------|
| 1 | List all processes | 5 min | `ps` and `ps aux` |
| 2 | Filter by name | 5 min | `grep` filtering |
| 3 | Parent/child relationships | 5 min | PPID, `pstree` |
| 4 | Monitor resources | 5 min | `top`, CPU, memory |
| 5 | First kill | 5 min | `kill`, SIGTERM (graceful) |
| 6 | Understand signals | 5 min | How SIGTERM works |
| 7 | Last resort | 5 min | `kill -9`, SIGKILL (force) |
| 8 | Multiple processes | 5 min | Parent/child strategies |
| 9 | Real-world hunt | 10 min | Apply all skills |
| 10 | Synthesis challenge | 15 min | Capstone exercise |

## Tips & Hints

- **Stuck on a step?** Check `data/secrets/tips.txt` for hints
- **Want a hint inside a step?** Look for "Hint:" in the clue file
- **Process won't die?** You might need `kill -9` – but only if gentle kill fails
- **Processes accumulating?** Run the CLEANUP script if you skip a step
- **Want to see process tree?** Try `pstree -p` (if installed)
- **Want to list your own background processes?** Start with `ps aux | grep $USER`

## Understanding Signals

The lab teaches two main signals:

| Signal | Name | Effect | Use Case |
|--------|------|--------|----------|
| 15 (SIGTERM) | Terminate | Graceful shutdown (process can ignore or clean up) | First choice, always try this first |
| 9 (SIGKILL) | Kill | Immediate termination (can't be ignored) | Last resort, when SIGTERM fails |

There are 60+ signals. To explore:

```bash
man 7 signal    # List all signals
kill -l         # Quick list of signal names
```

## Troubleshooting

**Problem: "Permission denied" when running kill**
- You can only kill your own processes (or use `sudo` for others)
- The lab uses your own background processes

**Problem: Process won't stop even with `kill -9`**
- Unlikely! `kill -9` always works
- Double-check the PID (might be a different process)
- Verify with `ps aux | grep <name>`

**Problem: Child processes become orphaned**
- Normal! When a parent dies, children are reparented to init (PID 1)
- Clean them up with their own PID: `kill <child_PID>`

**Problem: Too many processes listed?**
- Filter by user: `ps aux | grep $USER`
- Filter by name: `ps aux | grep bash`
- Count: `ps aux | wc -l`

## Instructor Notes

- Each step is independent; students can skip ahead if confident
- Cleanup scripts ensure no zombie processes between steps
- All test processes are harmless (dummy, sleep, or custom test scripts)
- Students can re-run steps without losing progress
- Answers are self-graded (students write to `my_answers.txt`)
- No global setup/cleanup needed – it's per-step

## Next Steps After the Lab

- **Monitor long-running processes**: Learn about `nohup` and `&`
- **Process groups & jobs**: `jobs`, `fg`, `bg`, `disown`
- **Signal handling**: `trap` in bash scripts
- **Resource limits**: `ulimit`, `/proc/<pid>/limits`
- **Advanced tools**: `lsof`, `strace`, `systemd`

## Files & Structure

```
linux_lab_process_hunt/
├── README.md              (this file)
├── clues/
│   ├── step1.txt         (find processes)
│   ├── step2.txt         (filter by name)
│   ├── step3.txt         (parent/child)
│   ├── step4.txt         (monitor with top)
│   ├── step5.txt         (first kill)
│   ├── step6.txt         (SIGTERM)
│   ├── step7.txt         (kill -9)
│   ├── step8.txt         (multiple processes)
│   ├── step9.txt         (real-world hunt)
│   └── step10.txt        (synthesis challenge)
├── scripts/
│   ├── setup_step1.sh through setup_step10.sh
│   └── cleanup_step1.sh through cleanup_step10.sh
├── data/
│   └── secrets/
│       └── tips.txt       (optional hints)
├── my_answers.txt         (student writes here)
└── .answers/
    └── solutions.txt      (instructor reference)
```

## Version

- **Version:** 2.0 (merged from "Processes Basics" v1.0 and "Process Kill" v1.0)
- **Format:** 10-step unified lab
- **Repository:** https://github.com/IITC-College/DevOps-Jan26
- **Last Updated:** 2026

---

**Start here:** `cat clues/step1.txt`

Happy hunting! 🔍
