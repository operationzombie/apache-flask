#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	:author: Muneeb Ali | http://muneebali.com
	:license: MIT, see LICENSE for more details.
"""

from flask import Flask, make_response, render_template, jsonify, request

import serial, socket

app = Flask(__name__)

from commontools import log

#Setup listen socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 8082              # Arbitrary non-privileged port
conn = None
adr = None

#Setup sending socket
#HOST = '0.0.0.0'    # The remote host
#PORT = 8083           # The same port as used by the server
#sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sender.connect((HOST, PORT))

#-----------------------------------
@app.route('/', methods=['POST', 'GET'])
def index():    
	if request.method == 'POST':
		if request.form['submit'] == 'Setup':
			print('\n')
			print '***************** SETUP ******************'
			print('\n')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			while not conn:
				conn, adr = s.accept()
			#sender.sendall('PING')
			return render_template('index.html')
		if request.form['submit'] == 'Ping':
			print('\n')
			print '***************** PINGING ******************'
			print('\n')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			conn.sendall('PING')
			conn.recv(1024)
			#sender.sendall('PING')
			conn.close()
			return render_template('index.html')
		elif request.form['submit'] == 'Pong':
			print('\n')
			print '***************** WAITING FOR DATA ******************'
			print('\n')
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			while True :
				data = conn.recv(1024)
				if data:
					return data
		elif request.form['submit'] == 'Ping-Pong':
			print('\n')
			print '***************** Ping-Pong ******************'
			print('\n')
			print 'WRITE PING'
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, adr = s.accept()
			conn.sendall('PING')
			data = None
			while data != 'PONG':
				data = conn.recv(1024)
				if data == 'PONG':
					conn.close()
					return data
			print 'PING PONG'
			return render_template('index.html')
	elif request.method == 'GET':
		return render_template('index.html')

#-----------------------------------
@app.errorhandler(500)
def internal_error(error):

	reply = []
	return jsonify(reply)

#-----------------------------------
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

