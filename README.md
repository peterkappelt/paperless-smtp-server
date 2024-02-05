# Paperless SMTP Server

This is a container that acts as a SMTP server. The attachments of all mails that get sent to this server will be extracted and uploaded to [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) via its API.

## Why would I need that?

Glad you're asking! I own a Scanner that is able to scan to SMB, FTP or Email.

- I don't have any SMB shares available or FTP servers running that can be consumed by paperless - and I don't really want to setup one just for the scanner
- One could configure the scanner to send e-mails to an inbox that is configured for consumption by Paperless. However, I'd prefer to not send any personal documents through a public mail service before being consumed by Paperless.

## So, how does it work?

- Run this container, it will start a basic SMTP (email) server
- You can configure your scanner to send mails to this SMTP server
- Any mail that's received will be processed and scanned for attachments. All attachments (i.e. the scanned PDFs) will be uploaded to Paperless

## Setting it up

### Prerequisites

- Generate an API token for your Paperless instance ([see their docs](https://docs.paperless-ngx.com/api/#authorization))
- Have a local server (Raspberry Pi or anything else) that runs Docker and is reachable by your scanner

### Create the configuration

Use `config.ini.example` as a starting point to create a new file `config.ini` in your working directory. Enter the address of your Paperless instance and an API token that has permission to upload documents.

### Run the container

`docker run -p 8025:8025 -v ./config.ini:/app/config.ini ghcr.io/peterkappelt/paperless-smtp-server:latest`

### Setup your scanner

- Configure the SMTP server
  - IP: The IP of the device the docker container is running on
  - Port: 8025 by default
  - Authentication: none
- Scan documents with the recipient being one of the accounts configured, e.g. `paperless1@example.com`

### Test it

Scan a document and send it via mail. It'll be uploaded to paperless

### Configuration

The application is configured via an ini-style configuration file.

|                                Section                                |      Option      |    Default value     |                                               Description                                               |
| :-------------------------------------------------------------------: | :--------------: | :------------------: | :-----------------------------------------------------------------------------------------------------: |
|                   `[server]` <br/> (server config)                    |    `BindHost`    |   "" (bind to any)   |                          Bind SMTP server to a specific hostname or IP address                          |
|                                                                       |      `Port`      |         8025         |                                       Port SMTP server listens on                                       |
| `[some-email@sample.com]` <br/> (per-account config, can be repeated) | `PaperlessHost`  | no default, required | Root URL of your Paperless-ngx instance. Include `http(s)://`. Example: `https://paperless.example.com` |
|                                                                       | `PaperlessToken` | no default, required |                       The API token used for uploading documents to Paperless-ngx                       |

By default, the app tries to load the config from `/app/config.ini`. This path can be changed by setting the environment variable `CONFFILE` to a different path.

## Contribution

Feel free to create a Pull Request if you'd like to add any features.

## Disclaimer

> This script runs an unauthenticated SMTP server. Make sure to only run it within a trusted network and/or take further actions (e.g. firewall rules) that only your trusted devices can connect to it.
