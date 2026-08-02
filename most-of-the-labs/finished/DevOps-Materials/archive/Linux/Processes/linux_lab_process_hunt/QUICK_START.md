# Process Hunt Lab – Quick Start

## Start Here

```bash
# Extract the lab
tar -xzf linux_lab_process_hunt.tar.gz
cd linux_lab_process_hunt

# Read the first step
cat clues/step1.txt
```

## Each Step Follows This Pattern

```bash
# 1. Start the test processes
./scripts/setup_step1.sh

# 2. Read the task
cat clues/step1.txt

# 3. Do the exercise (follow instructions in the clue file)
# ... use ps, top, kill, grep, etc. ...
# ... write your answer in my_answers.txt ...

# 4. Clean up
./scripts/cleanup_step1.sh

# 5. Move to the next step
cat clues/step2.txt
```

## The 10 Steps at a Glance

| # | Topic | Command | Time |
|---|-------|---------|------|
| 1 | List processes | `ps`, `ps aux` | 5 min |
| 2 | Filter by name | `grep` | 5 min |
| 3 | Parent/child | `pstree`, `ps auxf` | 5 min |
| 4 | Monitor resources | `top` | 5 min |
| 5 | Kill gracefully | `kill <PID>` | 5 min |
| 6 | SIGTERM | understand signals | 5 min |
| 7 | Force kill | `kill -9 <PID>` | 5 min |
| 8 | Multiple processes | parent/child strategies | 5 min |
| 9 | Real-world hunt | apply skills | 10 min |
| 10 | Full challenge | synthesis | 15 min |

## Key Commands You'll Use

```bash
# List processes
ps aux

# Monitor live
top

# Filter
ps aux | grep bash

# See process tree
pstree -p
ps auxf

# Kill gracefully
kill <PID>

# Force kill (last resort!)
kill -9 <PID>

# Check if running
ps aux | grep <name>
```

## Need Help?

- **During a step?** Check `data/secrets/tips.txt` for hints
- **About commands?** Use `man ps`, `man kill`, `man top`
- **Answers?** Compare with `.answers/solutions.txt` (instructor reference)

## Save Your Answers

Write your answers in `my_answers.txt` as you go. Format:

```
Step 1: [your answer]
Step 2: [your answer]
...
```

## Expected Duration

- **Quick pace**: 60–70 minutes
- **Normal pace**: 75–90 minutes
- **With exploration**: 90–120 minutes

## Remember

- ✅ Always try `kill` (gentle) first
- ✅ Only use `kill -9` if gentle kill doesn't work
- ✅ Run CLEANUP scripts between steps
- ✅ Write your answers as you go
- ✅ Ask for hints if stuck (they're in data/secrets/tips.txt)

---

**Ready?** Start with `cat clues/step1.txt` 🚀
