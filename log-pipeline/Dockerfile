FROM apache/airflow:3.0.1-python3.12

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      default-jdk-headless \
      procps \
 && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-1.17.0-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

USER airflow

RUN pip install --no-cache-dir pyspark==3.5.1