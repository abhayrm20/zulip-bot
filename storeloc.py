from googlemaps import Client as GoogleMaps


class Storeloc(object):
    def storeloc(self, x):
        try:
            message = " "
            api_key = 'YOUR-API-KEY'
            gmaps = GoogleMaps(api_key)
            geocode_result = gmaps.geocode(x)[0]
            lat = geocode_result["geometry"]["location"]["lat"]
            lng = geocode_result["geometry"]["location"]["lng"]
            store = gmaps.places_nearby(location=(lat, lng), type='store', radius=500)
            for i in range(0, 5):
                message = message + str(store["results"][i]["name"] + "\n")
            return message
        except:
            message = "You have Entered a invalid input please try again!"
            return message
