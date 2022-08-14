import math

'''this module contains all the math and calculations needed for Project 3'''

def _distance(lat1: float, lon1: float, lat2: float, lon2: float)-> float:
    '''calculates the distance from one place to another'''
    R = 3958.8
    
    dlat = math.radians(lat1 - lat2)
    dlon = math.radians(lon1 - lon2)
    
    alat = math.radians((lat1 + lat2) / 2)
    
    x = dlon * math.cos(alat)
    distance = math.sqrt(x ** 2 + dlat ** 2) * R

    return distance # in miles

def _convert_to_aqi(pm: float)-> int:
    '''calculates aqi conversion based on each region's ratio and off-setting to 0'''
    aqi = 0

    if 0.0 <= pm < 12.1:
        aqi_val = 0 + (50 / 12) * (pm - 0)
        
    elif 12.1 <= pm < 35.5:
        aqi_val = 51 + (49 /(35.4 - 12.1)) * (pm - 12.1)
    
    elif 35.5 <= pm < 55.5:
        aqi_val = 101 + (49 / (55.4 - 35.5)) * (pm - 35.5)
    
    elif 55.5 <= pm < 150.5:
        aqi_val = 151 + (49 / (150.4 - 55.5)) * (pm - 55.5)

    elif 150.5 <= pm < 250.5:
        aqi_val = 201 + (49 / (250.4 - 150.5)) * (pm - 150.5)
            
    elif 250.5 <= pm < 350.5:
        aqi_val = 301 + (49 / (350.4 - 250.5)) * (pm - 250.5)
    
    elif 350.5 <= pm < 500.5:
        aqi_val = 401 + (49 / (500.4 - 350.5)) * (pm - 350.5)
        
    else:
        aqi_val = 501
        
    return int(aqi_val + 0.5)

if __name__ == "__main__":
    pass
