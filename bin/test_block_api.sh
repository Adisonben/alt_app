#!/bin/bash
iptables -A OUTPUT -m string --algo bm --string "www.smartbusterminalkrss.org" -j DROP
iptables -A OUTPUT -m string --algo bm --string "net3.win" -j DROP
