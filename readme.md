# Impression Generator

## Setup
You may need to install Python 3:
`brew install python3`

You must then install the `requests` library for Python 3.x: `pip3 install requests`

## Flags
The following command line options are available:

+ `-n <num>` The number of impressions to generate. Required.
+ `-v <videoId>` The video ID to request an overlay or ad replacement for. Required.
+ `-d <deviceId>` Device ID to use. Defaults to a semi-randomised string.
+ `-s <serverURL>` Server URL to use - if the server is running on a port besides 80, include it in the URL.
+ `-t <type>` Overlay or Upcoming. Specify in lower case.
+ `--delay <secs>` Add a delay of <secs> seconds between requests.
+ `--body <json>` Specify a custom JSON string to be sent as the initial request body.

## Operation
A simple run for 5 impressions on video ABCD-1234 can be achieved as follows:
`python3 impression_generator.py -n 5 -v ABCD-1234`

Extra command line flags can be added as required.
