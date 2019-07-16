FROM continuumio/miniconda3
ADD app/environment.yml /tmp/environment.yml
COPY . /app
WORKDIR /app
SHELL ["/bin/bash", "-c"]
RUN conda config --add channels conda-forge
RUN conda env create -f /tmp/environment.yml
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH
RUN echo "source activate yelp" > ~/.bashrc
ENV PATH /opt/conda/envs/yelp/bin:$PATH
RUN python -m spacy download en_core_web_sm
ENTRYPOINT ["python", "./app/main.py"]