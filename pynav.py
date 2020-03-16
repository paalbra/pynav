from pprint import pprint
import logging
import requests

class NAVAPI():
    def __init__(self, url, token, cert):
        if not url.startswith("https://"):
            raise Exception("The URL does not begin with 'https://': %s" % args.url)
        if url[-1] == "/":
            raise Exception("The URL should not have a trailing slash: %s" % args.url)

        self.token = token
        self.url = url
        logging.debug("API URL set to: %s" % self.url)

        if cert is None:
            # Use builtin CAs
            self.verify = True
        else:
            # Use the given CAs
            self.verify = cert

    def __str__(self):
        return "[%s %s]" % (__class__.__name__, self.url)

    def get_mac(self, ip):
        """
        Get all MAC addresses seen with the given IP.
        Returns a dictionary with MAC as keys and the most recent end_time as values.
        """
        macs = {}
        results = self.send_arp_request({"ip": ip})
        if not results:
            raise Exception("The IP returned no results: %s" % ip)
        for result in results:
            mac = result["mac"]
            end_time = result["end_time"]
            if mac not in macs or macs[mac] < end_time:
                macs[mac] = end_time
        return macs

    def send_arp_request(self, params):
        url = "%s/arp/" % self.url 
        json_object = self.send_request(url, params)
        results = json_object["results"]
        while json_object["next"] is not None:
            json_object = self.send_request(json_object["next"])
            next_results = json_object["results"]
            results.extend(next_results)
        return results

    def send_request(self, url, params=None):
        res = requests.get(url, params, headers={"Authorization": "Token %s" % self.token}, verify=self.verify)
        logging.debug("HTTP: %d from %s took %f seconds" % (res.status_code, res.request.url, res.elapsed.total_seconds()))
        if res.status_code != 200:
            raise Exception("Request not OK: %d, %s" % (res.status_code, res.text))
        return res.json()

