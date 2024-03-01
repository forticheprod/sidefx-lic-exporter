# sidefx-lic-exporter

Export license usage for SideFX license server to Prometheus.

## Requirements

This project is expected to run in a Docker container, so you'll need a Docker
engine.

### Binaries

To run this exporter, you need the `hserver` and `sesictrl` binaries.
They are part of the houdini install on Linux, and can be found here :

- `/opt/hfs<version>/bin/hserver`
- `/opt/hfs<version>/houdini/sbin/sesictrl`

Make sure your Houdini version matches or is newer than your license server
version. Currently, this exporter has been tested with versions 19.5 and 20.

The available Docker compose configuration expects these binaries to be
installed in the `./hfs-bin/` directory, but you can use the directory of your
choice.

### Configuration

You will need to provide a configuration file to the exporter.

To get started, copy the template from the `examples` directory to the root of
this repository, and modify the `license_server_hostname` to match your SideFX
license server:

```bash
cp ./examples/config.yml .
sed -i 's/sidefx-licserv.example.com/<your-server-hostname>/' config.yml
```

## Usage

### Quick start

Once you've met the requirements, start the exporter using Docker compose :

```bash
docker compose up
```

Or, if you prefer vanilla Docker :

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

- Ensure you have the requirements installed and GNU make
- Start the development environment in Docker with `make dev`
- Inside the container, start the exporter with
  `sidefx-lic-exporter` and any desired flags

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
