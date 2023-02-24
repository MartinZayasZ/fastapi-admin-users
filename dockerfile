FROM python:3.11.2-alpine
RUN apk add --no-cache tzdata gcc libpq-dev libc-dev
ENV TZ=America/Hermosillo
WORKDIR /python-docker
COPY . .
RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "uvicorn", "app.main:app", "--reload", "--host=127.0.0.1", "--port=8000"]
#CMD "python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"