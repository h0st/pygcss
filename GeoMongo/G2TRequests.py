#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports

#
# Common Geo2Tag requests for working with Geo2Tag services, channels, points, filters
#
class G2TRequests(self):

	def __init__(self):
		self.url = 'http://localhost:5001'
		self.user = 'debug_user1'

	#
	# Services
	#
	def createNewService(self):
		# curl ­b 'cookiefile.cookie' ­X POST ­d 'name=SERVICE_NAME&ownerId=new_test_ownerId&logSize=10' http://geomongo/instance/service

	def servicesList(self):
		# curl ­b 'cookiefile.cookie' ­X GET 'http://geomongo/instance/service?number=0&offset=0'

	def getServiceByName(self):
		# curl ­b 'cookiefile.cookie' ­X GET 'http://geomongo/instance/service/SERVICE_NAME'

	def deleteServiceByName(self):
		# ​curl ­b 'cookiefile.cookie' ­X DELETE 'http://geomongo/instance/service/SERVICE_NAME'

	#
	# Channels
	#
	def createNewChannel(self):
		# ​curl ­b 'cookiefile.cookie' ­H "Content­Type: application/json" ­X POST ­d '{"name":"test_name","json":"{1: 2, 2: 4}"}'
		# 'http://geomongo/instance/service/testservice/channel'

	def getChannelById(self):
		# curl ­b 'cookiefile.cookie' ­X GET 'http://geomongo/instance/service/testservice/channel/CHANNEL_ID'

	# search by offset

	def editChannel(self):
		# curl ­b 'cookiefile.cookie' ­X PUT ­d 'name=new_test_channel' 'http://geomongo/instance/service/testservice/channel/CHANNEL_ID'

	def deleteChannelById(self):
		# curl ­b 'cookiefile.cookie' ­X DELETE 'http://geomongo/instance/service/testservice/channel/CHANNEL_ID'

	#
	# Points
	#
	def createNewPoint(self):
		# curl ­b 'cookiefile.cookie' ­H "Content­Type: application/json" ­X POST ­d '[{"lat":1.1,"lon":1.1,"alt":1.1,"json":{"a":"b"},"channel_id":"CHANNEL_ID", "bc":true}]' ​
		# 'http://geomongo/instance/service/testservice/point'

	def getPointById(self):
		# ​curl ­b 'cookiefile.cookie' ­X GET 'http://geomongo/instance/service/testservice/point/POINT_ID'

	def editPoint(self):
		# curl ­b 'cookiefile.cookie' ­X PUT ­d 'alt=5' '​http://geomongo/instance/service/testservice/p​oint/POINT_ID​'

	def deletePoint(self):
		# curl ­b 'cookiefile.cookie' ­X DELETE 'http://geomongo/instance/service/testservice/point/POINT_ID'

	#
	# Filtration
	#

	# TODO