#!/usr/bin/env python
"""
Receive or send  ESE messages via an AMQ broker.
Created on Mar 2, 2023

@author: fmassin
"""
import time
import stomp
from useractions import respond_heartbeat, respond
from datetime import datetime
from sys import exit
import lxml.etree as ET
from io import BytesIO

def connect_and_subscribe(conn):
    conn.connect(conn.args.user, conn.args.password, wait=True)
    conn.subscribe(destination=conn.args.topic, id=1, ack='auto')
    
class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn
        self.stop = False

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):

        if "<hb " in frame.body and self.conn.args.nohb:
            return
        
        if "<hb " in frame.body:
            respond_heartbeat(frame.body)
            if self.conn.args.hbback:
                self.send_hbback()
        else:
            respond(frame.body)

        print('processed message')

        if not self.conn.args.c:
            conn.disconnect()
            self.stop = True


    def on_disconnected(self):
        print('disconnected')
        if not self.stop:
            connect_and_subscribe(self.conn)
    
    def send_hbback(self):
        dt = datetime.utcnow()
        root = ET.Element('hb')
        root.set('originator', 'munigt')
        root.set('sender', 'munigt')
        now = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        root.set('xmlns', 'http://heartbeat.reakteu.org')
        root.set('timestamp', now)
        tree = ET.ElementTree(root)
        f = BytesIO()
        tree.write(f, encoding="UTF-8", xml_declaration=True, method='xml')
        msg = f.getvalue()
        try:
            self.conn.send(self.conn.args.hbtopic, msg)
        except Exception as e:
            print("ActiveMQ connection lost. Heartbeat was not sent.")
            print(str(e))
            
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help="This can be either 'receiver', 'sender' or 'heartbeat'", type=str)
    parser.add_argument("-u", "--user", help="User name.", type=str)
    parser.add_argument("-p", "--password", help="Password.", type=str)
    parser.add_argument("-H", "--host", help="Server name that is running AMQ broker.", type=str)
    parser.add_argument("-P", "--port", help="STOMP port of AMQ broker.", type=int)
    parser.add_argument("-t", "--topic", help="AMQ topic to send message to.", type=str)
    parser.add_argument("-c", help="Keep listening for messages instead of \
    closing the connection after the first received message.", action='store_true')
    parser.add_argument("-f", "--file", help="input/output file (optional)", type=str)
    parser.add_argument("-i", "--interval", help="interval (s) to send heartbeat (optional)", type=int)
    parser.add_argument("--nohb", help="When in 'receiver' mode ignore heartbeat messages.",
                        action="store_true")
    parser.add_argument("--hbback", help="When a heartbeat is received, then a hb is sent back to activeMQ broker",
                        action="store_true")
    parser.add_argument("--hbtopic", help="The heartbeat back topic. It must be in another topic different than -t option",
                        type=str )
    args = parser.parse_args()
    
    if args.hbback:
        if args.hbtopic == None:
             print("Error: hbtopic must be provided when --hbback is enabled.")
             exit(-1)
        if args.topic == args.hbtopic:
             print("Error: Topic -t and Heartbeat back topic --hbtopic must be different. Exiting....")
             exit(-1)
        
    conn = stomp.Connection([(args.host, args.port)])
    conn.set_listener('', MyListener(conn))
    conn.args = args
    connect_and_subscribe(conn)
    if args.type == 'receiver':
        while 1:
            time.sleep(1)
    conn.disconnect()
