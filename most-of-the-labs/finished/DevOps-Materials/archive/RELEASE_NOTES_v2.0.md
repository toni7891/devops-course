# Release Notes – Process Hunt Lab v2.0

**Release Date:** March 9, 2026
**Tag:** `v2.0-process-hunt`
**Commit:** af791e4

## Overview

Process Hunt Lab v2.0 is a **unified, 10-step lab** that merges two separate process labs into a cohesive troubleshooting workflow. This release represents a significant improvement in structure, pedagogy, and student experience.

## What's Included

### New Lab
- **linux_lab_process_hunt.tar.gz** – Production-ready lab (15 KB)
- **linux_lab_process_hunt/** – Full source directory with 37 files

### Key Files
- **README.md** – Comprehensive guide (2,700+ lines)
- **QUICK_START.md** – One-page reference for students
- **10 step clues** – step1.txt through step10.txt
- **20 scripts** – setup_step1-10.sh and cleanup_step1-10.sh
- **my_answers.txt** – Student answer template
- **.answers/solutions.txt** – Instructor solutions with examples
- **data/secrets/tips.txt** – Hints for stuck students

## Changes From Previous Release

### Deleted (Legacy Labs)
```
❌ linux_lab_processes_basics.tar.gz (v1.0)
❌ linux_lab_processes_kill.tar.gz (v1.0)
```

### Added (New Unified Lab)
```
✅ linux_lab_process_hunt.tar.gz (v2.0)
✅ linux_lab_process_hunt/ (full source)
```

## The 10 Steps

| Step | Topic | Focus | Duration |
|------|-------|-------|----------|
| 1 | List all processes | `ps`, `ps aux` | 5 min |
| 2 | Filter by name | `grep` piping | 5 min |
| 3 | Parent/child relationships | PPID, `pstree` | 5 min |
| 4 | Monitor resources | `top`, CPU, memory | 5 min |
| **5** | **First kill** | **`kill`, SIGTERM** | **5 min** |
| **6** | **Understand signals** | **SIGTERM explained** | **5 min** |
| **7** | **Last resort** | **`kill -9`, SIGKILL** | **5 min** |
| **8** | **Multiple processes** | **Strategy & decision** | **5 min** |
| **9** | **Real-world hunt** | **Apply all skills** | **10 min** |
| **10** | **Synthesis challenge** | **Capstone exercise** | **15 min** |

**Total Duration:** 60–90 minutes

## Learning Progression

### Phase 1: Discovery (Steps 1–4)
Students learn to find and observe processes:
- ✅ List processes with `ps` and `ps aux`
- ✅ Filter with `grep`
- ✅ Understand relationships (parent/child, PPID)
- ✅ Monitor resources in real-time with `top`

### Phase 2: Control (Steps 5–8)
Students learn to stop processes strategically:
- ✅ Graceful stop with `kill` (SIGTERM)
- ✅ How signals work
- ✅ Force-kill with `kill -9` (SIGKILL) as last resort
- ✅ Handle multiple processes and parent/child strategies

### Phase 3: Application (Steps 9–10)
Students apply all skills in realistic scenarios:
- ✅ Real-world troubleshooting
- ✅ Synthesis and decision-making
- ✅ Complex multi-process scenarios

## Key Improvements

### 1. Structure
- **Before:** Two separate labs (levels/clues format)
- **After:** Single cohesive 10-step progression
- **Benefit:** Clear narrative, easier navigation

### 2. Learning Progression
- **Before:** Discover in one lab, control in another
- **After:** Linear: Find → Monitor → Understand → Control → Troubleshoot
- **Benefit:** Realistic workflow, better retention

### 3. Documentation
- **Before:** Basic README, minimal guidance
- **After:** Comprehensive guide + quick start + tips + solutions
- **Benefit:** Support for students and instructors

### 4. Student Experience
- **Before:** Answer template scattered across clues
- **After:** Unified `my_answers.txt` for all steps
- **Benefit:** Cleaner, more organized

### 5. Instructor Support
- **Before:** Solutions in hidden folder
- **After:** `.answers/solutions.txt` with examples and grading notes
- **Benefit:** Easier assessment and feedback

### 6. Automation
- **Before:** Inconsistent setup/cleanup
- **After:** Complete, tested scripts for all 10 steps
- **Benefit:** Reliable process management

## Migration Guide

### For Students
No action needed. Simply:
```bash
tar -xzf linux_lab_process_hunt.tar.gz
cd linux_lab_process_hunt
cat clues/step1.txt
```

### For Instructors
1. **Replace old labs:**
   - Remove: `linux_lab_processes_basics.tar.gz`
   - Remove: `linux_lab_processes_kill.tar.gz`
   - Use: `linux_lab_process_hunt.tar.gz`

2. **Review new structure:**
   - See `README.md` for comprehensive guide
   - See `.answers/solutions.txt` for grading reference

3. **Give students hints if needed:**
   - Direct them to `data/secrets/tips.txt` in the lab directory

### For Courses
- Update syllabus/schedule from "Processes Basics" + "Process Kill" to "Process Hunt"
- Adjust duration if needed (merged labs may be more efficient)
- Consider using this as foundation for advanced process management topics

## Compatibility

- **OS:** Linux (tested on Ubuntu, CentOS, Debian)
- **Shell:** Bash
- **Tools Required:** `ps`, `top`, `kill`, `grep`, `pstree` (optional)
- **Prerequisites:** Basic Linux command line knowledge

## Testing Completed

✅ All 10 step clues created and reviewed
✅ All 20 setup/cleanup scripts created and tested
✅ README comprehensive and complete
✅ Student templates match all steps
✅ Instructor solutions provided with examples
✅ Tips file with helpful hints
✅ Quick start guide created
✅ File structure verified
✅ Tarball packaged and tested
✅ Git commit and tag created

## Deployment Status

🚀 **PRODUCTION READY**

- Immediate deployment to students: ✅
- Course integration: ✅
- GitHub hosting: ✅
- Synchronous delivery: ✅
- Asynchronous/remote delivery: ✅

## Known Limitations

None identified. Lab is fully functional and ready for production use.

## Future Enhancements (v2.1+)

Potential improvements for future releases:
- Interactive script feedback during exercises
- Automated answer validation
- Video walkthrough for each step
- Web-based interface
- Docker-based testing environment
- Advanced signal handling (SIGSTOP, SIGCONT, etc.)

## Support & Feedback

- **Questions?** See `README.md` in the lab directory
- **Issues?** Check `.answers/solutions.txt` or `data/secrets/tips.txt`
- **Improvements?** Submit feedback or patches

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| v2.0 | Mar 9, 2026 | ✅ Released | Unified lab (merged basics + kill) |
| v1.1 | Jan 29, 2026 | Archived | Last release of separate labs |

## Credits

- **Merged from:** linux_lab_processes_basics v1.0 + linux_lab_processes_kill v1.0
- **Enhanced by:** Comprehensive restructuring and documentation
- **Tested by:** Production readiness verification

## License

Same as repository (see LICENSE file)

---

## Quick Links

- **Lab Location:** `Linux/Processes/linux_lab_process_hunt.tar.gz`
- **Source Directory:** `Linux/Processes/linux_lab_process_hunt/`
- **README:** `Linux/Processes/linux_lab_process_hunt/README.md`
- **Quick Start:** `Linux/Processes/linux_lab_process_hunt/QUICK_START.md`
- **Solutions:** `Linux/Processes/linux_lab_process_hunt/.answers/solutions.txt`
- **Hints:** `Linux/Processes/linux_lab_process_hunt/data/secrets/tips.txt`

---

**Ready to use?** Start with: `cat Linux/Processes/linux_lab_process_hunt/clues/step1.txt`
