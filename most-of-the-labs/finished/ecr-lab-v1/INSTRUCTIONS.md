# ECR Lab — הוראות

---

## 🎯 מטרות הלמידה

- נארוז אפליקציית Node.js לתוך Docker Image
- ניצור ECR Repository ונבצע Authentication
- נדחוף את ה-Image ל-ECR באופן עצמאי

---

## 📦 קוד האפליקציה

נשתמש באפליקציית Node.js פשוטה הנמצאת ב-Repository. נשכפל אותה מ-GitHub:

```bash
git clone https://github.com/IITC-College/ecr-lab-v1.git
cd ecr-lab-v1
npm install
```

האפליקציה מריצה Jokes API פשוט על פורט 3000. ניתן לבדוק שהיא עובדת:

```bash
npm start
# http://localhost:3000
```

---

## 📋 משימות

### חלק א — בניית ה-Image מקומית

1. נבנה Docker Image מה-Dockerfile שב-Repository:
```bash
docker build -t ecr-demo .
```

2. נריץ את ה-Image מקומית ונוודא שהאפליקציה מגיבה על פורט 3000:
```bash
docker run -p 3000:3000 ecr-demo
```

---

### חלק ב — הכנת ECR

1. ניצור ECR Repository פרטי חדש דרך ה-AWS Console
2. נבצע Authentication מהמחשב המקומי מול ECR:
```bash
aws ecr get-login-password --region <region> | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

---

### חלק ג — Tag ו-Push

1. נבצע Tag ל-Image עם ה-URI של ה-Repository:
```bash
docker tag ecr-demo <account-id>.dkr.ecr.<region>.amazonaws.com/ecr-demo:latest
```

2. נדחוף את ה-Image ל-ECR:
```bash
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ecr-demo:latest
```

3. נאמת ב-Console שה-Image הופיע ב-Repository

---

⚠️ **לתשומת לב:** יש להחליף את `<account-id>` ו-`<region>` בערכים האמיתיים מה-Console שלכם.
