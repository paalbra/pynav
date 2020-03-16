# About

PyNAV is a very simple python module that interacts with [NAV](https://nav.uninett.no/) and its [API](https://nav.uninett.no/doc/latest/howto/using_the_api.html).

# Install

	$ python3 -m venv venv
	$ . venv/bin/activate
	$ pip install -r requirements.txt

# Usage

	import pynav

	api = pynav.NAVAPI("https://example.com/api", "tokentokentokentokentokentokentokentoken", "example.com.crt")

# Caveats

The API has some bugs. You might encounter very long request times and application crashes in some endpoints with certain parameters. [Bug tracker](https://github.com/UNINETT/nav/issues)
