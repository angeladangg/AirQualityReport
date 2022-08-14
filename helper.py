import json
import urllib.parse
import urllib.request
import math
import time
import calc
import sys

'''this modules contains classes and the necessary tools for Project 3 to funciton'''

class Center(): 
    '''String form center coordinates'''
    
    def __init__(self, location: str):
        '''builds the request url, download the address in dict form from url
            initializes address, latitude, and longtitude'''
        
        self._address = _download_data(_build_request_url(location))[0] #[0] becuase this came in a list
        time.sleep(1) 
        self._lat = float(self._address["lat"])
        self._lon = float(self._address["lon"])

    def get_address(self)->dict:
        '''returns a dictionary of the center address'''
        
        return self._address

    def get_lat(self)->float:
        '''returns latitude of center address'''
        
        return self._lat

    def get_lon(self)->float:
        '''returns longtitude of center address'''
        return self._lon


class CenterFile():
    '''File form center coordinates'''
    
    def __init__(self, file: str):
        '''opens the file and initializes address, latitude, and longtitude'''
        try:
            with open(file, 'r', encoding="utf-8") as file:
                text = file.read()
                self._address  = json.loads(text)[0]

                if not self._address:
                    print("FAILED")
                    print(file)
                    print("FORMAT")
                    sys.exit()
                    
                self._lat = float(self._address["lat"])
                self._lon = float(self._address["lon"])

        except OSError:
            print("FAILED")
            print(file)
            print("MISSING")
            sys.exit()
            
        except json.decoder.JSONDecodeError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()
            
        except KeyError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()
            
        except UnicodeDecodeError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()
    
    def get_address(self)->dict:
        '''returns a dictionary of the center address'''

        return self._address

    def get_lat(self)->float:
        '''returns latitude of center address'''
        
        return self._lat

    def get_lon(self)->float:
        '''returns longtitude of center address'''
        
        return self._lon



class AQI():
    '''Fetches AQI data by reaching out to API'''
    
    def __init__(self):
        '''request for the information from purpleair API and weeds out useless sensors'''
        
        self._data =_download_data_purple_air()
        self._data = self._data["data"]
        
        fitlered_data = []
        for sensor in self._data:
             if sensor[1] != None:
                if sensor[4] <= 3600: 
                    if sensor[25] == 0:
                        if sensor[27] != None and sensor[28] !=None:
                            fitlered_data.append(sensor)
        self._data = fitlered_data
        
    
    def get_aqi_data(self) ->"[[]]":
        '''fetches list of pre-filtered sensor data'''
        return self._data


class AQIFile():
    '''Fetches AQI data based on AQI FILE'''
    
    def __init__(self, file: str):
        '''gets sensor data from a purple air FILE(S) and weeds out useless sensors'''
        try:
            with open(file, 'r',encoding="utf-8") as file:
                text = file.read()
                self._data = json.loads(text)

                if not self._data:
                    print("FAILED")
                    print(file)
                    print("FORMAT")
                    sys.exit()

        
                self._data = self._data["data"] #put ["version"] to test/print it out

            fitlered_data = []
            for sensor in self._data:
                 if sensor[1] != None:
                    if sensor[4] <= 3600: 
                        if sensor[25] == 0:
                            if sensor[27] != None and sensor[28] !=None:
                                fitlered_data.append(sensor)        
            self._data = fitlered_data

        except OSError:
            print("FAILED")
            print(file)
            print("MISSING")
            sys.exit()
            
        except json.decoder.JSONDecodeError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()
            
        except KeyError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()
            
        except UnicodeDecodeError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()

    def get_aqi_data(self)->"[[]]":
        '''fetches list of pre-filtered sensor data'''
        return self._data

    
class Reverse():
    '''this class does reverse geocoding from API'''
    
    def __init__(self, filtered: list["sensors"]):
        '''given lat and lon, return the location url of the cords'''
        
        self._filtered = filtered
        base_url = "https://nominatim.openstreetmap.org/reverse?"
        
        self._data_master = []

        for sensor in self._filtered:
            
            request = [("lat", sensor[27]),("lon", sensor[28]), ('format', 'json')]
            encoded_request = urllib.parse.urlencode(request)

            self._data = _download_data(f'{base_url}{encoded_request}')
            time.sleep(1) 
            self._data_master.append(self._data['display_name'])
                
    
    def get_data(self)-> list:
        '''returns a list of final addresses'''
        
        return self._data_master
    

class ReverseFile():
    '''this class does reverse geocoding from File'''
    
    def __init__(self, files: list):
        ''''''
        try:
            self._data = []
            for file in files:
                with open(file, 'r', encoding="utf-8") as file:
                    text = file.read()

                    if not json.loads(text):
                        print("FAILED")
                        print(file)
                        print("FORMAT")
                        sys.exit()
                        
                    self._data.append(json.loads(text))
                    
            self._address = []
            for address in self._data:
                self._address.append(address["display_name"])
                            
        except OSError:
            print("FAILED")
            print(file)
            print("MISSING")
            sys.exit()
            
        except json.decoder.JSONDecodeError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()
            
        except KeyError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()
            
        except UnicodeDecodeError:
            print("FAILED")
            print(file)
            print("FORMAT")
            sys.exit()

    def get_data(self)->list:
        '''list of final addresses'''
        
        return self._address
    



'''the end of my classes & start of my helper functions'''

def _separate_once(user_input)-> str: 
    '''Returns only the user request. If not valid, end program'''
    
    user_input = user_input.split(" ")
    
    if type(int(user_input[1])) != int or int(user_input[1]) < 0:
        print("exited")
        sys.exit()
       
    return int(user_input[1])



def _download_data(url:str)-> dict:
    '''request for the info from given url, returns text (dict form) in JSON format'''

    try:
        request = urllib.request.Request(url, headers = {"Referer":"https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/angelad6"})
        response = urllib.request.urlopen(request)

        text = response.read().decode(encoding = "utf-8")
        
        data = json.loads(text)
        response.close()
        
        if not data:
            print("FAILED\n{}\nFORMAT".format(str(response.getcode()) + " " + url))
            sys.exit()
            
        return data
    
    except urllib.error.HTTPError as e:
        print("FAILED")
        print(str(e.code), url)
        print("NOT 200")
        sys.exit()

    except IndexError:
        print("FAILED")
        print(str(response.getcode()), url)
        print("FORMAT")
        sys.exit()
    
    except KeyError:
        print("FAILED")
        print(str(response.getcode()), url)
        print("FORMAT")
        sys.exit()
        
    except json.decoder.JSONDecodeError:
        print("FAILED")
        print(str(response.getcode()), url)
        print("FORMAT")
        sys.exit()
    
    except urllib.error.URLError:
        print("FAILED")
        print(url)
        print("NETWORK")
        sys.exit() 


    
        

def _download_data_purple_air()-> dict:
    '''request for the information in the given url returns text info in json fomrat'''
    
    url = "https://www.purpleair.com/data.json"
    
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        text = response.read().decode(encoding = "utf-8")
        data = json.loads(text)
        response.close()

        if not data:
            print("FAILED\n{}\nFORMAT".format(str(response.getcode()) + " " + url))
            sys.exit()
            
        return data

    except urllib.error.HTTPError as e:
        print("FAILED")
        print(str(e.code), url)
        print("NOT 200")
        sys.exit()

    
    except IndexError:
        print("FAILED")
        print(str(response.getcode()), url)
        print("FORMAT")
        sys.exit()
    
    except KeyError:
        print("FAILED")
        print(str(response.getcode()), url)
        print("FORMAT")
        sys.exit()
        
    except json.decoder.JSONDecodeError:
        print("FAILED")
        print(str(response.getcode()), url)
        print("FORMAT")
        sys.exit()
        
    except urllib.error.URLError:
        print("FAILED")
        print(url)
        print("NETWORK")
        sys.exit() 

    
        
def _build_request_url(location:str) -> str: 
    '''takes the search url and searches for the location in Nominatim'''
    
    base_url = "https://nominatim.openstreetmap.org/search?"
    request = [("q", location), ('format', 'json')]
    encoded_request = urllib.parse.urlencode(request)
    
    return f'{base_url}{encoded_request}'


def _extract_desired_info(data: "[[]]", lat:float, lon: float, threshold: int, miles: int, max_num: int)->list:
    '''Filters out unwanted data. Sort by highest concentration and the max result num'''
    
    results = []
    
    #sensor is each individual list in the 2D list called data

    for sensor in data: #sensor is each individual list in the 2D list called data
 
        if calc._distance(lat, lon, sensor[27], sensor[28]) <= miles:
            if calc._convert_to_aqi(sensor[1]) >= threshold:
                results.append(sensor)

    #sorting from highest AQI to lowest:
    results = sorted(results, key = lambda sensor: sensor[1], reverse = True) 

    #if the results we get is smaller than the requested maximum result, return whatever we have:
    final = []
    
    if len(results) >= max_num:
        i = 0
        for result in results:
            if i < max_num:
                final.append(result)
                i += 1
            else:
                break
            
    results = final
            
    return results

def _print_lat_and_lon(lat: float, lon: float)->str:
    '''prints the lat and lon for the results'''
    
    lon_direction = 'E'
    lat_direction = 'N'
    
    if lon < 0:
        lon_direction = 'W'
        lon = abs(lon)

    if lat < 0:
        lat_direction = 'S'
        lat = abs(lat)

        
    return f"{lat}/{lat_direction} {lon}/{lon_direction}"
    
if __name__ == "__main__":
    pass
