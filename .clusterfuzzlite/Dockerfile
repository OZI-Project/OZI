FROM gcr.io/oss-fuzz-base/base-builder:v1@sha256:f129d5ca21204a13bc3bfb5d564ea4dc1900a70ab1fbe2c6933ff49f82d5df8a
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
