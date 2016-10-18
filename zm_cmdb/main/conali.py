# coding=utf-8
from models import aliHost
from aliyunsdkcore import client
import json
import ConfigParser
import os
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest


'''
    "TotalCount": 122,
    "PageNumber": 1,
    "RequestId": "16EBA3FD-22EF-4DAE-A948-A6DD8E5785C0",
    "PageSize": 10,
    "Instances": {
        "Instance": [
            {
                "AutoReleaseTime": "",
                "RegionId": "cn-hangzhou",
                "SerialNumber": "3b94d4fb-6c60-4f43-bb8e-48d130f7c5a3",
                "CreationTime": "2016-08-15T08:35Z",
                "ExpiredTime": "2016-10-15T16:00Z",
                "IoOptimized": true,
                "PublicIpAddress": {
                    "IpAddress": [
                        "114.55.226.113"
                    ]
                },
'''


class Host:
	def __init__(self):
		self.RegionId = ''
		self.CreationTime = ''
		self.ExpiredTime = ''
		self.PublicIpAddress = ''
		self.ZoneId = ''
		self.InstanceName = ''
		self.Cpu = None
		self.Memory = None
		self.InnerIpAddress = ''
		self.DeviceAvailable = None

	def __unicode__(self):
		return u'Name: %s\t %s\t %s' % (self.InstanceName, self.PublicIpAddress, self.InnerIpAddress)

	def __repr__(self):
		return 'Name: %s\t %s\t %s' % (self.InstanceName, self.PublicIpAddress, self.InnerIpAddress)


class Aliyun:
	def __init__(self):
		try:
			config = ConfigParser.ConfigParser()
			config.read(os.path.expanduser('~/.aliyun.cfg'))
			accessid = config.get('main', 'id')
			key = config.get('main', 'key')
		except Exception as e:
			print 'cannot read ~/.aliyun.cfg'
			raise
		self.clt = client.AcsClient(accessid, key, 'cn-hangzhou')
		self.totalcount = 0
		self.hosts = []

	def getHostinfo(self):
		count = 0
		pagenum = 1
		while True:
			r = DescribeInstancesRequest.DescribeInstancesRequest()
			r.set_PageSize(100)
			r.set_PageNumber(pagenum)
			r.set_accept_format('json')
			ret = self.clt.do_action(r)
			data = json.loads(ret)
			# print json.dumps(data, indent=4)
			self.totalcount = data['TotalCount']
			for d in data['Instances']['Instance']:
				InstanceName = d.get('InstanceName')
				RegionId = d.get('RegionId')
				CreationTime = d.get('CreationTime')
				ExpiredTime = d.get('ExpiredTime')
				PublicIpAddress = d.get('PublicIpAddress').get('IpAddress')[0]
				InnerIpAddress = d.get('InnerIpAddress').get('IpAddress')[0]
				ZoneId = d.get('ZoneId')
				Cpu = d.get('Cpu')
				Memory = d.get('Memory')
				DeviceAvailable = d.get('DeviceAvailable')
				IoOptimized = d.get('IoOptimized')
				aliHost.objects.create_host(InstanceName, PublicIpAddress, InnerIpAddress, IoOptimized, Cpu, Memory, DeviceAvailable, ZoneId)
				print InstanceName
				# self.hosts.append(h)

			count += 100
			if count > self.totalcount:
				break
			else:
				pagenum += 1


if __name__ == '__main__':
	ali = Aliyun()
	ali.getHostinfo()
	print ali.totalcount
