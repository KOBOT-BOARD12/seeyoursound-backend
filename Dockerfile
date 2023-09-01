FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y

# install python 3.11.1
RUN apt-get install -y python3.11 python3.11-distutils
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN apt install -y python3-pip

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
