# Topic 2 — MongoDB Atlas Setup

**Time:** 10:00–11:00 (60 min)

> CRITICAL: Do this live with every student. Do not move on until every person has a working connection string. If a student cannot connect, they cannot participate in the rest of the day.

---

## Instructor Preparation

Before class:
- Create a backup cluster of your own with a ready-to-share connection string
- Test the connection string yourself from a clean environment
- Know the three failure modes (covered in Topic 4) so you can triage quickly

---

## Step-by-Step Setup

### Step 1 — Create an Account

1. Go to [mongodb.com/atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up with email or Google
3. Choose "Build a database" when prompted
4. Select **M0 Free** tier
5. Choose a cloud provider and region (any — pick the closest)
6. Name the cluster (e.g., `Cluster0` is fine)
7. Click **Create**

> Wait ~2 minutes for the cluster to provision.

---

### Step 2 — Create a Database User

In the left sidebar: **Database Access** → **Add New Database User**

| Field | Value |
|-------|-------|
| Authentication | Password |
| Username | `admin` (or your choice) |
| Password | Choose a strong password — **write it down** |
| Role | **Atlas Admin** |

Click **Add User**.

> Common mistake: forgetting the password. Tell students to save it immediately.

---

### Step 3 — Network Access (Allow Connections)

In the left sidebar: **Network Access** → **Add IP Address**

Click **Allow Access from Anywhere** — this sets:
```
0.0.0.0/0
```

Click **Confirm**.

**Why `0.0.0.0/0`?**
- In production you restrict to specific IPs (your server's IP)
- In development we allow all IPs so it works from any machine or network
- This is a deliberate tradeoff for ease of learning

---

### Step 4 — Get the Connection String

In the left sidebar: **Database** → click **Connect** on your cluster

Choose **Connect your application** → Driver: **Python**, Version: **3.6 or later**

Copy the connection string. It looks like:
```
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

Replace `<username>` and `<password>` with the values from Step 2.

---

### Step 5 — Verify It Works

Run this in a Python file or interactive shell:

```python
from pymongo import MongoClient

MONGO_URI = "your_connection_string_here"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print(f"Connection failed: {e}")
```

> Do not proceed until every student sees "Connected to MongoDB Atlas!"

---

## Checkpoint

Every student must have:
- [ ] A cluster in Atlas (green, running)
- [ ] A database user with a known password
- [ ] `0.0.0.0/0` in Network Access
- [ ] A connection string with username/password filled in
- [ ] Successful ping output in their terminal
