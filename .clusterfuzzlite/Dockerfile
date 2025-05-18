# Base image with clang toolchain
FROM gcr.io/oss-fuzz-base/base-builder:v1
# Install required packages to build your project.

# Copy source code.
COPY . $SRC/ozi
# Working directory for build.sh.
WORKDIR $SRC/ozi
# Copy build.sh into $SRC dir.
COPY ./.clusterfuzzlite/build.sh $SRC/
