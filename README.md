# About

PyNAV is a very simple python module that interacts with the [NAV API](https://nav.uio.no/doc/howto/using_the_api.html).

# Install

	$ virtualenv -p python3 venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt

# Usage

	import pynav

	api = pynav.NAVAPI("https://nav.uio.no/api", "tokentokentokentokentokentokentokentoken", "nav.uio.no.crt")

# Caveats

## nav.uio.no

The current (2016-10-12) certificate, expiring on april 24. 2019, at nav.uio.no does not contain the full certificate chain. If you do not have all the needed CAs you'll need to provide your own certificate for verification.

Given specific arguments some API endpoints are very slow (> 60sec). This is might be due to issues in the application or database layers. You should make sure you do not DOS the service.

