Review a day's content folder for quality, consistency, and completeness.

Usage: /review-day <day-folder>

Example: /review-day Day-1-API-Foundations

Checklist to verify:
1. **English-only** — scan all .md and .py files for Hebrew characters. Flag any found.
2. **README structure** — every subfolder has a README.md with: title, time block, topics, exercise
3. **Runnable code** — every .py file has `if __name__ == "__main__":` and can be parsed with `python -m py_compile`
4. **Naming convention** — folders are numbered `1-`, `2-`, etc. in order
5. **Code conventions**:
   - Functions return `{"success": bool, ...}` or plain data
   - No `requests` imported directly in service layers
   - Decorators ordered: `@log_execution` above `@handle_errors`
6. **Completeness** — exercises have clear requirements and expected output
7. **Evening assignment** — has `services/` + `core/` structure, caching, retry logic

Output format:
- List issues found (file path + line if applicable)
- List things that look good
- Overall score: Ready / Needs Minor Fixes / Needs Major Work
