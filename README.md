# Paperless SMTP Server

This is a container that acts as a SMTP server. The attachments of all mails that get sent to this server will be extracted and uploaded to [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) via its API.

## Why would I need that?
Glad you're asking! I own a Scanner that is able to scan to SMB, FTP or Email.
* I don't have any SMB shares available or FTP servers running that can be consumed by paperless - and I don't really want to setup one just for the scanner
* One could configure the scanner to send e-mails to an inbox that is configured for consumption by Paperless. However, I'd prefer to not send any personal documents through a public mail service before being consumed by Paperless.

## So, how does it work?
* You can run this container
* It will start a basic SMTP (email) server
* You can configure your scanner to send mails to this SMTP server
* Any mail that's received will be processed and scanned for attachments. All attachments (i.e. the scanned PDFs) will be uploaded to Paperless

## Setting it up

### Prerequisites
* Generate an API token for your Paperless instance ([see their docs](https://docs.paperless-ngx.com/api/#authorization))
* Have a local server (Raspberry Pi or anything else) that runs Docker and is reachable by your scanner

### Run the container
`docker run -p 8025:8025 -e PAPERLESS_HOST=https://your-paperless.example.com -e PAPERLESS_TOKEN=your-paperless-token ghcr.io/peterkappelt/paperless-smtp-server:main`

### Setup your scanner
* Configure the SMTP server
  * IP: The IP of the device the docker container is running on
  * Port: 8025 by default
  * Authentication: none
* Scan documents to `paperless@example.com` (or any other mail)

### Test it
Scan a document and send it via mail. It'll be uploaded to paperless

## Configuration
You can set the following options by setting their corresponding environment variables

|       Option      |     Default value    |                                               Description                                               |
|:-----------------:|:--------------------:|:-------------------------------------------------------------------------------------------------------:|
|  `PAPERLESS_HOST` | no default, required | Root URL of your Paperless-ngx instance. Include `http(s)://`. Example: `https://paperless.example.com` |
| `PAPERLESS_TOKEN` | no default, required | The API token used for uploading documents to Paperless-ngx                                             |
|  `SMTP_BIND_HOST` | "" (bind to any)     | Bind SMTP server to a specific hostname or IP address                                                   |
|       `SMTP_PORT` | 8025                 | Port SMTP server listens on                                                                             |

## Contribution
Feel free to create a Pull Request if you'd like to add any features.

## Disclaimer

> This script runs an unauthenticated SMTP server. Make sure to only run it within a trusted network and/or take further actions (e.g. firewall rules) that only your trusted devices can connect to it.
