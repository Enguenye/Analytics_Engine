import firebase_admin
from datetime import datetime
from Data import Data
from User import User
from firebase_admin import credentials
from firebase_admin import firestore
from folium import plugins
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import calendar
import matplotlib.pyplot as plt
import folium
import os
import numpy as np

class Analytics():
    def __init__(self):
        cred = credentials.Certificate('qa-bogota-firebase-adminsdk-ur7ir-ccd9c9c97d.json')
        firebase_admin.initialize_app(cred)

        db = firestore.client()
        docs = db.collection(u'Data').stream()
        docs2 = db.collection(u'Users').stream()
        self.arr = []
        self.arr2 =[]
        for doc in docs:
            arr = str(doc.to_dict())
            arr2 = arr.split(",")
            arr3=arr2
            try:
                timestamp = arr2[0].split("(")[1] + "," + arr2[1] + "," + arr2[2] + "," + arr2[3] + "," + arr2[4] + "," + \
                        arr2[
                            5]
                longitude = float(arr2[7].split(":")[1])
                latitude = float(arr2[8].split(":")[1])
                aq = float(arr2[9].split(":")[1])
                uv = float(arr2[10].split(":")[1].split("}")[0])
                dat = Data(timestamp, longitude, latitude, aq, uv)
                if dat.latitude!=0 and dat.longitude!=0:
                    self.arr.append(dat)
            except Exception:
                pass
        for doc in docs2:
            arr = str(doc.to_dict())
            arr2 = arr.split(",")
            try:
                mail = arr2[2].split(":")[1]
                name = arr2[4].split(":")[1].split("}")[0]
                number = arr2[1].split(":")[1]
                password = arr2[3].split(":")[1]
                points = int(arr2[0].split(":")[1])
                user=User(mail,name,number,password,points)
                self.arr2.append(user)
            except Exception:
                pass
        # Initializing the zones of Bogota
        self.zones=[[],[],[],[],[]]
        self.zones[0].append([4.6666,-74.06])
        self.zones[0].append([4.6592, -74.036])
        self.zones[0].append([4.7684, -74.022])
        self.zones[0].append([4.7632, -74.069])

        self.zones[1].append([4.6592, -74.036])
        self.zones[1].append([4.5042, -74.087])
        self.zones[1].append([4.5260, -74.128])
        self.zones[1].append([4.6666, -74.06])

        self.zones[2].append([4.6666, -74.06])
        self.zones[2].append([4.629, -74.07836])
        self.zones[2].append([4.6427, -74.117])

        self.zones[3].append([4.629, -74.07836])
        self.zones[3].append([4.5260, -74.128])
        self.zones[3].append([4.5724, -74.173])
        self.zones[3].append([4.6427, -74.117])

        self.zones[4].append([4.6666, -74.06])
        self.zones[4].append([4.6427, -74.117])
        self.zones[4].append([4.5724, -74.173])
        self.zones[4].append([4.617, -74.208])
        self.zones[4].append([4.7632, -74.069])
        self.polygons=[]
        for i in range (5):
            self.polygons.append(Polygon(self.zones[i]))

    def averageUVPerDay(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        data6 = []
        data7 = []
        data = {'Monday': data1, 'Tuesday': data2, 'Wednesday': data3, 'Thursday': data4, 'Friday': data5,
                'Saturday': data6, 'Sunday': data7}
        for doc in self.arr:
            my_date = doc.timestamp
            name = calendar.day_name[my_date.weekday()]
            for i in range(7):
                if name == days[i]:
                    data[name].append(doc.uv)
        fig, ax = plt.subplots()
        green_diamond = dict(markerfacecolor='g', marker='D')
        ax.boxplot(data.values(), flierprops=green_diamond)
        ax.set_xticklabels(data.keys())
        ax.set_title("Distribution of UV/Day")
        ax.set_ylabel('UV radiation level')
        plt.show()



    def growthofUV(self):
        months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        data = [[],[],[],[],[],[],[],[],[],[],[],[]]
        for doc in self.arr:
            my_date = doc.timestamp
            month = my_date.month
            for i in range(12):
                if month == i:
                    data[i].append(doc.uv)
        datadef=[]
        for x in data:
            suma=0
            for l in x:
                suma=suma+l
            tam=len(x)
            if tam==0:
                tam=1
            datadef.append(suma/tam)

        fig = plt.figure()
        fig.suptitle('Change of uv radiation during the year', fontsize=20)
        plt.xlabel('Month', fontsize=18)
        plt.ylabel('UV radiation', fontsize=16)
        plt.plot(months,datadef)
        plt.show()

    def growthofAQ(self):
        months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        data = [[],[],[],[],[],[],[],[],[],[],[],[]]
        for doc in self.arr:
            my_date = doc.timestamp
            month = my_date.month
            for i in range(12):
                if month == i:
                    data[i].append(doc.aq)
        datadef=[]
        for x in data:
            suma=0
            for l in x:
                suma=suma+l
            tam=len(x)
            if tam==0:
                tam=1
            datadef.append(suma/tam)
        fig = plt.figure()
        fig.suptitle('Change of air quality during the year', fontsize=20)
        plt.xlabel('Month', fontsize=18)
        plt.ylabel('Methane percentage on the air', fontsize=16)
        plt.plot(months,datadef)
        plt.show()

    def averageAQPerDay(self):
        days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        data6 = []
        data7 = []
        data = {'Monday':data1,'Tuesday':data2,'Wednesday':data3,'Thursday':data4,'Friday':data5,'Saturday':data6,'Sunday':data7}
        for doc in self.arr:
            my_date = doc.timestamp
            name = calendar.day_name[my_date.weekday()]
            for i in range(7):
                if name == days[i]:
                    data[name].append(doc.aq)
        fig, ax = plt.subplots()
        green_diamond = dict(markerfacecolor='g', marker='D')
        ax.boxplot(data.values(),flierprops=green_diamond)
        ax.set_xticklabels(data.keys())
        ax.set_title("Distribution of AQ/Day")
        ax.set_ylabel('Air quality level')
        plt.show()

    def map(self):
        map1 = folium.Map(location=[4.64964, -74.1081], tiles='cartodbpositron', zoom_start=14)
        tooltip = 'Click me!'
        for i in range(len(self.arr)):
            if (self.arr[i].uv < 10):
                folium.Marker(location=[self.arr[i].latitude, self.arr[i].longitude],
                              popup='<b> UV index: <b> \n' + str(
                                  '{0:.2f}'.format(self.arr[i].uv)),
                              icon=folium.Icon(color='blue', icon='flag'), tooltip=tooltip).add_to(map1);
            else:
                folium.Marker(location=[self.arr[i].latitude, self.arr[i].longitude],
                              popup='<b> UV index: <b> \n' + str(
                                  '{0:.2f}'.format(self.arr[i].uv)),
                              icon=folium.Icon(color='red', icon='flag'), tooltip=tooltip).add_to(map1);

        map1.save('Map.html')
        os.system("start Map.html")

    def AqPerZone(self):
        valuesZone=[[],[],[],[],[]]
        namesZones=["North","East","Center","South","West"]
        for x in range (len(self.arr)):
            point = Point(self.arr[x].latitude, self.arr[x].longitude)
            for y in range(len(self.polygons)):
                if self.polygons[y].contains(point):
                    valuesZone[y].append(self.arr[x].aq)
        mean=[0,0,0,0,0]
        for x in range(len(valuesZone)):
            sum=0
            for y in range(len(valuesZone[x])):
                sum+=valuesZone[x][y]
            tam=len(valuesZone[x])
            if len(valuesZone[x])==0:
                tam=1
            mean[x]=sum/tam
        map1 = folium.Map(location=[4.64964, -74.1081], tiles='cartodbpositron', zoom_start=14)
        folium.Polygon(self.zones[0], "The methane percentage of this zone is: " + str(mean[0]) + "%",
                       namesZones[0], fill=True, color='yellow').add_to(map1)
        folium.Polygon(self.zones[1], "The methane percentage of this zone is: " + str(mean[1]) + "%",
                       namesZones[1], fill=True, color='red').add_to(map1)
        folium.Polygon(self.zones[2], "The methane percentage of this zone is: " + str(mean[2]) + "%",
                       namesZones[2], fill=True, color='green').add_to(map1)
        folium.Polygon(self.zones[3], "The methane percentage of this zone is: " + str(mean[3]) + "%",
                       namesZones[3], fill=True, color='blue').add_to(map1)
        folium.Polygon(self.zones[4], "The methane percentage of this zone is: " + str(mean[4]) + "%",
                       namesZones[4], fill=True, color='orange').add_to(map1)
        map1.save('Map6.html')
        os.system("start Map6.html")

    def UvPerZone(self):
        valuesZone=[[],[],[],[],[]]
        namesZones=["North","East","Center","South","West"]
        for x in range (len(self.arr)):
            point = Point(self.arr[x].latitude, self.arr[x].longitude)
            for y in range(len(self.polygons)):
                if self.polygons[y].contains(point):
                    valuesZone[y].append(self.arr[x].uv)
        mean=[0,0,0,0,0]
        for x in range(len(valuesZone)):
            sum=0
            for y in range(len(valuesZone[x])):
                sum+=valuesZone[x][y]
            tam=len(valuesZone[x])
            if len(valuesZone[x])==0:
                tam=1
            mean[x]=sum/tam
        map1 = folium.Map(location=[4.64964, -74.1081], tiles='cartodbpositron', zoom_start=14)
        folium.Polygon(self.zones[0], "The UV radiation of this zone is: " + str(mean[0]),
                       namesZones[0], fill=True, color='yellow').add_to(map1)
        folium.Polygon(self.zones[1], "The UV radiation of this zone is: " + str(mean[1]),
                       namesZones[1], fill=True, color='red').add_to(map1)
        folium.Polygon(self.zones[2], "The UV radiation of this zone is: " + str(mean[2]),
                       namesZones[2], fill=True, color='green').add_to(map1)
        folium.Polygon(self.zones[3], "The UV radiation of this zone is: " + str(mean[3]),
                       namesZones[3], fill=True, color='blue').add_to(map1)
        folium.Polygon(self.zones[4], "The UV radiation of this zone is: " + str(mean[4]),
                       namesZones[4], fill=True, color='orange').add_to(map1)
        map1.save('Map7.html')
        os.system("start Map7.html")

    def UserAvtivityPerZone(self):
        valuesZone=[[],[],[],[],[]]
        namesZones=["North","East","Center","South","West"]
        for x in range (len(self.arr)):
            point = Point(self.arr[x].latitude, self.arr[x].longitude)
            for y in range(len(self.polygons)):
                if self.polygons[y].contains(point):
                    valuesZone[y].append(self.arr[x].uv)
        mean=[0,0,0,0,0]
        suma=0
        for x in range(len(valuesZone)):
            suma+=len(valuesZone[x])
            mean[x]=len(valuesZone[x])
        map1 = folium.Map(location=[4.64964, -74.1081], tiles='cartodbpositron', zoom_start=14)
        mean2=[0,0,0,0,0]
        for x in range(len(valuesZone)):
            mean2[x]=(mean[x]/suma)*100
        folium.Polygon(self.zones[0], "The percentaje of user activity on this zone is: " + str(mean2[0]) + "%", namesZones[0], fill=True,color='yellow').add_to(map1)
        folium.Polygon(self.zones[1], "The percentaje of user activity on this zone is: " + str(mean2[1]) + "%",
                       namesZones[1], fill=True, color='red').add_to(map1)
        folium.Polygon(self.zones[2], "The percentaje of user activity on this zone is: " + str(mean2[2]) + "%",
                       namesZones[2], fill=True, color='green').add_to(map1)
        folium.Polygon(self.zones[3], "The percentaje of user activity on this zone is: " + str(mean2[3]) + "%",
                       namesZones[3], fill=True, color='blue').add_to(map1)
        folium.Polygon(self.zones[4], "The percentaje of user activity on this zone is: " + str(mean2[4]) + "%",
                       namesZones[4], fill=True, color='orange').add_to(map1)
        map1.save('Map7.html')
        os.system("start Map7.html")

    def map2(self):
        map1 = folium.Map(location=[4.64964, -74.1081], tiles='cartodbpositron', zoom_start=14)
        tooltip = 'Click me!'
        for i in range(len(self.arr)):
            if (self.arr[i].aq< 60):
                folium.Marker(location=[self.arr[i].latitude, self.arr[i].longitude],
                              popup='<b>Methane Percentage:<b> \n ' + str(
                                  '{0:.2f}'.format(self.arr[i].aq)) + ' %',
                              icon=folium.Icon(color='blue', icon='flag'), tooltip=tooltip).add_to(map1);
            else:
                folium.Marker(location=[self.arr[i].latitude, self.arr[i].longitude],
                              popup='<b>Methane Percentage:<b> \n ' + str(
                                  '{0:.2f}'.format(self.arr[i].aq)) + ' %',
                              icon=folium.Icon(color='red', icon='flag'), tooltip=tooltip).add_to(map1);

        map1.save('Map2.html')
        os.system("start Map2.html")

    def Methane_concentration_per_hour(self):
        data=[]
        names=[]
        for i in range(24):
            data.append([])
            names.append(str(i)+"-"+str(i+1))
        for x in self.arr:
            data[x.timestamp.hour].append(x.aq)
        fig, ax = plt.subplots()
        green_diamond = dict(markerfacecolor='g', marker='D')
        ax.boxplot(data, flierprops=green_diamond)
        ax.set_xticklabels(names)
        ax.set_title("Distribution of methane in the air")
        ax.set_ylabel('Percentage of methane concentration')
        ax.set_xlabel('Hour of the day')
        fig.set_size_inches(18.5, 10.5, forward=True)
        plt.show()


    def Radiation(self):
        data=[]
        names=[]
        for i in range(24):
            data.append([])
            names.append(str(i)+"-"+str(i+1))
        for x in self.arr:
            data[x.timestamp.hour].append(x.uv)
        fig, ax = plt.subplots()
        green_diamond = dict(markerfacecolor='g', marker='D')
        ax.boxplot(data, flierprops=green_diamond)
        ax.set_xticklabels(names)
        ax.set_title("Distribution of uv radiation around bogota per hour of the day")
        ax.set_ylabel('UV radiation')
        ax.set_xlabel('Hour of the day')
        fig.set_size_inches(18.5, 10.5, forward=True)
        plt.show()

    def UserActivityPerHour(self):
        data=[]
        names=[]
        for i in range(24):
            data.append([])
            names.append(str(i)+"-"+str(i+1))
        for x in self.arr:
            data[x.timestamp.hour].append(x.aq)

        datasize=np.zeros(24)
        suma=0
        for i in range(24):
            datasize[i]=len(data[i])
            suma=suma+len(data[i])
        datadef=np.zeros(24)
        for i in range(24):
            datadef[i]=(datasize[i]*100)/suma
        index=[]
        for i in range(24):
            if datadef[i]==0:
                index.append(i)
        datadef2=np.delete(datadef, index)
        namesdef=np.delete(names, index)
        fig, ax = plt.subplots()
        ax.pie(datadef2, explode=np.zeros(len(datadef2)), labels=namesdef, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title("Percentage of engagement on those hours respect to the total day")
        plt.show()

    def UserActivityPerDayWeek(self):
        data=[[],[],[],[],[],[],[]]
        names=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        for x in range (0,len(self.arr)):
            day=self.arr[x].timestamp.weekday()
            for i in range(7):
                if day == i:
                    data[i].append(self.arr[x].aq)
        datasize=np.zeros(7)
        suma=0
        for i in range(7):
            datasize[i]=len(data[i])
            suma=suma+len(data[i])
        datadef=np.zeros(7)
        for i in range(7):
            datadef[i]=(datasize[i]*100)/suma
        index=[]
        for i in range(7):
            if datadef[i]==0:
                index.append(i)
        datadef2=np.delete(datadef, index)
        namesdef=np.delete(names, index)
        fig, ax = plt.subplots()
        ax.pie(datadef2, explode=np.zeros(len(datadef2)), labels=namesdef, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title("Percentage of engagement on the respective day of the week")
        plt.show()


    def KilometersTraveled(self):
        data = [[],[],[],[],[],[],[],[],[],[],[],[]]
        months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        for x in self.arr:
            data[x.timestamp.month-1].append(x.timestamp)

        datadef=[0,0,0,0,0,0,0,0,0,0,0,0]

        for x in range (0,12):
            datadef[x]=len(data[x])/5
        fig, ax = plt.subplots()
        ax.set_ylabel('Kilometers')
        ax.set_title("Number of kilometers traveled by month")
        ax.bar(months, datadef)
        plt.show()

    def KilometersTraveledbyUser(self):
        data = []
        names=[""]
        for x in self.arr2:
            data.append(x.points/100)
        fig, ax = plt.subplots()
        green_diamond = dict(markerfacecolor='g', marker='D')
        ax.boxplot(data, flierprops=green_diamond)
        ax.set_xticklabels(names)
        ax.set_ylabel('Kilometers')
        ax.set_title("Distribution of kilometers traveled by user")
        plt.show()

    def QuarantineUV(self):
        data = [[],[]]
        names=["Before quarantine", "After quarantine"]
        timestamp1 = "Mar 25 00:00:00 2020"
        quarantineDay = datetime.strptime(timestamp1, "%b %d %H:%M:%S %Y")
        for x in self.arr:
            difference=x.timestamp-quarantineDay
            if (difference.days>0):
                data[0].append(x.uv)
            else:
                data[1].append(x.uv)
        fig, ax = plt.subplots()
        green_diamond = dict(markerfacecolor='g', marker='D')
        ax.boxplot(data, flierprops=green_diamond)
        ax.set_xticklabels(names)
        ax.set_ylabel('UV radiation')
        ax.set_title("Distribution of UV quality before and after quarantine")
        plt.show()

    def QuarantineAQ(self):
        data = [[],[]]
        names=["Before quarantine", "After quarantine"]
        timestamp1 = "Mar 25 00:00:00 2020"
        quarantineDay = datetime.strptime(timestamp1, "%b %d %H:%M:%S %Y")
        for x in self.arr:
            difference=x.timestamp-quarantineDay
            if (difference.days>0):
                data[0].append(x.aq)
            else:
                data[1].append(x.aq)
        fig, ax = plt.subplots()
        green_diamond = dict(markerfacecolor='g', marker='D')
        ax.boxplot(data, flierprops=green_diamond)
        ax.set_xticklabels(names)
        ax.set_ylabel('Methane percentage')
        ax.set_title("Distribution of Methane concentration on the air before and after quarantine")
        plt.show()



    def HeatMap(self):
        map_hooray = folium.Map(location=[4.64964, -74.1081], tiles='stamentoner', zoom_start=14)

        heat_data = np.zeros((len(self.arr), 2))
        for i in range(0, len(self.arr)):
            for j in range(0, 2):
                if j == 0:
                    heat_data[i][j] = self.arr[i].latitude
                else:
                    heat_data[i][j] = self.arr[i].longitude
        map_hooray.add_children(plugins.HeatMap(heat_data, radius=70))
        map_hooray.save('Map5.html')
        os.system("start Map5.html")


    def HeatMapUV(self):
        map_hooray = folium.Map(location=[4.64964, -74.1081], tiles='stamentoner', zoom_start=13.5)

        heat_data=np.zeros((len(self.arr),2))
        for i in range(0,len(self.arr)):
            if self.arr[i].uv>10:
                for j in range(0, 2):
                    if j == 0:
                        heat_data[i][j] = self.arr[i].latitude
                    else:
                        heat_data[i][j] = self.arr[i].longitude
        map_hooray.add_children(plugins.HeatMap(heat_data, radius=70))
        map_hooray.save('Map3.html')
        os.system("start Map3.html")

    def HeatMapAQ(self):
        map_hooray = folium.Map(location=[4.64964, -74.1081], tiles='stamentoner', zoom_start=13.5)

        heat_data=np.zeros((len(self.arr),2))
        for i in range(0,len(self.arr)):
            if self.arr[i].aq>60:
                for j in range(0, 2):
                    if j == 0:
                        heat_data[i][j] = self.arr[i].latitude
                    else:
                        heat_data[i][j] = self.arr[i].longitude
        map_hooray.add_children(plugins.HeatMap(heat_data, radius=70))
        map_hooray.save('Map4.html')
        os.system("start Map4.html")
