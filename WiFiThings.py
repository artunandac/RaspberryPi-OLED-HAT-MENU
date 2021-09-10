import subprocess
import os

class WiFiThing():
    def ScanForIPs(self):
        devices = subprocess.check_output(['arp','-a'])
        devices = devices.decode('ascii')
        # devices = devices.replace("\r","")
        devices = devices.replace("\n"," ")
        devices = devices.split("? ")
        devices = devices[1:]
        self.devices = devices
    def IPCount(self):
        return len(self.devices)
    def DeviceList(self):
        return self.devices
    def LongestIPItem(self):
        itemlength = []
        for item in self.devices:
            itemlength.append(len(item))
        itemlength.sort()
        return itemlength[-1]
    def ScanForSSIDs(self):
        ssids = subprocess.check_output(["sudo","iwlist","wlan0","scan"])
        ssids = ssids.replace("          ", "")
        ssids = ssids.split("Cell")
        for index in ssids:
            ssids[ssids.index(index)] = index.split("\n")
        

        ssidinfos = []

        for i in range(len(ssids)):
            ssidinfos.append([])

        ssidlistkeys = ["Address:", "Channel:", "Frequency:", "Quality", "ESSID:", "WPA", "Authentication"]

        for i in range(1,len(ssids)):
            for z in range(len(ssids[i])):
                    for t in ssidlistkeys:
                        if t in ssids[i][z]:
                            ssidinfos[i].append(ssids[i][z])
        ssidinfos.pop(0)
        self.ssidinfos = ssidinfos
    def SSIDsDetails(self):
        return self.ssidinfos
    def eSSIDList(self):
        essidlist = []
        for i in range(len(self.ssidinfos)-1):
            for z in range(len(self.ssidinfos[i])-1):
                if "ESSID:" in self.ssidinfos[i][z]:
                    essidlist.append(self.ssidinfos[i][z])
        self.essidlist = essidlist
        return essidlist
    def LongestSSIDItem(self):
        itemlength = []
        for item in self.ssidinfos:
            itemlength.append(len(item))
        itemlength.sort()
        return itemlength[-1]
    def LongestESSIDItem(self):
        itemlength = []
        for item in self.essidlist:
            itemlength.append(len(item))
        itemlength.sort()
        return itemlength[-1]
    def __init__(self):
        self.ScanForIPs()
        self.ScanForSSIDs()

# wifi = WiFiThing()

# print(wifi.DeviceList())
