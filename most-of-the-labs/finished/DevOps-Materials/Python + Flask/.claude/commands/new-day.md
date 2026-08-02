Scaffold a complete new day folder from a lesson plan.

Usage: /new-day <number> <day-name> <goal>

Example: /new-day 2 Flask-Basics "Build a REST API with Flask from scratch"

What to create:
1. `Day-<number>-<day-name>/` folder
2. `README.md` with:
   - Day number and title
   - Goal line
   - Schedule table (Time | Topic | Folder columns)
   - "By end of Day N, students will:" bullet list
3. Numbered topic subfolders (1 through 7) based on the lesson plan provided
4. Each subfolder gets a `README.md` and `.py` files as appropriate
5. Final subfolder (6) is always the in-class final exercise with `core/` structure
6. Last subfolder (7) is always the evening assignment with `services/` + `core/` structure

Folder naming: `Day-<number>-<day-name>/`
All content in English. No Hebrew anywhere.

After scaffolding, summarize:
- What was created
- Which folders need code files added
- Any assumptions made about the lesson plan
