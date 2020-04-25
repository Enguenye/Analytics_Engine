import firebase_admin
from Data import Data
from firebase_admin import credentials
from firebase_admin import firestore
import calendar
import matplotlib.pyplot as plt
import folium
import os

class Analytics():
    def __init__(self):
        cred = credentials.Certificate('qa-bogota-firebase-adminsdk-ur7ir-ccd9c9c97d.json')
        firebase_admin.initialize_app(cred)

        db = firestore.client()
        docs = db.collection(u'Data').stream()
        self.arr = []
        for doc in docs:
            arr = str(doc.to_dict())
            arr2 = arr.split(",")
            timestamp = arr2[0].split("(")[1] + "," + arr2[1] + "," + arr2[2] + "," + arr2[3] + "," + arr2[4] + "," + \
                        arr2[
                            5]
            longitude = float(arr2[7].split(":")[1])
            latitude = float(arr2[8].split(":")[1])
            aq = float(arr2[9].split(":")[1])
            uv = float(arr2[10].split(":")[1].split("}")[0])
            dat = Data(timestamp, longitude, latitude, aq, uv)
            self.arr.append(dat)

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
        ax.set_title("Average UV/Day")
        ax.set_ylabel('UV radiation level')
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
        ax.set_title("Average AQ/Day")
        ax.set_ylabel('Air quality level')
        plt.show()

    def map(self):
        map1 = folium.Map(location=[4.64964, -74.1081], tiles='cartodbpositron', zoom_start=16)
        tooltip = 'Click me!'
        for i in range(len(self.arr)):
            if (self.arr[i].uv < 10):
                folium.Marker(location=[self.arr[i].latitude, self.arr[i].longitude],
                              popup='<b> UV index: <b> \n' + str(
                                  '{0:.2f}'.format(self.arr[i].uv)) + '\n' + '<b>Methane Percentage:<b> \n ' + str(
                                  '{0:.2f}'.format(self.arr[i].aq)) + ' %',
                              icon=folium.Icon(color='blue', icon='flag'), tooltip=tooltip).add_to(map1);
            else:
                folium.Marker(location=[self.arr[i].latitude, self.arr[i].longitude],
                              popup='<b> UV index: <b> \n' + str(
                                  '{0:.2f}'.format(self.arr[i].uv)) + '\n' + '<b>Methane Percentage:<b> \n ' + str(
                                  '{0:.2f}'.format(self.arr[i].aq)) + ' %',
                              icon=folium.Icon(color='red', icon='flag'), tooltip=tooltip).add_to(map1);

        map1.save('Map.html')
        os.system("start Map.html")

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
        ax.set_title("Average concentration of methane in the air")
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
        ax.set_title("Average uv radiation around bogota per hour of the day")
        ax.set_ylabel('UV radiation')
        ax.set_xlabel('Hour of the day')
        fig.set_size_inches(18.5, 10.5, forward=True)
        plt.show()
