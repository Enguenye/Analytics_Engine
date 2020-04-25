
import datetime

class Data():
    def __init__(self, timestamp, longitude, latitude, aq, uv):
        arr=timestamp.split(",")
        self.timestamp = datetime.datetime(int(arr[0]),int(arr[1]),int(arr[2]),int(arr[3]),int(arr[4]),int(arr[5]))
        self.longitude = longitude
        self.latitude = latitude
        self.aq = aq
        self.uv = uv
