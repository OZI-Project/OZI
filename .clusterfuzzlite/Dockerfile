# Base image with clang toolchain
FROM gcr.io/oss-fuzz-base/base-builder:v1@sha256:394befbfca0f5530bb4591548a47579e0b2ac3f99734c90db3ace4719ba24c7b
# Install required packages to build your project.
RUN pip3 install -r requirements.txt
# Copy source code.
RUN git clone https://github.com/OZI-Project/ozi-core $SRC/ozi-core
# Working directory for build.sh.
WORKDIR $SRC/ozi-core
# Copy build.sh into $SRC dir.
COPY ./.clusterfuzzlite/build.sh $SRC/
