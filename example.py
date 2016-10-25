#!/usr/bin/env python
#coding: utf-8
from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
import argparse
import dateutil.parser
import dateutil.relativedelta
import getpass
import logging
import pynav
import requests
import socket
import sys
import time

def api_it():
    # Ask for the very secret NAV token.
    token = getpass.getpass("Enter NAV Token: ")

    url = "https://nav.uio.no/api/1"
    api = pynav.NAVAPI(url, token, args.cert)

    # Each line in hosts.txt is expected to start with a hostname followed by a space.
    with open("hosts.txt", "r") as f:
        hosts = [s.strip().split(" ", 1) for s in f.readlines()]

    for host in hosts:
        hostname, info = host
        ip = socket.gethostbyname(hostname)
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

def just_do_it():
    # Do not use the API. JUST DO IT (with a sessionid)!
    # This is much faster than using the API.
    
    def tracker_table2list(table):
        l = []
        for tr in table.find("tbody").find_all("tr"):
            tds = tr.find_all("td")
            hostname = tds[0].text.strip()
            ip = tds[1].a.text.strip()
            mac = tds[3].a.text.strip()
            start_time = dateutil.parser.parse(tds[4].text.strip())
            end_time = tds[5].text.strip()
            if end_time == "Still active":
                end_time = dateutil.parser.parse("9999-12-31T23:59:59.999")
            else:
                end_time = dateutil.parser.parse(end_time)
            l.append((hostname, ip, mac, start_time, end_time))
        return l
    
    def get_newest_entry(entries):
        # Expects a list returned from tracker_table2list
        # Returnes the newest entry based on start_time
        return sorted(entries, key=lambda e: e[4], reverse=True)[0]

    if args.cert is None:
        args.cert = True
    
    session_id = getpass.getpass("Session ID: ")
    cookies = dict(nav_sessionid=session_id)

    # Each line in hosts.txt is expected to start with a hostname followed by a space.
    with open("hosts.txt", "r") as f:
        hosts = [s.strip().split(" ", 1) for s in f.readlines()]

    for host in hosts:
        hostname, info = host
        ip = socket.gethostbyname(hostname)
        url = "https://nav.uio.no/machinetracker/ip/?ip_range=%s&days=10000&dns=on" % ip
        res = requests.get(url, cookies=cookies, verify=args.cert, allow_redirects=False)
        if res.status_code != 200:
            raise Exception("FAIL %d %s" % (res.status_code, url))
        content = res.content

        soup = BeautifulSoup(content, "html.parser")
        table = soup.find(id="tracker-table")

        if table is not None:
            l = tracker_table2list(table)
            e = get_newest_entry(l)
            print(ip, hostname, info, "YES-NAV", e[3].isoformat(), e[4].isoformat())
        else:
            print(ip, hostname, info, "NO-NAV", "NO-StartDate", "NO-EndDate")

        # Go slower on the webserver
        time.sleep(0.1)

if __name__ == "__main__":
    log_format = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.WARN)

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cert", help="A CA bundle that will be used to verify the NAV host certificate.")
    args = parser.parse_args()

    api = False

    if api:
        api_it()
    else:
        just_do_it()
