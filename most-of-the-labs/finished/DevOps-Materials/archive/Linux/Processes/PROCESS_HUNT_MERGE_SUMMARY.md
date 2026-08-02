# Process Hunt Lab – Merge Summary

## What Was Done

Two separate labs were merged into a single, unified **10-step Process Hunt lab**:

### Original Labs
1. **linux_lab_processes_basics.tar.gz** (v1.0)
   - 3 levels × 3 clues = 9 exercises
   - Focus: Finding and observing processes (ps, top, parent/child)

2. **linux_lab_processes_kill.tar.gz** (v1.0)
   - 2 levels × 3 clues = 6 exercises
   - Focus: Killing processes (kill, SIGTERM, kill -9)

### New Merged Lab
**linux_lab_process_hunt.tar.gz** (v2.0)
- **10 sequential steps** (not levels/clues)
- **Cohesive workflow**: Find → Monitor → Control
- **Better format**: Linear progression, clearer learning arc
- **Enhanced structure**:
  - Each step has setup/cleanup scripts
  - Student answer template (my_answers.txt)
  - Instructor solutions (.answers/solutions.txt)
  - Tips file (data/secrets/tips.txt)

## Step Progression

| Step | Topic | Source | Time |
|------|-------|--------|------|
| 1 | List all processes | Basics L1C1 | 5 min |
| 2 | Filter by name | Basics L1C2 | 5 min |
| 3 | Parent/child (PPID) | Basics L3C1 | 5 min |
| 4 | Monitor with top | Basics L2C1-2 | 5 min |
| 5 | First kill (gentle) | Kill L1C1 | 5 min |
| 6 | SIGTERM (graceful) | Kill L1C2 | 5 min |
| 7 | kill -9 (force) | Kill L2C1 | 5 min |
| 8 | Multiple processes | Kill L2C2 | 5 min |
| 9 | Real-world hunt | Combined concept | 10 min |
| 10 | Synthesis challenge | Combined/enhanced | 15 min |

## Key Improvements

### 1. **Better Learning Arc**
   - **Before**: Two separate labs with no connection
   - **After**: Single narrative: "Find processes → Understand them → Control them"

### 2. **Clearer Structure**
   - **Before**: "Level 1, Level 2" with unclear progression
   - **After**: "Step 1 of 10, Step 2 of 10" – students always know where they are

### 3. **Realistic Workflow**
   - **Before**: Find processes in one lab, kill them in another
   - **After**: Real troubleshooting scenario: "Something is wrong. Hunt it. Fix it."

### 4. **Student-Friendly**
   - **Before**: Answers/solutions in a hidden folder
   - **After**: Dedicated `my_answers.txt` template matching each step

### 5. **Instructor-Ready**
   - **Before**: Basic README and solutions
   - **After**:
     - Detailed README with learning objectives and duration
     - Full solution examples
     - Grading notes
     - Tips for instructors

### 6. **Better Setup/Cleanup**
   - **Before**: 6 setup/cleanup scripts for processes basics, 6 for kill (12 total, some missing)
   - **After**: 20 targeted scripts (setup + cleanup for each step, all complete)

## File Structure

```
linux_lab_process_hunt/
├── README.md                          (comprehensive guide)
├── clues/
│   ├── step1.txt ... step10.txt       (10 sequential clues)
├── scripts/
│   ├── setup_step1.sh ... setup_step10.sh
│   └── cleanup_step1.sh ... cleanup_step10.sh
├── data/
│   └── secrets/
│       └── tips.txt                   (hints for students)
├── my_answers.txt                     (student answer template)
├── .answers/
│   └── solutions.txt                  (instructor reference)
├── .gitignore
└── [no start_here.txt needed]         (starts directly with step 1)
```

## Usage

### Starting the Lab
```bash
cd linux_lab_process_hunt
cat clues/step1.txt
```

### Per-Step Workflow
```bash
./scripts/setup_step1.sh       # Before starting
cat clues/step1.txt            # Read the task
# ... do the exercise ...
./scripts/cleanup_step1.sh     # After finishing

cat clues/step2.txt            # Next step
```

### For Instructors
- **Reference answers**: `.answers/solutions.txt`
- **Student progress**: `my_answers.txt` (collected after lab)
- **Hints**: `data/secrets/tips.txt` (give to students who ask)

## Duration

- **Before**: ~40–45 min (Basics) + ~20–25 min (Kill) = 60–70 min total
- **After**: ~60–90 min (unified), same content, better paced

## What Gets Removed

The original two labs are still in the repository as `.tar.gz` files, but the new merged lab is the preferred path forward:
- `linux_lab_processes_basics.tar.gz` – legacy (can be archived)
- `linux_lab_processes_kill.tar.gz` – legacy (can be archived)
- `linux_lab_process_hunt.tar.gz` – new standard

## Testing the Lab

Quick test:
```bash
cd linux_lab_process_hunt
tar -tzf ../linux_lab_process_hunt.tar.gz | wc -l  # Should list ~50+ files
./scripts/setup_step1.sh      # Should succeed
ps aux | wc -l                # Should show normal output
./scripts/cleanup_step1.sh    # Should succeed
```

## Version Info

- **New Lab Version**: 2.0 (merged)
- **Source Lab Versions**: 1.0 (Processes Basics) + 1.0 (Process Kill)
- **Format**: 10-step unified (not levels)
- **Status**: Ready for student deployment

## Next Steps

1. ✅ **Done**: Create merged lab structure with 10 steps
2. ✅ **Done**: Write all step clues (1–10)
3. ✅ **Done**: Create all setup/cleanup scripts
4. ✅ **Done**: Create README with learning objectives
5. ✅ **Done**: Create student answer template
6. ✅ **Done**: Create instructor solutions
7. ✅ **Done**: Add tips file
8. ✅ **Done**: Package as tarball
9. **Next**: Deploy to students or update course materials
10. **Next**: Retire old labs (keep as archive if needed)

---

**Lab Ready for Deployment!** 🚀

Questions? See README.md or .answers/solutions.txt
