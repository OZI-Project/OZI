FROM gcr.io/oss-fuzz-base/base-builder:v1@sha256:a651f096640e8132687793856658f6e8592e6a44e736e25b188f345778636d85
COPY ./.clusterfuzzlite/requirements.txt $SRC
RUN echo 'deb http://security.ubuntu.com/ubuntu jammy-security main' > /etc/apt/sources.list
RUN echo 'deb http://us.archive.ubuntu.com/ubuntu jammy main restricted' > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install libc6 -y
RUN apt-get install gettext -y
RUN pip3 install --require-hashes -r $SRC/requirements.txt
RUN git clone https://github.com/OZI-Project/ozi-core $SRC/ozi-core
WORKDIR $SRC/ozi-core
COPY ./.clusterfuzzlite/build.sh $SRC/
