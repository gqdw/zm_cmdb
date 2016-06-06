import os
import logging
import paramiko
#import socket

def get_keys(hostname, username='root'):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.client.WarningPolicy())
	keyfile = '/Users/gqdw/Downloads/pkey/id_rsa'
	client.connect(hostname, username=username, key_filename=keyfile)
	cmd1 = 'cat /root/.ssh/authorized_keys'
	# cmd1 = 'cat %s' % os.path.expanduser('~/.ssh/authorized_keys')
	print cmd1
	stdin, stdout, stderr = client.exec_command(cmd1)
	keys = stdout.read().split('\n')
	return keys
	# files = stdout.read().split()

if __name__ == '__main__':
	keys = get_keys('114.55.72.105')
	#keys = get_keys('121.40.76.26')
	print keys

