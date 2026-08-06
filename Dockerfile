FROM python:3.12-slim
RUN useradd --create-home --uid 10001 sna
WORKDIR /app
COPY app /app/app
COPY data /app/data
RUN mkdir /data && chown sna:sna /data
USER sna
ENV SNA_DB_PATH=/data/pilot.db PYTHONUNBUFFERED=1
EXPOSE 8080
HEALTHCHECK --interval=20s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')"
CMD ["python","app/server.py","--host","0.0.0.0","--port","8080"]
