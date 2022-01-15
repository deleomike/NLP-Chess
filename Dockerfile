FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu18.04

WORKDIR app

RUN apt-get update
RUN apt-get install python3.8 python3-pip python3-venv python3-dev zlib1g-dev libjpeg-dev -y

RUN python3 -m venv env

RUN . ./env/bin/activate && pip install --upgrade pip

COPY requirements-cuda.txt requirements.txt

RUN . ./env/bin/activate && \
    pip install -r requirements.txt --no-cache-dir

FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu18.04

WORKDIR app

COPY ./src ./src
COPY --from=0 /app/env /app/env

RUN apt-get update && apt-get install python3.8 python3-venv zlib1g-dev libjpeg-dev -y

ENV PATH="/app/env/bin:$PATH"
#CMD ["/app/env/bin/pip3", "list"]
CMD ["jupyter", "lab", "--port=8080", "--ip=0.0.0.0", "--allow-root"]
