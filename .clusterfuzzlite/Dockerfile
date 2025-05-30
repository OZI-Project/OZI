# Base image with clang toolchain
FROM gcr.io/oss-fuzz-base/base-builder:v1
# Install required packages to build your project.
RUN pip3 install hypothesis atheris tox pyinstaller pytest
# Copy source code.
RUN git clone https://github.com/OZI-Project/ozi-core $SRC/ozi-core
# Working directory for build.sh.
WORKDIR $SRC/ozi-core
# Copy build.sh into $SRC dir.
COPY ./.clusterfuzzlite/build.sh $SRC/
