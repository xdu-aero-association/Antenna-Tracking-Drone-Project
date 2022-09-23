from plangenerater import PlanGenerater
import math
import csv
class CircleGenerater():
    Length_Lon = 20037000 #经线的长度
    Length_equator = 40075020
    def InitPlanGenerater(self):
        self.plangenerater = PlanGenerater()
        

    def __init__(self) -> None:
        #self.InitPlanGenerater()
        pass
    
    def SetCenter(self,Center_Lat,Center_Lon,Center_AltRel):
        self.Center_Lat = Center_Lat
        self.Center_Lon = Center_Lon
        self.Center_AltRel = Center_AltRel
        self.Length_ThisLat = math.cos(2*math.pi*Center_Lat/180.0)

    def FromcsvGetPointList(self,csvFileName):
        csvPointList = []
        with open(csvFileName) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                PointElement = {"Lat":row[0],"Lon":row[1],"AltRel":row[2]}
                csvPointList.append(PointElement)
                
        return csvPointList    
        

    def CircleGetPointList(self,Circle_Rad,Circle_Dis,Circle_theta):
        self.PointList = [{"Lat":self.Center_Lat,"Lon":self.Center_Lon,"AltRel":self.Center_AltRel+Circle_Rad}]

    def RainbowGetPointList(self,Rainbow_Rad,Rainbow_Dis,Rainbow_Begin_Lat,Rainbow_Begin_Lon,Rainbow_Begin_AltRel,Rainbow_Center_Lat,Rainbow_Center_Lon,Rainbow_Center_AltRel):
        RainbowPointList = [{"Lat":Rainbow_Begin_Lat,"Lon":Rainbow_Begin_Lon,"AltRel":Rainbow_Begin_AltRel}]
        Length_thisLat = self.Length_equator*math.cos(Rainbow_Center_Lat*math.pi/90)
        Rainbow_Lenthground = math.sqrt(math.pow((Rainbow_Begin_Lat-Rainbow_Center_Lat)*self.Length_Lon/360,2)+math.pow((Rainbow_Begin_Lon-Rainbow_Center_Lon)*Length_thisLat/360,2)) # length in ground
        Rainbow_LengthPoint2Center = Rainbow_Lenthground - Rainbow_Dis
        
        while Rainbow_LengthPoint2Center >= 0 :
            PointElement = {}
            PointElement["Lat"] = (Rainbow_LengthPoint2Center*Rainbow_Begin_Lat+(Rainbow_Lenthground-Rainbow_LengthPoint2Center)*Rainbow_Center_Lat)/Rainbow_Lenthground
            PointElement["Lon"] = (Rainbow_LengthPoint2Center*Rainbow_Begin_Lon+(Rainbow_Lenthground-Rainbow_LengthPoint2Center)*Rainbow_Center_Lon)/Rainbow_Lenthground
            PointElement["AltRel"] = math.sqrt(math.pow(Rainbow_Rad,2) - math.pow(Rainbow_LengthPoint2Center,2))+Rainbow_Center_AltRel
            RainbowPointList.append(PointElement)
            print(PointElement)
            Rainbow_LengthPoint2Center = Rainbow_LengthPoint2Center - Rainbow_Dis

        Rainbow_LengthPoint2Center = Rainbow_LengthPoint2Center + Rainbow_Dis

        while Rainbow_LengthPoint2Center <= Rainbow_Lenthground :
            PointElement = {}
            PointElement["Lat"] = (-Rainbow_LengthPoint2Center*Rainbow_Begin_Lat+(Rainbow_Lenthground+Rainbow_LengthPoint2Center)*Rainbow_Center_Lat)/Rainbow_Lenthground
            PointElement["Lon"] = (-Rainbow_LengthPoint2Center*Rainbow_Begin_Lon+(Rainbow_Lenthground+Rainbow_LengthPoint2Center)*Rainbow_Center_Lon)/Rainbow_Lenthground
            PointElement["AltRel"] = math.sqrt(math.pow(Rainbow_Rad,2) - math.pow(Rainbow_LengthPoint2Center,2))+Rainbow_Center_AltRel
            RainbowPointList.append(PointElement)
            print(PointElement)
            Rainbow_LengthPoint2Center = Rainbow_LengthPoint2Center + Rainbow_Dis

            
        return RainbowPointList

    def Run(self,PointList,TargetFile):
        self.InitPlanGenerater()
        self.plangenerater.ChangeTakeoffPoint(PointList[0]["Lat"],PointList[0]["Lon"],PointList[0]["AltRel"])
        for PointElement in PointList:
            self.plangenerater.AddWaypoint(PointElement["Lat"],PointElement["Lon"],PointElement["AltRel"])
        self.plangenerater.AddLandtoTakeoffPointCommand()
        self.plangenerater.GenerateFile(TargetFile)    
        



if __name__ == "__main__":
    circlegenerater = CircleGenerater()
    circlegenerater.Run(circlegenerater.RainbowGetPointList(30,1,34.12694001,108.82283213,30,34.12710522,108.82293812,10),"testall.plan")
