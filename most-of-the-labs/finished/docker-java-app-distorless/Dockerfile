FROM eclipse-temurin:21-jdk-alpine AS build

WORKDIR /app

COPY src/Main.java .

RUN javac -d out Main.java && \
    jar --create --file app.jar --main-class Main -C out .

FROM gcr.io/distroless/java21-debian12:nonroot

WORKDIR /app

COPY --from=build --chown=nonroot:nonroot /app/app.jar /app/app.jar

EXPOSE 3000 

CMD ["app.jar"]

