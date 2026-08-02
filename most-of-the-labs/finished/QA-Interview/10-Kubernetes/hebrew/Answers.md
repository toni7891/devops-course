# תשובות ראיון Kubernetes

**ש1. איך מבצעים פעולת תחזוקה על node ב-K8s?**
פעולות תחזוקה הן חלק בלתי נמנע מהאדמיניסטרציה — לעיתים יש צורך ב-patching או בהחלת תיקוני אבטחה על K8s. יש לסמן את ה-node כ-unschedulable ולאחר מכן לבצע drain ל-PODs שנמצאים עליו.

- `kubectl cordon <hostname>`
- `kubectl drain --ignore-daemonsets <hostname>`

חשוב לכלול את `--ignore-daemonsets` עבור כל DaemonSet שרץ על ה-node. אם StatefulSet רץ על ה-node הזה ואין node אחר פנוי לשמור על מספר ה-replicas, ה-POD של ה-StatefulSet יישאר במצב pending.

**ש2. מה התפקיד של pause container?**
ה-pause container משמש כקונטיינר ההורה לכל הקונטיינרים ב-POD.

- הוא מהווה את הבסיס לשיתוף namespace ב-Linux בתוך ה-POD.
- הוא PID 1 של ה-POD ואוסף תהליכי zombie.

https://www.ianlewis.org/en/almighty-pause-container

**ש3. למה צריך service mesh?**
service mesh מבטיח שהתקשורת בין שירותי תשתית קונטיינריזציה, שלעיתים הם אפמריים, תהיה מהירה, אמינה ומאובטחת. ה-mesh מספק יכולות קריטיות כמו service discovery, load balancing, הצפנה, observability, traceability, אימות והרשאות, ותמיכה ב-circuit breaker pattern.

**ש4. איך שולטים על ניצול המשאבים של POD?**
באמצעות requests ו-limits אפשר לשלוט בניצול המשאבים של POD.

- **request**: כמות המשאבים המבוקשת לקונטיינר. אם קונטיינר חוצה את ה-request שלו, הוא עשוי להיות מוגבל (throttled) בחזרה אל ה-request.
- **limit**: תקרה עליונה לכמות המשאבים שקונטיינר יכול לנצל. אם הוא מנסה לחצות את ה-limit, ייתכן שיופסק אם Kubernetes מחליטה שקונטיינר אחר צריך את המשאבים. אם רגישים ל-restart של pods, רצוי שסכום כל ה-limits של הקונטיינרים יהיה שווה או קטן מקיבולת המשאבים הכוללת של ה-cluster.

https://www.noqcks.io/notes/2018/02/03/understanding-kubernetes-resources/

**ש5. מהן יחידות המידה של CPU וזיכרון בהגדרת POD?**
CPU נמדד ב-millicores וזיכרון נמדד ב-bytes. ניתן להגביל (throttle) CPU בקלות, אך לא זיכרון.

**ש6. איפה עוד אפשר להגדיר resource limit?**
ניתן גם להגדיר resource limit על namespace. זה מועיל במצבים שבהם אנשים נוהגים לא להגדיר resource limits בהגדרת ה-POD.

**ש7. איך מעדכנים את גרסת K8s?**
לפני עדכון K8s, חשוב לקרוא את release notes כדי להבין את השינויים שמוצגים בגרסה החדשה ואם העדכון יעדכן גם את etcd.

https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade-1-12/

**ש8. מה ההבדל בין Helm לבין K8s Operator?**
Operator הוא controller ספציפי לאפליקציה שמרחיב את ה-Kubernetes API ליצירה, הגדרה וניהול של אינסטנסים של אפליקציות stateful מורכבות בשם משתמש Kubernetes. הוא בנוי על מושגי resource ו-controller בסיסיים של Kubernetes, אך כולל גם ידע ספציפי לתחום/אפליקציה כדי לאוטומט משימות נפוצות. לעומת זאת, Helm הוא package manager, בדומה ל-yum או apt-get.

**ש9. הסבר את תפקיד ה-CRD (Custom Resource Definition) ב-K8s.**
custom resource הוא הרחבה של ה-Kubernetes API שאינה זמינה בהכרח בהתקנת Kubernetes ברירת מחדל. הוא מייצג התאמה אישית של התקנת Kubernetes מסוימת. למעשה, רבות מהפונקציות המרכזיות של Kubernetes נבנות כיום באמצעות custom resources, מה שעושה את Kubernetes למודולרי יותר.

**ש10. מהם השירותים הקשורים ל-K8s שרצים על ה-nodes, ומה תפקיד כל אחד מהם?**
cluster של K8s מורכב בעיקר משני סוגי nodes: master ו-executor.

- שירותי master:
  - **kube-apiserver**: שירות ה-API הראשי שמשמש כ"דלת" אל cluster ה-K8s.
  - **kube-scheduler**: מתזמן PODs בהתאם למשאבים הזמינים על nodes מסוג executor.
  - **kube-controller-manager**: לולאת בקרה שעוקבת אחר המצב המשותף של ה-cluster דרך ה-apiserver ומבצעת שינויים בניסיון להזיז את המצב הנוכחי לכיוון המצב הרצוי.

- שירותי executor node (אלו רצים גם על master node):
  - **kube-proxy**: ה-network proxy של Kubernetes שרץ על כל node. הוא משקף את ה-services שמוגדרים ב-Kubernetes API ויכול לבצע forwarding בסיסי של TCP, UDP ו-SCTP, או round-robin forwarding על פני קבוצת backends.
  - **kubelet**: לוקח קבוצת PodSpecs שמתקבלים במספר דרכים (בעיקר דרך ה-apiserver) ומבטיח שהקונטיינרים המתוארים בהם רצים ותקינים.

**ש11. מה השיטה המומלצת לניהול גישה למספר clusters?**
`kubectl` מחפש קובץ config שבו ניתן להגדיר מידע גישה למספר clusters. ניתן להשתמש בפקודות `kubectl config` כדי לנהל את הגישה ל-clusters אלו.

**ש12. מהו PDB (Pod Disruption Budget)?**
PDB מגדיר את מספר ה-replicas שאפליקציה יכולה לסבול, יחסית למספר שהיא צריכה להחזיק. לדוגמה, Deployment עם `.spec.replicas: 5` אמור להחזיק 5 pods בכל זמן נתון. אם ה-PDB שלו מאפשר 4 בכל זמן נתון, Eviction API יאפשר שיבוש וולונטרי (voluntary disruption) של pod אחד, אך לא של שניים בו-זמנית. הדבר חל על שיבושים וולונטריים.

**ש13. באילו מצבים משתמשים ב-DaemonSet?**
DaemonSets משמשים להפעלת PODs על כל node ב-cluster. הם משמשים בעיקר להרצת agents לניטור או logging שצריכים לרוץ על כל executor node ב-cluster.

**ש14. מתי מעדיפים StatefulSet?**
כשמריצים אפליקציות שדורשות quorum — אפליקציות שאינן stateless אמיתיות — נדרשים StatefulSets.

**ש15. מהו init container ומתי אפשר להשתמש בו?**
init containers מכינים את הקרקע לפני הרצת ה-POD בפועל.

- המתנה זמן מסוים לפני הפעלת ה-app container, עם פקודה כמו `sleep 60`.
- שכפול (clone) של git repository לתוך volume.

**ש16. מהן אסטרטגיות הפריסה (deployment) של אפליקציות?**
בעולם האג'ילי הזה קיים דרישה מתמדת לעדכן אפליקציות. ישנן מספר אפשרויות לפריסת גרסה חדשה של אפליקציה:

1. **Recreate**: סטייל ישן — הגרסה הקיימת נהרסת והגרסה החדשה נפרסת. downtime משמעותי.
2. **Rolling update**: הורדה הדרגתית של הפריסה הקיימת והכנסת הגרסה החדשה. ניתן לקבוע כמה instances מתעדכנים בכל זמן נתון.
3. **Shadow**: התעבורה שמגיעה לגרסה הקיימת משוכפלת לגרסה החדשה כדי לבדוק שהיא עובדת. Istio מספק pattern זה.
4. **A/B Testing באמצעות Istio**: הרצת מספר וריאנטים של האפליקציה במקביל וקביעת הטוב ביותר על בסיס תעבורת המשתמשים. בעיקר עבור החלטות ניהוליות.
5. **Blue/Green**: בעיקר מעבר תעבורה מגרסה אחת של האפליקציה לגרסה אחרת.
6. **Canary deployment**: אחוז מסוים מהתעבורה מועבר מגרסה אחת לאחרת. אם הדברים פועלים טוב, מגדילים בהדרגה את אחוז התעבורה. שונה מ-rolling update בכך שמספר המופעים של הגרסה הקיימת מצטמצם בהדרגה.

**ש17. איך מאתרים תקלה כש-POD לא מתוזמן (scheduled)?**
גורמים רבים יכולים לגרום ל-POD שלא עולה. הנפוץ ביותר הוא חוסר במשאבים. יש להשתמש בפקודות כמו `kubectl describe <POD> -n <Namespace>` כדי לראות את הסיבה שה-POD לא עולה. כן רצוי לעקוב אחרי `kubectl get events` כדי לראות את כל האירועים שמגיעים מה-cluster.

**ש18. איך מריצים POD על node מסוים?**
ישנן כמה שיטות לכך:

- **nodeName**: לציין את שם ה-node בהגדרת ה-POD; הוא ינסה להריץ את ה-POD על אותו node ספציפי.
- **nodeSelector**: להקצות label ספציפי ל-node עם משאבים מיוחדים ולהשתמש באותו label בהגדרת ה-POD כך שה-POD ירוץ רק על אותו node.
- **node affinities**: `requiredDuringSchedulingIgnoredDuringExecution` ו-`preferredDuringSchedulingIgnoredDuringExecution` הן דרישות hard ו-soft להרצת POD על nodes ספציפיים. אלו יחליפו את nodeSelector בעתיד. זה תלוי ב-labels של ה-node.

**ש19. איך מבטיחים ש-PODs ימוקמו יחד (colocated) לשם שיפור ביצועים?**
`podAntiAffinity` ו-`podAffinity` הם מושגי affinity לשמירה (או אי-שמירה) של PODs על אותו node. הנקודה המרכזית היא שזה תלוי ב-labels של ה-PODs.

**ש20. מהם taints ו-tolerations?**
taints מאפשרים ל-node "לדחות" קבוצת pods. אפשר להגדיר taints על node, ורק PODs עם tolerations שמתאימים לתנאי ה-taint יוכלו לרוץ על אותם nodes. שימושי כשמייעדים node למשתמש מסוים ולא רוצים שיריצו עליו PODs ממשתמשים אחרים.

**ש21. איך מסַפְּקים אחסון פרסיסטנטי (persistent) ל-POD?**
Persistent Volumes משמשים לאחסון פרסיסטנטי של POD. ניתן לפרוס אותם באופן סטטי או דינמי.

- **Static**: מנהל cluster יוצר מספר PVs, הנושאים פרטים על האחסון הפיזי הזמין לשימוש משתמשי ה-cluster.
- **Dynamic**: מנהל יוצר PVC (Persistent Volume Claim) שמציין storage class קיים, וה-volume נוצר דינמית בהתבסס על ה-PVC.

**ש22. איך שני קונטיינרים הרצים ב-POD אחד חולקים כתובת IP יחידה?**
Kubernetes מממש זאת על ידי יצירת קונטיינר מיוחד לכל pod שמטרתו היחידה היא לספק network interface לקונטיינרים האחרים. זהו קונטיינר ה-`pause`, האחראי לשיתוף namespace בתוך ה-POD. אנשים נוהגים להתעלם מקיומו, אך בפועל הוא לב הרשת ושאר הפונקציונליות של ה-POD — הוא מספק interface וירטואלי יחיד שבו משתמשים כל הקונטיינרים שרצים ב-POD.

**ש23. מהן הדרכים השונות לחבר את K8s לעולם החיצוני?**
כברירת מחדל, POD יכול להגיע לעולם החיצוני, אך לכיוון ההפוך יש צורך בעבודה נוספת. אפשרויות:

- NodePort (חושף פורט אחד על כל node לתקשורת איתו)
- Load balancers (שכבת L4 של TCP/IP)
- Ingress (שכבת L7 של TCP/IP)

שיטה נוספת היא `kube-proxy`, שמאפשרת חשיפת service עם cluster IP בלבד על פורט מקומי של המערכת:

```
kubectl proxy --port=8080
http://localhost:8080/api/v1/proxy/namespaces/<NAMESPACE>/services/<SERVICE-NAME>:<PORT-NAME>/
```

https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0

**ש24. מה ההבדל בין NodePort לבין load balancer?**
NodePort מתבסס על כתובת ה-IP של ה-node, וניתן להשתמש רק בטווח פורטים 30000–32767. ל-load balancer יש כתובת IP משלו. כל ספקי הענן הגדולים מאפשרים יצירת LB עבורכם אם מציינים את סוג ה-LB ביצירת ה-service. ב-clusters מבוססי bare-metal, MetalLB הוא אופציה מבטיחה.

**ש25. מתי צריך Ingress במקום load balancer?**
לכל service נדרש LB נפרד. ניתן להשתמש ב-Ingress יחיד עבור מספר services, מה שמאפשר ניתוב מבוסס path וגם מבוסס subdomain לשירותי backend, וניתן לבצע SSL termination ב-Ingress.

**ש26. איך עובדת תקשורת POD-ל-POD?**
לתקשורת POD-ל-POD, מומלץ תמיד להשתמש ב-DNS של ה-service של K8s במקום ב-IP של ה-POD, כי PODs הם אפמריים וה-IP שלהם יכול להשתנות לאחר redeployment.

אם שני PODs רצים על אותו host, ה-interface הפיזי לא נכנס לתמונה:

- חבילה (packet) עוזבת את ה-virtual network interface של POD1 ועוברת ל-docker bridge (`cbr0`).
- ה-docker bridge מעביר את החבילה ל-POD2, שרץ על אותו host.

אם שני PODs רצים על hosts שונים, ה-interfaces הפיזיים של שני המכונות נכנסים לתמונה. נבחן תרחיש שבו CNI לא בשימוש:

```
POD1 = 192.168.2.10/24 (node1, cbr0 192.168.2.1)
POD2 = 192.168.3.10/24 (node2, cbr1 192.168.3.1)
```

- POD1 שולח תעבורה המיועדת ל-POD2 ל-gateway שלו (`cbr0`) כי שניהם בתת-רשתות שונות.
- ה-gateway לא מכיר את הרשת `192.168.3.0/24`, ולכן הוא מעביר את התעבורה ל-interface הפיזי של node1.
- node1 מעביר את התעבורה אל ה-router/gateway הפיזי שלו.
- ל-router/gateway הפיזי הזה צריך להיות route עבור `192.168.3.0/24` כדי לנתב את התעבורה ל-node2.
- כשהתעבורה מגיעה ל-node2, היא מועברת ל-POD2 דרך `cbr1`.

עם Calico CNI, הוא אחראי על הוספת routes עבור ה-cbr (כתובת ה-IP של docker bridge) בכל ה-nodes.

**ש27. איך עובדת תקשורת POD-ל-service?**
מכיוון ש-PODs אפמריים וכתובות ה-IP שלהם יכולות להשתנות, נעשה שימוש ב-service כ-proxy/load balancer לתקשורת אמינה עם PODs. service הוא resource של Kubernetes שמגדיר proxy להעברת בקשות לקבוצת pods. קבוצת ה-pods שתקבל את התעבורה נקבעת על ידי ה-selector, שמתאים labels שהוקצו ל-pods בעת יצירתם. K8s מספק DNS פנימי ל-cluster שמתרגם את שם ה-service.

service משתמש ברשת פנימית שונה מרשת ה-POD — חוקי netfilter שמוזרקים על ידי `kube-proxy` מפנים בקשות שמיועדות ל-IP של ה-service ל-POD הנכון.

**ש28. איך service יודע אילו endpoints תקינים (healthy)?**
ה-`kubelet` שרץ על worker node אחראי לאיתור endpoints לא תקינים. הוא מעביר את המידע הזה ל-API server, שבסופו של דבר מעביר אותו ל-`kube-proxy`, שמתאים את חוקי ה-netfilter בהתאם.

קריאה מומלצת בנושא networking של K8s:

https://medium.com/google-cloud/understanding-kubernetes-networking-pods-7117dd28727

https://medium.com/google-cloud/understanding-kubernetes-networking-services-f0cb48e4cc82

https://medium.com/google-cloud/understanding-kubernetes-networking-ingress-1bc341c84078

**ש29. מהן הפעולות השונות שאפשר לבצע כדי להגביר את אבטחת K8s?**
זה נושא רחב — כמה תרגולים מרכזיים:

- כברירת מחדל, POD יכול לתקשר עם כל POD אחר; יש להגדיר network policies כדי להגביל תקשורת בין PODs.
- RBAC (Role Based Access Control) לצמצום הרשאות.
- שימוש ב-namespaces לקביעת גבולות אבטחה.
- הגדרת admission control policies למניעת הרצת קונטיינרים privileged.
- הפעלת audit logging.

**ש30. איך מבצעים ניטור (monitoring) של cluster ב-K8s?**
Prometheus משמש לניטור K8s. מערכת Prometheus מורכבת ממספר רכיבים:

- שרת Prometheus הראשי, שאחראי על scraping ואחסון time series data.
- ספריות client לשילוב במונה (instrumentation) של קוד האפליקציה.
- push gateway לתמיכה ב-jobs קצרי חיים.
- exporters מיוחדים לשירותים כמו HAProxy, StatsD, Graphite וכו'.
- alertmanager לטיפול בהתראות.
- כלי תמיכה נוספים.

**ש31. איך עושים את Prometheus highly available (HA)?**
אפשר להריץ כמה אינסטנסים של Prometheus עבור HA, אך Grafana יכולה להשתמש רק באחד מהם כ-datasource. אפשר להציב load balancer מול כמה אינסטנסים של Prometheus, להשתמש ב-sticky sessions ו-failover אם אחד האינסטנסים נכשל — זה מסבך את הדברים. Thanos הוא פרויקט נוסף שפותר את האתגרים האלה.

**ש32. מהם אתגרים נוספים עם Prometheus?**
אף ש-Prometheus מצוין לניטור K8s, יש לו עדיין כמה בעיות:

- תמיכת HA.
- אין downsampling זמין למטריקות שנאספו על פני זמן.
- אין תמיכה ב-object storage לשמירת מטריקות לטווח ארוך.

כל האתגרים האלה נפתרים שוב על ידי Thanos.

**ש33. מהו Prometheus Operator?**
המשימה של Prometheus Operator היא להפוך את הרצת Prometheus על Kubernetes לפשוטה ככל האפשר, בעוד שהוא שומר על יכולת קונפיגורציה ועושה את ההגדרה native ל-Kubernetes.

**ש34. איך מקבלים לוגים מרוכזים (centralized) מ-POD?**
הארכיטקטורה הזו תלויה באפליקציה ובגורמים רבים נוספים. תבניות logging נפוצות:

- agent לוגינג בשכבת node
- streaming sidecar container
- sidecar container עם agent לוגינג
- ייצוא לוגים ישירות מהאפליקציה

הגדרה נפוצה מריצה `filebeat` ו-`journalbeat` כ-DaemonSets. הלוגים שנאספים על ידם נשלחים ל-Kafka topic, שמועבר בסופו של דבר ל-ELK stack. אפשר להגיע לתוצאה דומה באמצעות EFK stack ו-Fluent Bit.
