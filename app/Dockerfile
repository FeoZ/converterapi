FROM python:3.11-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_SERVER_PORT=8080
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app.py"]