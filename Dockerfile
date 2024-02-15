FROM python:3.10

WORKDIR /app

COPY setup.py .
COPY src ./src
COPY README.md .

RUN python3 setup.py bdist_wheel
RUN pip3 install dist/*.whl

VOLUME /etc/sidefx-lic-exporter

ENTRYPOINT ["sidefx-lic-exporter"]
CMD ["--config", "/etc/sidefx-lic-exporter/config.yml"]
