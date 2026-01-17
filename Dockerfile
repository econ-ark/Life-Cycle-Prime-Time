# Dockerfile for Life-Cycle-Prime-Time REMARK
# Compatible with repo2docker and Binder
FROM jupyter/base-notebook:python-3.12

# Set working directory
WORKDIR /home/jovyan/work

# Copy environment file
COPY binder/environment.yml /tmp/environment.yml

# Install conda dependencies
RUN conda env update -n base -f /tmp/environment.yml && \
    conda clean -afy && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Copy the entire repository
COPY . /home/jovyan/work

# Install the package in editable mode
RUN pip install --no-cache-dir -e . && \
    fix-permissions "/home/${NB_USER}"

# Set the default command
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
