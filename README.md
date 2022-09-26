# Antenna-Tracking-Drone-Project

## Description

这是一个与电院天线所合作的项目，由501实验室的研发学生Phillweston与Devotlig负责联合开发基于pixhawk的无人机飞行与云台控制以及空地通信的部分，由天线所的研究团队负责负载设备的设计与数据处理。

## Project Structure

待补充

## Hardware

- 飞控：雷迅V5+，NEO V2 GPS
- 机载计算机：树莓派4
- 遥控和接收设备：天地飞7 + SBUS接收机
- 云台：待指定
- 负载设备：信号源 + 一对偶极子天线
- WiFi通信设备：蒲公英R300 4G工业路由器

## Function

以下功能均在树莓派4机载计算机上面实现

- [ ] 三轴云台串口控制
- [x] 航点生成
- [ ] 云台控制
- [ ] 图形界面

## Simulation

仿真功能在VMware ESXi虚拟机中实现，使用Clover VM镜像。

## Maintenance

- Project Owner: Phillweston
- Copilot: Devotlig

### 9月27日更新，增加csv航点导入支持