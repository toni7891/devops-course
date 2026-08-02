FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=3000

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/

RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup --no-create-home --shell /bin/bash appuser

USER appuser

EXPOSE ${PORT}

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
