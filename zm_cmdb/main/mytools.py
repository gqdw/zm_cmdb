import os
import logging
import paramiko
# import socket


def execmd(hostname, username, cmd):
	try:
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.client.WarningPolicy())
		keyfile = '/tmp/id_rsa'
		client.connect(hostname, username=username, key_filename=keyfile, timeout=5)
		stdin, stdout, stderr = client.exec_command(cmd)
	except Exception, e:
		print e
	return stdout.read()


def get_keys(hostname, username='root'):
	cmd = 'cat /root/.ssh/authorized_keys'
	res = execmd('114.55.72.105', 'root', cmd)
	return res.strip().split('\n')


if __name__ == '__main__':
	keys = get_keys('114.55.72.105')
# 	keys = get_keys('121.40.76.26')
	print execmd('114.55.72.105', 'root', 'ls /tmp')
	print keys
