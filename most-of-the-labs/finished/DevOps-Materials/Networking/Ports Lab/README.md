# Ports Lab

Two FastAPI apps — both configured to bind on port 3000. This lab simulates a real port conflict and walks through diagnosing and resolving it.

---

## Setup

Both apps are configured to start on **port 3000**.

Run the **blue** app in the background, then try to start the **red** app.

> Hint: search `run process in background linux`

Red will fail — the lab starts here.

---

## Part 1: Identify the Error

### Overview

Red crashed — read the error carefully.

### Steps

1. Look at the error message printed by red
2. Identify what kind of error it is

### Hint

Search for: `address already in use uvicorn`

---

## Part 2: Confirm Blue Is Running

### Overview

Verify that blue is actually serving traffic on the port.

> Hint: search `how to send http request from terminal`

---

## Part 3: Identify the Problematic Port

### Overview

Read the error from Part 1 again and extract the port number.

### Steps

1. Re-read the error message
2. Note the port number

### Think About It

- Which app is supposed to use that port?
- Which app is actually holding it?

---

## Part 4: Find the Process Holding the Port

### Overview

Use system tools to find the PID of the process bound to port 3000.

Note the **PID** from the output — you will need it next.

> Hint: search `find process using port linux`

---

## Part 5: Kill the Process and Run Red

### Overview

Free the port by stopping the blue process, then start red in its place.

### Steps

1. Kill the blue process using its PID
2. Confirm the port is now free
3. Start the red app

> Hint: search `kill process by pid linux`

### Expected Behavior

- red starts successfully on port 3000
- `curl localhost:3000` returns the red app response

---

## Part 6: Final Fix – Run Both Apps Together

### Overview

Change red's port in the source code so both apps can run at the same time.

### Steps

1. Find where the port is defined in `red-app/main.py` and change it
2. Start both apps
3. Verify each app responds on its own port

### Expected Output

- `localhost:3000` → blue app response
- `localhost:3001` → red app response
