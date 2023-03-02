#!/usr/bin/env python
"""
implement user actions in response to ESE messages.
Created on Mar 2, 2023

@author: fmassin
"""
import time
import stomp

def respond(body):
    print('received an message "%s"' % body)

def respond_heartbeat(body):
    print('received an heartbeat "%s"' % body)
