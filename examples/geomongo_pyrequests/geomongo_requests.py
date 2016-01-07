#
# Http-requests for GeoMongo Geo2Tag
# Server: http://localhost:5001/instance/
#
import requests     # simple http requests


#
# Tests with requests lib
#
print('GET Request:')
webpage = requests.get('https://api.github.com/events')
print('CODE: ', webpage.status_code)
print('Content-Type: ', webpage.headers['content-type'])
print('Encoding: ', webpage.encoding)
print('Text: ', webpage.text)
print('Json: ', webpage.json())

print('\n')
print('POST Request:')
post = requests.post("http://httpbin.org/post", data = {"key":"value"})
print('Code:', post.status_code)

print('\n')
print('PUT Request:')
put = requests.put("http://httpbin.org/put", data = {"key":"value"})
print('Code:', put.status_code)
#delete = requests.delete("http://httpbin.org/delete")
#get_head = requests.head("http://httpbin.org/get")
#get_options = requests.options("http://httpbin.org/get")

print('\n')
#
# GeoMongo tests
#
status = requests.get('http://localhost:5001/instance/status')
print('GeoMongo status:', status.status_code)

print('\n')
print('GeoMongo tests')
tests = requests.get('http://localhost:5001/instance/tests')
print(tests.status_code)
print('HtmlText: ', tests.text)

print('\n')
print('GeoMongo: Login')
login = requests.get('http://localhost:5001/instance/login/debug?_id=kirill.yudenok')
print(login.status_code)

print('\n')
print('GeoMongo: List of services')
services_list = requests.get('http://localhost:5001/instance/service?number=0&offset=0')
print(services_list.status_code)
print('Json: ', services_list.json())

print('\n')
print('GeoMongo: Get service by name')
service_by_name = requests.get('http://localhost:5001/instance/service/testservice')
print(service_by_name.status_code)
print('Json: ', service_by_name.json())

print('\n')
print('GeoMongo: Get exist channel by ID:')
get_channel = requests.get('http://localhost:5001/instance/service/testservice/channel/568ab02b4387b46cdbe01d6b')
print(get_channel.status_code)
print('Json data: ', get_channel.json())

print('\n')
print('GeoMongo: Get channel by substring with offset')
channel_by_substr = requests.get('http://localhost:5001/instance/service/testservice/channel?number=2&offset=0&substring=test')
print(channel_by_substr.status_code)
print('Json data: ', channel_by_substr.json())

# test point id : a,b: 568ea8974387b46cdbe01e2a, a,c: 568ebff44387b46cdbe01e7e, b,c: 568ec04e4387b46cdbe01e81

print('\n')
print('GeoMongo: Add point to channel')
add_point = requests.post('http://localhost:5001/instance/service/testservice/point', data = {"lat":1.1,"lon":1.0,"alt":1.1,"json":{"a":"c"},"channel_id":"568ab02b4387b46cdbe01d6b","bc":"true"})
print(add_point.status_code)

print('\n')
print('GeoMongo: Get point by ID:')
get_point_by_id = requests.get('http://localhost:5001/instance/service/testservice/point/568ea8974387b46cdbe01e2a')
print(get_point_by_id.status_code)
print('Json data: ', get_point_by_id.json())

print('\n')
print('GeoMongo: Change (a,c) point altitude for id - 568ebff44387b46cdbe01e7e')
change_point_by_id = requests.put('http://localhost:5001/instance/service/testservice/point/568ebff44387b46cdbe01e7e', data = {"alt":3.1})
print(change_point_by_id.status_code)
print('Json data: ', change_point_by_id.json())

print('\n')
print('GeoMongo: View changed point (a,c):')
changed_point = requests.get('http://localhost:5001/instance/service/testservice/point/568ebff44387b46cdbe01e7e')
print(changed_point.status_code)
print('Json data: ', changed_point.json())

print('\n')
print('GeoMongo: Filter points')

print('\n')
print('GeoMongo: Filter by time interval and one channel:')
filter_by_time_inverval = requests.get('http://localhost:5001/instance/service/testservice/point?number=10&date_from=1970-09-10T01:01:01.000000&bc_from=True&date_from=3970-09-10T01:01:01.000000&bc_to=False&channel_ids=568ab02b4387b46cdbe01d6b')
print(filter_by_time_inverval.status_code)
print('Json data: ', filter_by_time_inverval.json())

print('\n')
print('GeoMongo: Filter by altitude:')
filter_by_altitude = requests.get('http://localhost:5001/instance/service/testservice/point?number=10&altitude_from=1&altitude_to=4&channel_ids=568ab02b4387b46cdbe01d6b')
print(filter_by_altitude.status_code)
print('Json data: ', filter_by_altitude.json())

print('\n')
print('GeoMongo: Filter by points by circle with radius:')
filter_by_radius = requests.get('http://localhost:5001/instance/service/testservice/point?number=10&geometry={"type":"Point","coordinates":[0,0]}&radius=3000&channel_ids=568ab02b4387b46cdbe01d6b')
print(filter_by_radius.status_code)
print('Json data: ', filter_by_radius.json())

print('\n')
print('GeoMongo: Filter by polygon:')
filter_by_polygon = requests.get('http://localhost:5001/instance/service/testservice/point?number=10&geometry={"type":"Polygon","coordinates":[[[0.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[0.0,0.0]]]}&channel_ids=568ab02b4387b46cdbe01d6b')
print(filter_by_polygon.status_code)
print('Json data: ', filter_by_polygon.json())