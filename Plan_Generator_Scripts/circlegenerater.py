from enum import Flag
from plangenerater import PlanGenerater
import math
import csv
import numpy as np
class CircleGenerater():
    Length_Lon = 20037000 # 经线的长度
    Length_equator = 40075020
    def InitPlanGenerater(self):
        self.plangenerater = PlanGenerater()

    def __init__(self) -> None:
        # self.InitPlanGenerater()
        pass

    def SetCenter(self, Center_Lat, Center_Lon, Center_AltRel):
        ''' description 
        :param Center_Lat:中心点的纬度
        :param Center_Lon:中心点的经度
        :param Center_AltRel:中心点的相对高度
        :return:无
        '''
        self.Center_Lat = Center_Lat
        self.Center_Lon = Center_Lon
        self.Center_AltRel = Center_AltRel
        self.Length_ThisLat = math.cos(2 * math.pi * Center_Lat / 180.0)

    def FromcsvGetPointList(self, csvFileName):    
        ''' description 
        :param csvFileName:从该csv文件中获取航点列表
        :return:返回航点列表
        '''
        csvPointList = []
        with open(csvFileName) as csvfile:
            csv_reader = csv.reader(csvfile)
            firstrow_Flag = True
            for row in csv_reader:
                # print(row)
                # row = row[0].split("\t")
                if  firstrow_Flag:
                    firstrow_Flag = False
                    continue
                # print(row)
                PointElement = {"Lat":float(row[1]), "Lon":float(row[2]), "AltRel":float(row[3]), "Pitch":float(row[4]), "Yaw":float(row[5])}
                csvPointList.append(PointElement)
        # print(csvPointList[1:len(csvPointList)])
        # [1:len(csvPointList)]
        return csvPointList

    def CircleGetPointList(self, Circle_Rad, Circle_Dis, Circle_theta, Circle_Center_Lat, Circle_Center_Lon, Circle_Center_AltRel):
        ''' description 
        :param Circle_Rad:生成球体的半径
        :param Circle_Dis:生成球体的两个航点之间的距离
        :param Circle_theta:生成球体的与中心轴相对的最大角度
        :param Circle_Center_Lat:生成球体的中心点的纬度
        :param Circle_Center_Lon:生成球体的中心点的经度
        :param Circle_Center_AltRel:生成球体的中心点的相对高度
        :return:返回航点列表
        '''
        Length_thisLat = self.Length_equator * math.cos(Circle_Center_Lat * math.pi / 90)
        CirclePointList = [{"Lat": Circle_Center_Lat, "Lon": Circle_Center_Lon, "AltRel": Circle_Center_AltRel + Circle_Rad, "Pitch": 90.0, "Yaw": 90.0}]
        Circle_MaxDisinGround = Circle_Rad * math.cos(Circle_theta * math.pi / 180.0)
        Last_Angle = 2 * math.pi
        for Distance in np.arange( Circle_Dis, Circle_MaxDisinGround, Circle_Dis):
            PointElement = {}
            PointElement["Lat"] = Circle_Center_Lat + Distance * math.cos(Last_Angle) / self.Length_Lon  * 180.0
            PointElement["Lon"] = Circle_Center_Lon + Distance * math.sin(Last_Angle) / Length_thisLat  * 180.0
            PointElement["AltRel"] = Circle_Center_AltRel + math.sqrt(math.pow(Circle_Rad, 2) - math.pow(Distance, 2))
            PointElement["Pitch"] = math.acos(Distance / Circle_Rad) * 180 / math.pi
            PointElement["Yaw"] = 180
            CirclePointList.append(PointElement)

            # Calculate the begin angle
            Begin_Angle = Last_Angle + Circle_Dis / Distance
            while Begin_Angle > - 2 * math.pi:
                Begin_Angle = Begin_Angle - 2 * math.pi

            for Angle in np.arange (Begin_Angle, 2 * math.pi + Circle_Dis / Distance + Begin_Angle, Circle_Dis / Distance):
                PointElement = {}
                PointElement["Lat"] = Circle_Center_Lat + Distance * math.cos(Angle) / self.Length_Lon * 180.0
                PointElement["Lon"] = Circle_Center_Lon + Distance * math.sin(Angle) / Length_thisLat * 180.0
                PointElement["AltRel"] = Circle_Center_AltRel + math.sqrt(math.pow(Circle_Rad, 2) - math.pow(Distance, 2))
                PointElement["Pitch"] = math.acos(Distance / Circle_Rad) * 180 / math.pi
                PointElement["Yaw"] = 180 - (180 - Circle_Dis / Distance * 180 / math.pi) / 2
                CirclePointList.append(PointElement)
                pass
            Last_Angle = Angle
        return CirclePointList    
            

    def RainbowGetPointList(self, Rainbow_Rad, Rainbow_Dis, Rainbow_Begin_Lat, Rainbow_Begin_Lon, Rainbow_Begin_AltRel, Rainbow_Center_Lat, Rainbow_Center_Lon, Rainbow_Center_AltRel):
        ''' description 
        :param Rainbow_Rad:生成弧线的半径
        :param Rainbow_Dis:生成弧线相邻两个点的距离
        :param Rainbow_Begin_Lat:生成弧线的起始点的纬度
        :param Rainbow_Begin_Lon:生成弧线的起始点的经度
        :param Rainbow_Begin_AltRel:生成弧线的起始点的相对高度
        :param Rainbow_Center_Lat:生成弧线的中心点的纬度
        :param Rainbow_Center_Lon:生成弧线的中心点的经度
        :param Rainbow_Center_AltRel:生成弧线的中心点的相对高度
        :return:返回航点列表
        '''
        RainbowPointList = []
        Length_thisLat = self.Length_equator * math.cos(Rainbow_Center_Lat * math.pi / 90)
        # Length in ground
        Rainbow_Lenthground = math.sqrt(math.pow((Rainbow_Begin_Lat - Rainbow_Center_Lat) * self.Length_Lon / 360, 2) + math.pow((Rainbow_Begin_Lon - Rainbow_Center_Lon) * Length_thisLat / 360, 2))
        Rainbow_LengthPoint2Center = Rainbow_Lenthground 
        
        while Rainbow_LengthPoint2Center >= 0 :
            PointElement = {}
            PointElement["Lat"] = (Rainbow_LengthPoint2Center * Rainbow_Begin_Lat + (Rainbow_Lenthground - Rainbow_LengthPoint2Center) * Rainbow_Center_Lat) / Rainbow_Lenthground
            PointElement["Lon"] = (Rainbow_LengthPoint2Center * Rainbow_Begin_Lon + (Rainbow_Lenthground - Rainbow_LengthPoint2Center) * Rainbow_Center_Lon) / Rainbow_Lenthground
            PointElement["AltRel"] = math.sqrt(math.pow(Rainbow_Rad, 2) - math.pow(Rainbow_LengthPoint2Center, 2)) + Rainbow_Center_AltRel
            PointElement["Pitch"] = 180 * math.acos(Rainbow_LengthPoint2Center / Rainbow_Rad) / math.pi
            PointElement["Yaw"] = 0
            RainbowPointList.append(PointElement)
            # print(PointElement)
            Rainbow_LengthPoint2Center = Rainbow_LengthPoint2Center - Rainbow_Dis

        Rainbow_LengthPoint2Center = Rainbow_LengthPoint2Center + Rainbow_Dis

        while Rainbow_LengthPoint2Center <= Rainbow_Lenthground:
            PointElement = {}
            PointElement["Lat"] = (-Rainbow_LengthPoint2Center * Rainbow_Begin_Lat + (Rainbow_Lenthground + Rainbow_LengthPoint2Center) * Rainbow_Center_Lat) / Rainbow_Lenthground
            PointElement["Lon"] = (-Rainbow_LengthPoint2Center * Rainbow_Begin_Lon + (Rainbow_Lenthground + Rainbow_LengthPoint2Center) * Rainbow_Center_Lon) / Rainbow_Lenthground
            PointElement["AltRel"] = math.sqrt(math.pow(Rainbow_Rad, 2) - math.pow(Rainbow_LengthPoint2Center, 2)) + Rainbow_Center_AltRel
            PointElement["Pitch"] = 180 * math.acos(Rainbow_LengthPoint2Center / Rainbow_Rad) / math.pi
            PointElement["Yaw"] = 180
            RainbowPointList.append(PointElement)
            # print(PointElement)
            Rainbow_LengthPoint2Center = Rainbow_LengthPoint2Center + Rainbow_Dis

        return RainbowPointList

    def Run(self, PointList, TargetFile):
        ''' description 
        :param PointList:航点列表
        :param TargetFile:生成的plan文件的名字
        '''
        self.InitPlanGenerater()
        self.plangenerater.ChangeTakeoffPoint(PointList[0]["Lat"], PointList[0]["Lon"], PointList[0]["AltRel"])
        for PointElement in PointList:
            self.plangenerater.AddWaypoint(PointElement["Lat"], PointElement["Lon"], PointElement["AltRel"], Gimbal_Pitch = PointElement["Pitch"], Gimbal_Yaw = PointElement["Yaw"])
            print(PointElement)
        self.plangenerater.AddLandtoTakeoffPointCommand()
        self.plangenerater.GenerateFile(TargetFile)    




if __name__ == "__main__":
    circlegenerater = CircleGenerater()
    # circlegenerater.Run(circlegenerater.RainbowGetPointList(20,1,34.12694001,108.82283213,30,34.12710522,108.82293812,0),"testall.plan")
    # circlegenerater.Run(circlegenerater.FromcsvGetPointList("point.csv"), "plan_generated.plan")
    circlegenerater.Run(circlegenerater.CircleGetPointList(50, 2, 70, 34.12710522, 108.82293812, 0), "testcircle2022y10m22d.plan")