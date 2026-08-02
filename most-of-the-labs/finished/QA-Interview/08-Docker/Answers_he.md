# תשובות ראיון Docker

**ש1. מהי Docker image?**
תבנית ליצירת קונטיינרים — מכילה קוד, ספריות והגדרות להרצת אפליקציה בסביבה מבודדת.

**ש2. מהו Docker host?**
המחשב שעליו מותקן Docker. הוא מריץ ומנהל קונטיינרים — בין אם על מחשב מקומי, VM או ענן.

**ש3. מה ההבדל בין Docker client ל-Docker daemon?**
ה-client שולח פקודות (כמו `docker run`), ה-daemon מקבל ומבצע אותן. הם יכולים לרוץ על אותה מכונה או על מכונות שונות.

**ש4. מהי רשת Docker? איך יוצרים רשתות bridge/overlay?**
רשת מאפשרת תקשורת בין קונטיינרים. Bridge (אותו host): `docker network create -d bridge my-bridge-network`. Overlay (בין hosts): `docker network create --scope=swarm -d overlay my-overlay`.

**ש5. איך עובדת רשת bridge ב-Docker?**
מצב הרשת הברירת-מחדל. כל קונטיינר מקבל IP ייחודי ויכול לתקשר עם קונטיינרים אחרים על אותה bridge.

**ש6. מהו Dockerfile?**
סקריפט הוראות בנייה. מגדיר image בסיס, תיקיית עבודה, העתקת קבצים, התקנת תלויות, פורטים פתוחים ופקודת הפעלה — כל שלב יוצר שכבה.

**ש7. מהו Docker Compose? במה הוא שונה מ-Dockerfile?**
Compose מנהל אפליקציות רב-קונטיינר דרך קובץ YAML. Dockerfile בונה image אחד; Compose מפעיל ומחבר מספר קונטיינרים יחד.

**ש8. למה משתמשים ב-volumes?**
Volumes שומרים מידע מחוץ לקונטיינר כך שהוא נשמר גם אחרי מחיקתו. קל לגבות אותם ולשתף בין קונטיינרים.

**ש9. מהם bind mounts? למה עדיף volumes?**
Bind mounts מקשרים נתיב מהמחשב המארח לקונטיינר. Volumes עדיפים כי הם לא תלויי מערכת הפעלה, קלים יותר לניהול ומאובטחים יותר.

**ש10. מהו Docker Swarm?**
כלי תזמור מובנה של Docker. מנהל אשכול של nodes, מאפשר load balancing, סקיילינג וזמינות גבוהה.

**ש11. האם Docker Swarm תומך ב-autoscale?**
לא באופן מובנה. ניתן לממש זאת ידנית עם כלי ניטור כמו Prometheus שמפעילים פקודת `docker service scale`.

**ש12. איך מגדילים שירות ב-Docker Compose?**
עם דגל `--scale`: `docker-compose up --scale web=3` מריץ 3 instances של שירות ה-`web`.

**ש13. האם קונטיינרים יכולים לעלות מחדש אוטומטית?**
כן. ברירת המחדל היא `no` (ללא הפעלה מחדש). שימוש ב-`--restart=always` מפעיל מחדש את הקונטיינר בכל פעם שהוא נעצר.

**ש14. מהו מחזור החיים של קונטיינר Docker?**
יצירה ← הרצה ← השהייה ← עצירה ← מחיקה. קונטיינר יכול להיעצר על ידי פקודה, סיום התהליך, או OOM kill.

**ש15. מהו Docker image repository?**
מערכת אחסון ל-images עם גרסאות וסימוני tag. Docker Hub הוא הנפוץ ביותר; אלטרנטיבות כוללות Amazon ECR ו-GitHub Container Registry.

**ש16. ציין שלוש שיטות אבטחה לקונטיינרים.**
1. השתמש ב-images קטנים (כמו Alpine).
2. הגבל syscalls עם Seccomp.
3. השתמש ב-Docker secrets לנתונים רגישים במקום משתני סביבה.

**ש17. למה קונטיינרים צריכים health checks?**
כדי לזהות מתי קונטיינר שרץ הפסיק לתפקד (תקוע או לא מגיב) — ואז ניתן להפעיל אותו מחדש או להחליפו.

**ש18. מהם dangling images? איך מסירים אותם?**
שכבות image לא בשימוש ללא tag, שמבזבזות מקום. איתור: `docker images -f dangling=true`. הסרה: `docker image prune -f`.

**ש19. מה ההבדל בין Docker ל-Kubernetes?**
Docker בונה ומריץ קונטיינרים בודדים. Kubernetes מתזמר קונטיינרים רבים על פני אשכול עם סקיילינג אוטומטי, load balancing ותיקון עצמי.

**ש20. Docker Swarm לעומת Kubernetes?**
Swarm פשוט יותר ומתאים לסביבות קטנות. Kubernetes עוצמתי יותר, עם תיקון עצמי, ניטור ותמיכה בפריסות גדולות.

**ש21. איך Kubernetes מנהל מספר גדול של קונטיינרים?**
דרך תזמון חכם, הקצאת משאבים על פני nodes, סקיילינג אוטומטי לפי עומס — ותיקון עצמי כשקונטיינרים נכשלים.

**ש22. מהו Kubernetes Pod?**
היחידה הקטנה ביותר ב-Kubernetes. Pod מקבץ קונטיינר אחד או יותר שחולקים רשת ואחסון — בניגוד לקונטיינרים שמבודדים אחד מהשני.

**ש23. איך מנהלים מידע רגיש ב-Docker וב-Kubernetes?**
Docker: Docker secrets — מוצפן ונגיש רק בזמן ריצה. Kubernetes: אובייקטי Secret — מוזרקים כ-volumes או משתני סביבה לתוך ה-pod.

**ש24. איך מקטינים image גדול מבוסס Maven?**
מוסיפים `.dockerignore` להוצאת קבצים מיותרים, ומשתמשים ב-multi-stage build — קומפילציה בשלב אחד, העתקת artifact בלבד ל-image קטן ורזה.

**ש25. איך מעלים Docker images ל-Docker Hub דרך Jenkins?**
מגדירים Jenkins pipeline עם Jenkinsfile שבונה את ה-image, מתחבר ל-Docker Hub עם credentials שמורים, ומעלה את ה-image אוטומטית.

**ש26. איך מעבירים קונטיינר WordPress לשרת חדש ללא אובדן מידע?**
1. גיבוי מידע: `docker cp <container>:/var/www/html ./backup`
2. העברה לשרת חדש: `scp`
3. הפעלת קונטיינרים בשרת היעד
4. שחזור ה-volume לפני ההפעלה
