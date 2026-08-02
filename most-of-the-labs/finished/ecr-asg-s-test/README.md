# ecr-asg-s-test

Node.js / Express app for ECS Auto Scaling stress testing. Exposes three endpoints:

| Endpoint | Description |
| --- | --- |
| `GET /` | Health check — returns `Hello from ECR!` |
| `GET /cpu` | Runs a CPU-intensive loop |
| `GET /memory` | Allocates ~400 MB of memory |

---

## Run Locally

```bash
npm install
node app.js
```

## Run with Docker

```bash
docker build -t ecr-asg-s-test .
docker run -p 3000:3000 ecr-asg-s-test
```

## Push to ECR

```bash
docker buildx build --platform linux/amd64 \
  -t <account-id>.dkr.ecr.<region>.amazonaws.com/ecr-demo:latest \
  --push .
```

Then update the ECS Task Definition to the new revision and update the Service.

---

## 🎯 מטרות הלמידה

- הגדרת Auto Scaling לפי CPU וגם Memory
- ביצוע Stress Test שיגרום Scale Out על שני המדדים
- צפייה ב-CloudWatch שה-Tasks עולים

---

## דרישות מקדימות

- יש לך ECS Service פעיל ממעבדות קודמות

---

## חלק א — עדכון ה-App לעומס CPU ו-Memory

הקוד כבר מעודכן ב-[app.js](app.js) עם Express ועם שני ה-endpoints.

```bash
docker buildx build --platform linux/amd64 \
  -t <account-id>.dkr.ecr.<region>.amazonaws.com/ecr-demo:latest \
  --push .
```

נעדכן את ה-Task Definition ל-Revision חדשה ונעדכן את ה-Service.

---

## חלק ב — הגדרת Auto Scaling

1. נכנסים ל-Service ולחצים **Update Service**
2. תחת **Service Auto Scaling** מאפשרים ומגדירים:

| שדה | ערך |
| --- | --- |
| Minimum tasks | `1` |
| Maximum tasks | `4` |

3. מוסיפים **שתי** Scaling Policies:

**Policy 1 — CPU:**

| שדה | ערך |
| --- | --- |
| Policy type | Target Tracking |
| Metric | ECSServiceAverageCPUUtilization |
| Target value | `30` |

**Policy 2 — Memory:**

| שדה | ערך |
| --- | --- |
| Policy type | Target Tracking |
| Metric | ECSServiceAverageMemoryUtilization |
| Target value | `50` |

4. שומרים

---

## חלק ג — Stress Test

### בדיקת CPU

```bash
hey -n 500 -c 50 http://<public-ip>:3000/cpu
```

### בדיקת Memory

```bash
hey -n 200 -c 20 http://<public-ip>:3000/memory
```

אלטרנטיבה ללא `hey`:

```bash
# CPU stress
for i in {1..200}; do curl -s http://<public-ip>:3000/cpu & done

# Memory stress
for i in {1..100}; do curl -s http://<public-ip>:3000/memory & done
```

---

## חלק ד — צפייה

1. נצפים ב-ECS Console שעצמת ה-Tasks עולה
2. ננווט ל-CloudWatch → Metrics → ECS ונצפים בגרפי CPU ו-Memory במקביל

---

⚠️ **לתשומת לב:**

- Scale Out יתרחש אם **אחד** מהמדדים עולה מעל ה-Target — לא צריך שנייהם יעלו בו-זמנית
- Scale In לוקח יותר זמן — ברירת מחדל 15 דקות
