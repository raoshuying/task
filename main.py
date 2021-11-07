import requests
import pprint


class RoomInfoHandle:

    def __init__(self, room_details: dict):
        self.data = room_details

    def get_property_name(self):
        return self.data["pdp_listing_detail"]["p3_summary_title"]

    def get_property_type(self):
        return self.data["pdp_listing_detail"]["room_and_property_type"]

    def get_number_of_bedroom(self):
        bedroom_info = self.data["pdp_listing_detail"]["bedroom_label"]
        number_of_bedrooms = bedroom_info.split(" ")[0]
        return number_of_bedrooms

    def get_number_of_bathroom(self):
        bathroom_info = self.data["pdp_listing_detail"]["bathroom_label"]
        number_of_bathrooms = bathroom_info.split(" ")[0]
        return number_of_bathrooms

    def get_list_of_amenities(self):
        return [info['name'] for info in self.data["pdp_listing_detail"]["listing_amenities"] if
                info['is_present'] == True]


class AirbnbQuery:

    def __init__(self):
        self.api_url = "https://api.airbnb.com/v2"
        headers = {'accept': 'application/json',
                   'accept-encoding': 'br, gzip, deflate',
                   'content-type': 'application/json',
                   'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
                   'user-agent': 'Airbnb/21.44 AppVersion/21.44 iPhone/13 Type/Phone',
                   'x-airbnb-screensize': 'w=375.00;h=812.00',
                   'x-airbnb-carrier-name': 'T-Mobile',
                   'x-airbnb-network-type': 'wifi', 'x-airbnb-currency': 'GDP',
                   'x-airbnb-locale': 'en', 'x-airbnb-carrier-country': 'us',
                   'accept-language': 'en-us',
                   'airbnb-device-id': '9120210f8fb1ae837affff54a0a2f64da821d227',
                   'x-airbnb-advertising-id': 'C326397B-3A38-474B-973B-F022E6E4E6CC'}
        self.sess = requests.Session()
        self.sess.headers = headers

    def get_room_details(self, room_id: str):
        params = {
            'adults': '0',
            '_format': 'for_native',
            'infants': '0',
            'children': '0'
        }
        detail_uri = '/pdp_listing_details/'
        query_url = self.api_url + detail_uri + str(room_id)
        res = self.sess.get(query_url, params=params)
        if res.status_code != 200:
            # No data returned for this room ID
            return None
        # Handle bad request
        return res.json()

    def get_json_file(self, room_id):
        print(self.get_room_details(room_id))

    def get_all_rooms_details(self, ids: list):
        details = {}
        for room_id in ids:
            room_data = self.get_room_details(room_id)
            if room_data:
                handle = RoomInfoHandle(room_data)
                details[room_id] = {
                    "property_name": handle.get_property_name(),
                    "property_type": handle.get_property_type(),
                    "number_of_bedroom": handle.get_number_of_bedroom(),
                    "number_of_bathroom": handle.get_number_of_bathroom(),
                    "list_of_amenities": handle.get_list_of_amenities(),
                }
            else:
                details[room_id] = f"Cannot find detailed information for room {room_id}"
        return details


if __name__ == '__main__':
    airbnb_query = AirbnbQuery()
    all_data = airbnb_query.get_all_rooms_details([50633275])
    print(all_data)
    query = AirbnbQuery()
    all_results = query.get_all_rooms_details([33571268, 33090114, 50633275])
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(all_results)

