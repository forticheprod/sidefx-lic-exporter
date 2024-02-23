.PHONY: dev run

dev:
	sudo docker build -t sidefx-lic-exporter-dev -f Dockerfile.dev .
	sudo docker run -it --rm \
		-v $(PWD):/app \
		-v ./config.yml:/etc/sidefx-lic-exporter/config.yml \
		-v ./hfs-bin/hserver:/usr/local/bin/hserver \
		-v ./hfs-bin/sesictrl:/usr/local/bin/sesictrl \
		-p 9102:9102 sidefx-lic-exporter-dev

run:
	sudo docker compose build
	sudo docker compose up

