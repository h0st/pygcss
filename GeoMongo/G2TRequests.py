#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests     # simple http requests

#
# Common Geo2Tag requests for working with Geo2Tag services, channels, points, filters
#
class G2TRequests:

	def __init__(self):
		self.url = 'http://localhost:5001'
		self.login = 'debug_user1'
		# self.services_list = new Hash
		self.service_name = 'testservice'
		# self.channel_id = 'NULL'
		#
		self.lat = '0.0'
		self.lon = '0.0'
		self.alt = '0'
		self.bc = False
		#
		# self.points_id = new Hash

	#
	# check service status, will return OK
	def serviceStatus(self):
		print('GeoMongo: Status')
		status = requests.get('http://localhost:5001/instance/status')
		print('GeoMongo status:', status.status_code)

	#
	# login check
	def loginCheck(self, login):
		print('GeoMongo: Login')
		self.login = login
		login_status = requests.get('http://localhost:5001/instance/login/debug?_id='+self.login)
		print(login_status.status_code)

	#
	# Services
	#
	#def createNewService(self):
	#	# curl ­b 'cookiefile.cookie' ­X POST ­d 'name=SERVICE_NAME&ownerId=new_test_ownerId&logSize=10' http://geomongo/instance/service

	def servicesList(self):
		print('GeoMongo: List of services')
		services_list = requests.get('http://localhost:5001/instance/service?number=0&offset=0')
		print(services_list.status_code)
		print('Json: ', services_list.json())

	def getServiceByName(self, name):
		print('GeoMongo: Get service by name')
		self.service_name = name
		service_by_name = requests.get('http://localhost:5001/instance/service/'+self.service_name)
		print(service_by_name.status_code)
		print('Json: ', service_by_name.json())

	def deleteServiceByName(self, service_name):
	#	# ​curl ­b 'cookiefile.cookie' ­X DELETE 'http://geomongo/instance/service/SERVICE_NAME'
		print('GeoMongo: Delete service by name:')
		del_channel = requests.delete('http://localhost:5001/instance/service/'+service_name)
		print(del_channel.status_code)

	#
	# Channels
	#
	#def createNewChannel(self):
		# ​curl ­b 'cookiefile.cookie' ­H "Content­Type: application/json" ­X POST ­d '{"name":"test_name","json":"{1: 2, 2: 4}"}'
		# 'http://geomongo/instance/service/testservice/channel'

	def getChannelById(self, channel_id):
		print('GeoMongo: Get exist channel by ID:')
		get_channel = requests.get('http://localhost:5001/instance/service/testservice/channel/'+channel_id)
		print(get_channel.status_code)
		print('Json data: ', get_channel.json())

	# search by offset and substring
	# channel_by_substr = requests.get('http://localhost:5001/instance/service/testservice/channel?number=2&offset=0&substring=test')
	# print(channel_by_substr.status_code)
	# print('Json data: ', channel_by_substr.json())

	#def editChannel(self):
		# curl ­b 'cookiefile.cookie' ­X PUT ­d 'name=new_test_channel' 'http://geomongo/instance/service/testservice/channel/CHANNEL_ID'

	def deleteChannelById(self, service_name, channel_id):
		# curl ­b 'cookiefile.cookie' ­X DELETE 'http://geomongo/instance/service/testservice/channel/CHANNEL_ID'
		print('GeoMongo: Delete channel by ID:')
		del_channel = requests.delete('http://localhost:5001/instance/service/'++service_name+'/channel/'+channel_id)
		print(del_channel.status_code)

	#
	# Points
	#
	def createNewPoint(self, service_name, lat, lon, alt, json_data, channel_id, bc):   # json {"a":"c"}
		print('GeoMongo: Add point to channel')
		add_point = requests.post('http://localhost:5001/instance/service/testservice/point', data = {"lat":lat,"lon":lon,"alt":alt,"json":json_data,"channel_id":channel_id,"bc":bc})
		print(add_point.status_code)
		# curl ­b 'cookiefile.cookie' ­H "Content­Type: application/json" ­X POST ­d '[{"lat":1.1,"lon":1.1,"alt":1.1,"json":{"a":"b"},"channel_id":"CHANNEL_ID", "bc":true}]' ​
		# 'http://geomongo/instance/service/testservice/point'

	def getPointById(self, point_id):
		get_point_by_id = requests.get('http://localhost:5001/instance/service/testservice/point/'+point_id)
		print(get_point_by_id.status_code)
		print('Json data: ', get_point_by_id.json())

	def editPoint(self, service_name, point_id, new_data):
		# curl ­b 'cookiefile.cookie' ­X PUT ­d 'alt=5' '​http://geomongo/instance/service/testservice/p​oint/POINT_ID​'
		change_point_by_id = requests.put('http://localhost:5001/instance/service/'+service_name+'/point/'+point_id, data = new_data)    # {"alt":3.1}
		print(change_point_by_id.status_code)
		print('Json data: ', change_point_by_id.json())

	def deletePointById(self, service_name, point_id):
		# curl ­b 'cookiefile.cookie' ­X DELETE 'http://geomongo/instance/service/testservice/point/POINT_ID'
		delete_point_by_id = requests.delete('http://localhost:5001/instance/service/'+service_name+'/point/'+point_id)
		print(delete_point_by_id.status_code)
		print('Json data: ', delete_point_by_id.json())

	#
	# Filtration
	#
	def filterTagsByTimeIntervalInChannel(self, service_name, date_from, date_to, channel_id):
		# date_from format: 1970-09-10T01:01:01.000000
		print('GeoMongo: Filter by time interval and channel id:')
		filter_by_time_inverval = requests.get('http://localhost:5001/instance/service/'+service_name+'/point?number=10&date_from=1970-09-10T01:01:01.000000&bc_from=True&date_from=3970-09-10T01:01:01.000000&bc_to=False&channel_ids='+channel_id)
		print(filter_by_time_inverval.status_code)
		print('Json data: ', filter_by_time_inverval.json())


	def filterTagsByAltitude(self, service_name, alt_from, alt_to, channel_id):
		print('GeoMongo: Filter by altitude:')
		filter_by_altitude = requests.get('http://localhost:5001/instance/service/'+service_name+'/point?number=10&altitude_from='+alt_from+'&altitude_to='+alt_to+'&channel_ids='+channel_id)
		print(filter_by_altitude.status_code)
		print('Json data: ', filter_by_altitude.json())


	def filterTagsByAltitude(self, service_name, geometry_type, radius, channel_id):
		# geometry format json: {"type":"Point","coordinates":[0,0]}
		print('GeoMongo: Filter by points by circle with radius:')
		geometry_type = {"type":"Point","coordinates":[0,0]}
		filter_by_radius = requests.get('http://localhost:5001/instance/service/'+service_name+'/point?number=10&geometry='+geometry_type+'&radius='+radius+'&channel_ids='+channel_id)
		print(filter_by_radius.status_code)
		print('Json data: ', filter_by_radius.json())

	def filterTagsByAltitude(self, service_name, geometry_type, channel_id):
		print('GeoMongo: Filter by polygon:')
		geometry_type = {"type":"Polygon","coordinates":[[[0.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[0.0,0.0]]]}
		filter_by_polygon = requests.get('http://localhost:5001/instance/service/'+service_name+'/point?number=10&geometry='+geometry_type+'&channel_ids='+channel_id)
		print(filter_by_polygon.status_code)
		print('Json data: ', filter_by_polygon.json())

g2t_requests = G2TRequests
g2t_requests.serviceStatus
g2t_requests.loginCheck("kirill.yudenok")