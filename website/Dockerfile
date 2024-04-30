FROM python:3.11.2
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
RUN apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    apt-get clean
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/'        /etc/locale.gen \
    && sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen
RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN locale-gen en_US.UTF-8
RUN pip3 install -r requirements.txt
