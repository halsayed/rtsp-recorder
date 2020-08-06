FROM fedora:32

RUN dnf install -y ffmpeg

RUN mkdir /app
WORKDIR /app
#COPY requirements.txt ./
#RUN pip install -r requirements.txt

CMD ["/bin/bash"]