from email.mime import base
import json
json.encoder.FLOAT_REPR = lambda x: format(x, '.11f')
'''
with open("testwaypoint.plan","r",encoding = "utf-8") as f:
    word = f.read()
    
    #print(word)
    word_load = json.loads(word)
    print(word_load)
    
    advise = []
    s = word.split("\n")
    for single in s:
        if len(single.split("：")) == 2:
            advise.append(single.split("：")[1])



    givetimes = Give_Times(*advise)
    times = givetimes.run()
'''
class PlanGenerater:
    BaseFile = {
        "fileType": "Plan",
        "geoFence": {
            "circles": [

            ],
            "polygons": [

            ],
            "version": 2
        },
        "groundStation": "QGroundControl",
        "mission":{
            "cruiseSpeed": 15,
            "firmwareType": 12,
            "globalPlanAltitudeMode": 1,
            "hoverSpeed": 5,
            "items":[{
                "AMSLAltAboveTerrain": None,
                "Altitude": 50,
                "AltitudeMode": 1,
                "autoContinue": True,
                "command": 22,
                "doJumpId": 1,
                "frame": 3,
                "params": [
                    0,
                    0,
                    0,
                    None,
                    34.12739242,
                    108.83128143,
                    50
                ],
                "type": "SimpleItem"
            }
            ],
            "plannedHomePosition": [
                34.12739242,
                108.83128143,
                421.61314800000787
            ],
            "vehicleType": 2,
            "version": 2
        },
        "rallyPoints": {
            "points": [

            ],
            "version": 2
        },
        "version": 1
    }
    BaseItem = {
        "AMSLAltAboveTerrain": None,
        "Altitude": 50,
        "AltitudeMode": 1,
        "autoContinue": True,
        "command": 22,    # 操作ID
        "doJumpId": 1,    # 顺序
        "frame": 3,
        "params": [
            0,
            0,
            0,
            None,
            34.12739242,
            108.83128143,
            50
        ],
        "type": "SimpleItem"
    }
    def __init__(self) -> None:
        pass
    def GetItemNum(self):
        return len(self.BaseFile["mission"]["items"])
    def AddCommandItem(self,CommandID,param):
        pass
    def ChangeTakeoffPoint(self, Takeoffpoint_Lat, Takeoffpoint_Lon, Takeoffpoint_AltRel):
        self.Takeoffpoint_Lat = Takeoffpoint_Lat
        self.Takeoffpoint_Lon = Takeoffpoint_Lon
        self.Takeoffpoint_AltRel = Takeoffpoint_AltRel
        self.BaseFile["mission"]["items"][0]["Altitude"] = Takeoffpoint_AltRel
        self.BaseFile["mission"]["items"][0]["params"][4] = Takeoffpoint_Lat
        self.BaseFile["mission"]["items"][0]["params"][5] = Takeoffpoint_Lon
        self.BaseFile["mission"]["items"][0]["params"][6] = Takeoffpoint_AltRel
        self.BaseFile["mission"]["plannedHomePosition"][0] = Takeoffpoint_Lat
        self.BaseFile["mission"]["plannedHomePosition"][1] = Takeoffpoint_Lon
        self.BaseFile["mission"]["plannedHomePosition"][2] = Takeoffpoint_AltRel
    def AddSpeedCommand(self,Speed):
        SpeedCommand = {
            "autoContinue": True,
            "command": 178,
            "doJumpId": self.GetItemNum()+1,
            "frame": 2,
            "params": [
                1,
                Speed,
                -1,
                0,
                0,
                0,
                0
            ],
            "type": "SimpleItem"
        }
        self.BaseFile["mission"]["items"].append(SpeedCommand)
    
    def AddGimbalCommand(self,Pitch,Yaw):
        GimbalCommand = {
            "autoContinue": True,
            "command": 205,
            "doJumpId": self.GetItemNum()+1,
            "frame": 2,
            "params": [
                -Pitch,
                0,
                Yaw,
                0,
                0,
                0,
                2
            ],
            "type": "SimpleItem"
        }
        self.BaseFile["mission"]["items"].append(GimbalCommand)

    def AddWaypoint(self, Waypoint_Lat, Waypoint_Lon, Waypoint_AltRel, Waypoint_Speed = 5, Gimbal_Pitch = 0, Gimbal_Yaw = 0):
        #AddSpeedCommand(self,Waypoint_Speed)
        WaypointCommand = {
            "AMSLAltAboveTerrain": None,
            "Altitude": Waypoint_AltRel,
            "AltitudeMode": 1,
            "autoContinue": True,
            "command": 16,
            "doJumpId": self.GetItemNum()+1,
            "frame": 3,
            "params": [
                0,
                0,
                0,
                None,
                Waypoint_Lat,
                Waypoint_Lon,
                Waypoint_AltRel
            ],
            "type":"SimpleItem"
        }
        self.BaseFile["mission"]["items"].append(WaypointCommand)
        if Gimbal_Pitch != 0 or Gimbal_Yaw != 0:
            self.AddGimbalCommand(Gimbal_Pitch, Gimbal_Yaw)
        if Waypoint_Speed != 5 :
            self.AddSpeedCommand(Waypoint_Speed)
    
    def AddLandtoTakeoffPointCommand(self):
        LandtoTakeoffPointCommand = {
            "autoContinue": True,
            "command": 20,
            "doJumpId": self.GetItemNum()+1,
            "frame": 2,
            "params": [
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "type": "SimpleItem"
        }
        self.BaseFile["mission"]["items"].append(LandtoTakeoffPointCommand)
        
    def GenerateFile(self,TargetFileName):
        with open(TargetFileName,"w+",encoding = "utf-8") as f:
            f.write(json.dumps(self.BaseFile))
            # print(self.BaseFile)

        


    
if __name__ == "__main__":
    plangenerater = PlanGenerater()
    plangenerater.ChangeTakeoffPoint(51, 114, 4)
    plangenerater.AddWaypoint(51.004000144, 114.05000012, 53)
    plangenerater.AddWaypoint(51.000000204, 114.02000012, 56)
    plangenerater.AddWaypoint(51.006000454, 114.00000000, 30)
    plangenerater.AddLandtoTakeoffPointCommand()
    plangenerater.GenerateFile("generatedplan.plan")
    
