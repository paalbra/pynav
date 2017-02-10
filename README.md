# About

PyNAV is a very simple python module that interacts with [NAV](https://nav.uninett.no/) and its [API](https://nav.uninett.no/doc/latest/howto/using_the_api.html).

# Install

	$ virtualenv -p python3 venv
	$ source venv/bin/activate
	$ pip install -r requirements.txt

# Usage

	import pynav

	api = pynav.NAVAPI("https://example.com/api", "tokentokentokentokentokentokentokentoken", "example.com.crt")

# Caveats

