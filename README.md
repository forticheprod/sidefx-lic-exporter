# sidefx-lic-exporter

Export license usage for SideFX license server to Prometheus.

## Requirements

This project is expected to run in a docker container, so one of the
requirements is a docker engine.

### Binaries

To run this exporter, you need to provide the binaries `hserver` and `sesictrl`.
They are part of the houdini install on Linux, and you can retrieve them from
their respective destination paths after installing houdini :

- `/opt/hfs<version>/bin/hserver`
- `/opt/hfs<version>/houdini/sbin/sesictrl`

The version of houdini (which translates 1:1 with the version of these binaries)
should be above the version of your license server. At the time of writing, the
exporter has been tested with versions 19.5 and 20.

The available docker compose configuration expects these binaries to be
installed in the `./hfs-bin/` directory, but you can change that as you see fit.

### Configuration

You will need to provide a configuration file to the exporter.

The easiest way to get started is to copy the template included in the
`examples` directory to the root of this repo, and modify the
`license_server_hostname` to your sidefx license server hostname :

```bash
cp ./examples/config.yml .
sed -i 's/sidefx-licserv.example.com/<your-server-hostname>/' config.yml
```

## Usage

### Quick start

After completing the requirements, you can simply start the exporter with the
provided docker compose configuration :

```bash
docker compose up
```

Or if you prefer to use vanilla docker :

```bash
docker run \
  -p "9102:9102" \
  -v "./config.yml:/etc/sidefx-lic-exporter/config.yml" \
  -v "./hfs-bin/hserver:/usr/local/bin/hserver" \
  -v "./hfs-bin/sesictrl:/usr/local/bin/sesictrl" \
  ghcr.io/forticheprod/sidefx-lic-exporter:latest
```

The exporter will be available on port `9102`.

### Quick start from source

If you want to run the application from source (e.g. to test changes) :

- Follow the requirements, and make sure you have gnu make installed
- Start the dev environment in docker with the command `make dev`
- Inside the container, start the exporter with the command
  `sidefx-lic-exporter` and any flags you want

```
usage: sidefx-lic-exporter [-h] [--config CONFIG] [-l LOG_LEVEL] [-p PORT]

options:
  -h, --help            show this help message and exit
  --config CONFIG       path to config file
                        Default : /etc/sidefx-lic-exporter/config.yml
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                        Default : INFO
  -p PORT, --port PORT  port to run the exporter on
                        Default : 9102
```
