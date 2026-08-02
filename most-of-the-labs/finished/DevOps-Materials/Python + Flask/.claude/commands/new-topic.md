Create a new numbered topic folder for the current day.

Usage: /new-topic <number> <folder-name> <time-block> <title>

Example: /new-topic 3 Working-With-Requests "11:00–12:15" "Working with requests"

Steps:
1. Create the folder: `Day-X-<day-name>/<number>-<folder-name>/`
2. Create `README.md` with:
   - Title (English only)
   - Time block
   - ## Topics section (bullet list of concepts)
   - ## Exercise section (clear task description with expected output)
3. Create a runnable `.py` file if the topic involves code
4. All text must be in English — no Hebrew anywhere

README structure:
```
# <Title>

**Time:** <time-block>

## Topics
- ...

## Exercise
...
```

Code file conventions:
- Imports at top
- Section comments in English using `# ── Section Name ──────` style
- Every function has a one-line docstring
- `if __name__ == "__main__":` block at the bottom that runs and prints results
