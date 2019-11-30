FROM continuumio/miniconda3

WORKDIR /code
COPY ./env.yaml /code

RUN conda update -n base -c defaults conda
RUN conda env create -f env.yaml

COPY . /code

# Pull the environment name out of the environment.yml
RUN echo "source activate headshot-creator" > ~/.bashrc
ENV PATH /opt/conda/envs/headshot-creator/bin:$PATH