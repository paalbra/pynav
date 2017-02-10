#!/usr/bin/env python
#coding: utf-8
from datetime import datetime
from pprint import pprint
import argparse
import dateutil.relativedelta
import getpass
import logging
import pynav
import socket

if __name__ == "__main__":
    log_format = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cert", help="A CA bundle that will be used to verify the NAV host certificate.")
    args = parser.parse_args()

    # Ask for the very secret NAV token.
    token = getpass.getpass("Enter NAV Token: ")

    url = "https://example.com/api/1"
    api = pynav.NAVAPI(url, token, args.cert)

    # Each line in hosts.txt is expected to start with a hostname followed by a space.
    with open("hosts.txt", "r") as f:
        hosts = [s.strip().split(" ", 1) for s in f.readlines()]

    for host in hosts:
        hostname, info = host
        try:
            ip = socket.gethostbyname(hostname)
        except:
            print("NODNS", hostname)
            continue
        date_limit = (datetime.now() - dateutil.relativedelta.relativedelta(years=1)).isoformat()
        try:
            results = api.send_arp_request({"ip": ip})
        except Exception as e:
            print("ERR", ip, info, e)
            continue
        if len(results) == 0:
            print("ARP-nay-inactive", ip, info)
        else:
            newest_record = sorted(results, key=lambda result: result["end_time"], reverse=True)[0]
            if newest_record["end_time"] == "9999-12-31T23:59:59.999":
                print("ARP-yay-active", ip, info, newest_record["start_time"], newest_record["end_time"], newest_record["mac"])
            elif newest_record["end_time"]:
                print("ARP-yay-inactive", ip, info, newest_record["start_time"], newest_record["end_time"], newest_record["mac"])
