FROM python:3.10

WORKDIR /app

COPY ./ /app

RUN pip install build
RUN python -m build
RUN pip install dist/*.whl

ENTRYPOINT ["sidefx-lic-exporter"]
CMD ["--config", "/etc/sidefx-lic-exporter/config.yml"]
