# docker-java-app-distorless

Tiny Java HTTP server. Listens on port **3000**, responds with a
coffee message.

## File

- `src/Main.java` — the app. Uses the built-in JDK
  `com.sun.net.httpserver` (no dependencies).

## Run locally

```sh
javac -d out src/Main.java
java -cp out Main
curl http://localhost:3000/
```

Expected:

```
Here is your coffee ☕
```
