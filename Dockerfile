FROM python:3.10.5-slim

WORKDIR /cicd-budgeting

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 --no-cache-dir install --upgrade awscli

RUN pip3 install --upgrade pip && \
    pip3 install -e .

CMD ["python","-u","src/main.py"]