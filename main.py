import database

#db = database.create_from_static_data()
db = database.create_from_mbta_server()
print db.stops
