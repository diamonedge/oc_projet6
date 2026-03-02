FROM python:3
LABEL project-name="python_app"

WORKDIR /usr/src/app

COPY requirements.pip ./
RUN pip install --no-cache-dir -r requirements.pip

COPY build_params.sh ./
RUN /bin/bash build_params.sh
COPY . .

CMD [ "python", "./main.py" ]

