#Angela Dang 80841454
import json
import urllib.parse
import urllib.request
import helper as h
import calc
import sys



def run():
    '''handles inputs and printing of the whole program'''
    
    center = _center_type(input()) #1 input
    miles = h._separate_once(input()) #2 input
    threshold = h._separate_once(input()) #3 input
    max_num = h._separate_once(input()) #4 input
    aqi = _aqi_type(input()) #5 input

    #grabbing data from class and initializing into vairables
    data = aqi.get_aqi_data()
    lat = center.get_lat()
    lon = center.get_lon()

    #filtering
    valid = h._extract_desired_info(data,lat, lon, threshold, miles, max_num)

    reverse = _reverse_type(input(), valid) #6 input
    address = reverse.get_data()

    #print statement
    print()
    _print_lat_and_lon(center.get_address())
    if len(valid) == 0:
        print("No results found based on the requirements...")
        print("Maybe the air quality is too good today")
        print("Try another threshold or range?")

    else:
        for i in range(len(valid)):
            print("AQI", str(calc._convert_to_aqi(valid[i][1])))
            print(h._print_lat_and_lon(valid[i][27],valid[i][28]))
            print(address[i])

    
def _center_type(center: str)-> "Center Class object":
    '''decides if center is nominatim or file, and creates class object accordingly'''

    center = center.split(" ")

    if center[0] != "CENTER":
        sys.exit()
        
    if center[1] == "NOMINATIM":
        c = h.Center(" ".join(center[2:]))
    else: 
        c = h.CenterFile(center[2])
        
    return c


def _aqi_type(aqi: str)-> "class obj":
    '''determines the type of the AQI (5th) input, and creates class object accordingly'''

    aqi = aqi.split()
    
    if aqi[0] != "AQI":
        sys.exit()
        
    if aqi[1] == "PURPLEAIR":
        a = h.AQI()
        
    elif aqi[1] == "FILE":
        a = h.AQIFile("".join(aqi[2:]))
        
    return a


def _reverse_type(reverse: str, valid: "[[]]")-> "class obj":
    '''determines the type of the Reverse (6th) input, and creates class object accordingly'''

    reverse = reverse.split()
    
    if reverse[0] != "REVERSE":
        print("exited")
        sys.exit()

    if reverse[1] == "NOMINATIM":
        r = h.Reverse(valid)
        
    if reverse[1] == "FILES":
        r = h.ReverseFile(reverse[2:])

    return r


        
def _print_lat_and_lon(address: dict)->None:
    '''gets the latitude and longtitude from the address and print coords fo requested CENTER location'''

    lat = float(address['lat'])
    lon = float(address['lon'])
    lon_direction = 'E'
    lat_direction = 'N'
    
    if lon < 0:
        lon_direction = 'W'
        lon = abs(lon)

    if lat < 0:
        lat_direction = 'S'
        lat = abs(lat)

    print(f"CENTER {lat}/{lat_direction} {lon}/{lon_direction}")
    

    
if __name__ == "__main__":
    run()
    

