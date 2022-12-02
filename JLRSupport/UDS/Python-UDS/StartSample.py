from doipclient import DoIPClient

print( "----" )
address, announcement = DoIPClient.await_vehicle_announcement()

logical_address = announcement.logical_address
print( ip, port, logical_address )