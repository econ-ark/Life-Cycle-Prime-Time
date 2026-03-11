# Life-Cycle-Prime-Time Dockerfile
# Single Source of Truth: reproduce/docker/setup.sh
#
# Build:   docker build -t life-cycle-prime-time .
# Run:     docker run -it --rm life-cycle-prime-time
# Jupyter: docker run -it --rm -p 8888:8888 life-cycle-prime-time jupyter lab --ip=0.0.0.0 --no-browser

FROM mcr.microsoft.com/devcontainers/python:3.12

# Metadata
LABEL org.opencontainers.image.title="Life-Cycle-Prime-Time"
LABEL org.opencontainers.image.description="Development environment for Life-Cycle-Prime-Time REMARK"
LABEL org.opencontainers.image.source="https://github.com/econ-ark/Life-Cycle-Prime-Time"

# Environment
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory with correct ownership
RUN mkdir -p /workspace && chown vscode:vscode /workspace
WORKDIR /workspace

# Copy files with correct ownership (including .git for hatch-vcs version detection)
COPY --chown=vscode:vscode . /workspace/

# Set execute permissions on all shell scripts
USER vscode
RUN find /workspace -name "*.sh" -type f -exec chmod +x {} \;

# Run setup (creates architecture-specific venv)
RUN bash /workspace/reproduce/docker/setup.sh

# Set runtime environment
# Note: The actual venv path depends on architecture (e.g., .venv-linux-x86_64 or .venv-linux-aarch64)
ENV PATH="/workspace/.venv-linux-x86_64/bin:/workspace/.venv-linux-aarch64/bin:/home/vscode/.local/bin:$PATH"
ENV PYTHONPATH="/workspace/src"

# Create entrypoint script that activates the venv
RUN echo '#!/bin/bash' > /home/vscode/entrypoint.sh && \
    echo 'set -e' >> /home/vscode/entrypoint.sh && \
    echo '' >> /home/vscode/entrypoint.sh && \
    echo '# Determine architecture-specific venv path' >> /home/vscode/entrypoint.sh && \
    echo 'ARCH=$(uname -m)' >> /home/vscode/entrypoint.sh && \
    echo 'VENV_PATH="/workspace/.venv-linux-$ARCH"' >> /home/vscode/entrypoint.sh && \
    echo '' >> /home/vscode/entrypoint.sh && \
    echo '# Activate venv if it exists' >> /home/vscode/entrypoint.sh && \
    echo 'if [ -f "$VENV_PATH/bin/activate" ]; then' >> /home/vscode/entrypoint.sh && \
    echo '    source "$VENV_PATH/bin/activate"' >> /home/vscode/entrypoint.sh && \
    echo 'fi' >> /home/vscode/entrypoint.sh && \
    echo '' >> /home/vscode/entrypoint.sh && \
    echo '# Execute the command' >> /home/vscode/entrypoint.sh && \
    echo 'exec "$@"' >> /home/vscode/entrypoint.sh && \
    chmod +x /home/vscode/entrypoint.sh

# Expose common ports
EXPOSE 8888 8866

# Use entrypoint to activate venv, then run command
ENTRYPOINT ["/home/vscode/entrypoint.sh"]
CMD ["/bin/bash"]
