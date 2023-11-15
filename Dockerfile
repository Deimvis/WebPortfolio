FROM python:3.11.2

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY /main.py /main.py
COPY /db.py /db.py
COPY /models.py /models.py

ENTRYPOINT [ "uvicorn", "main:app" ]
