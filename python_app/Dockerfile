FROM python:3
LABEL project-name="python_app"

WORKDIR /usr/src/app

COPY requirements.pip ./
RUN pip install --no-cache-dir -r requirements.pip

COPY . .

CMD [ "python", "./main.py" ]

