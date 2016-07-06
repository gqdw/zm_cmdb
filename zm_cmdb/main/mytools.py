import os
import logging
import paramiko
import re
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
	res = execmd(hostname, username, cmd)
	return res.strip().split('\n')


def get_cpu_info(hostname, username='root'):
	"""
	return cpu nums
	"""
	cmd = 'nproc'
	res = execmd(hostname, username, cmd)
	return res


def get_mem_info(hostname, username='root'):
	"""
	return memory in kB
	"""
	cmd = 'grep MemTotal /proc/meminfo'
	res = execmd(hostname, username, cmd)
	m = re.search(r'(\d+)', res)
	return m.group(0)


def get_disk_info(hostname, username='root'):
	"""
	get disk num form /dev/vdb+ or /dev/xvdb+
	"""
	cmd = 'if [ -e /dev/vda ]; then ls /dev/vd[b-z]|wc -l;else ls /dev/xvd[b-z]|wc -l ;fi;'
	res = execmd(hostname, username, cmd)
	return 1 + int(res)


if __name__ == '__main__':
	print get_keys('114.55.72.105')
	print get_cpu_info('114.55.72.105')
	print get_mem_info('114.55.72.105')
	print get_disk_info('114.55.72.105')
