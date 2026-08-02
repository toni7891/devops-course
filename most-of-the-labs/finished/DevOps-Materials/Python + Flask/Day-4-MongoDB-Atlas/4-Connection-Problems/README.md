# Topic 4 — Common Connection Problems

**Time:** 12:00–12:30 (30 min)

---

## Objective

Teach students to read PyMongo error messages and self-diagnose the three most common Atlas connection failures — so they are not stuck during the afternoon.

---

## The Three Failure Modes

### 1. Wrong Password

**Error you will see:**
```
pymongo.errors.OperationFailure: bad auth : Authentication failed.
```

**Cause:** The password in the connection string does not match the Atlas database user.

**Fix:**
1. Go to Atlas → Database Access
2. Click **Edit** on the user → **Edit Password** → set a new one
3. Update the connection string with the new password

> Special characters in passwords (`@`, `#`, `!`) must be URL-encoded. Easiest fix: use a password with only letters and numbers.

---

### 2. IP Not Whitelisted

**Error you will see:**
```
pymongo.errors.ServerSelectionTimeoutError: ... connection timeout ...
[SSL: CERTIFICATE_VERIFY_FAILED] or connection refused
```

The connection just hangs and times out.

**Cause:** Your current IP address is not in the Atlas Network Access list.

**Fix:**
1. Go to Atlas → Network Access
2. Click **Add IP Address** → **Allow Access from Anywhere** (`0.0.0.0/0`)
3. Retry the connection

> Changing networks (switching from home WiFi to mobile hotspot) changes your IP and can cause this mid-session.

---

### 3. Wrong Connection String Format

**Error you will see:**
```
pymongo.errors.ConfigurationError: ... is not a valid URI ...
```
or
```
pymongo.errors.InvalidURI: ...
```

**Common causes:**
- Still has the literal `<username>` or `<password>` placeholders
- Missing `@` between credentials and host
- Extra spaces copied from the Atlas UI

**Fix:** Re-copy the string from Atlas, replace placeholders manually, paste into a text editor first to check.

---

## Diagnostic Decision Tree

```
Connection fails?
    │
    ├── "Authentication failed" → wrong password
    │
    ├── "Timeout" or hangs → IP not whitelisted
    │
    └── "Invalid URI" or "ConfigurationError" → bad connection string
```

---

## Exercise: `diagnose.py`

A script that gives a clear error message for each failure mode:

```bash
python diagnose.py
```

Students run this to verify their connection before the afternoon session.
