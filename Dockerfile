# THIS FILE IS A TEMPLATE, SO PLEASE MODIFY IT

FROM docker.io/headsman/py3.12:1.2

WORKDIR /app

COPY mock_gui /app/mock_gui

COPY Dockerfile /app/

RUN pip install -r /app/mock_gui/requirements.txt

WORKDIR /app/mock_gui

CMD ["python", "main.py"]