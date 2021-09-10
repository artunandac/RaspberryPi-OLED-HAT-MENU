import time
import datetime
import subprocess
import utils as u
import config as c

import WiFiThings
wifi = WiFiThings.WiFiThing()


def shell(cmd):
    return(subprocess.check_output(cmd, shell = True ))

def get_ip():
    cmd = "hostname -I"
    return shell(cmd).split(" ")

def get_max_ip_len():
    tmp = 0
    ip_list = get_ip()
    for i in range(len(ip_list)):
        tmp = max(tmp, len(ip_list[i]))
    return tmp


def sysinfos(channel):
    _id = 0
    i = u.v6
    if channel == 0:
        if u.page != _id:
            #init
            u.page = _id
            u.cursor = 0
        now = datetime.datetime.now()
        today_time = now.strftime("%H:%M:%S")
        today_date = now.strftime("%d %b %y")
        try:
	        IP1, IP2, IP3 = get_ip()
        except:
	        IP1= get_ip()[0]
	        IP2= "Nan"
	        IP3= "Nan"
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        u.gui_buffer = [
            str(CPU),
            str(MemUsage),
            str(Disk),
            "IP1: " + str(IP1)[i:i+14],
            "IP2: " + str(IP2)[i:i+14],
            "IP3: " + str(IP3)[i:i+14],
            today_date + " " + today_time,
        ]

    elif channel == c.KEY_PRESS_PIN:
        sysinfos(0)

    elif channel == c.KEY1_PIN:
        sysinfos(0)

    elif channel == c.KEY_LEFT_PIN:
        if u.v6 > 0:
            u.v6 -= 1
        sysinfos(0)

    elif channel == c.KEY_RIGHT_PIN:
        if u.v6 < get_max_ip_len() - 1:
            u.v6 += 1
        sysinfos(0)

    elif channel == c.KEY2_PIN:
        mainmenu(0)

def auto_hotspot(channel):
    _id = 7
    if channel == 0:
        if u.page != _id:
            #init
            u.page = _id
            u.cursor = 0
        u.gui_buffer = [
            "",
            "Do you want to restart",
            "AutoHotSpotN",
            "",
            " > No",
            "   Yes",
            ""
        ]
    elif channel == c.KEY_DOWN_PIN:
        u.cursor = 1
        u.gui_buffer = [
            "",
            "Do you want to restart",
            "AutoHotSpotN",
            "",
            "   No",
            " > Yes",
            ""
        ]
    elif channel == c.KEY_UP_PIN:
        u.cursor = 0
        u.gui_buffer = [
            "",
            "Do you want to restart",
            "AutoHotSpotN",
            "",
            " > No",
            "   Yes",
            ""
        ]
    elif channel == c.KEY1_PIN:
        if u.cursor == 0:
            mainmenu(0)
        elif u.cursor == 1:
            # reset

            # GUI reset
            u.gui_buffer = [
            "",
            "AutoHotSpotN Restarting",
            "",
            "",
            "",
            "",
            ""
            ]
            time.sleep(0.1)
            shell("sudo /usr/bin/autohotspotN")
            mainmenu(0)

    elif channel == c.KEY2_PIN:
        mainmenu(0)

def IPMenu(channel):
    _id = 1
    locip = u.iploc
    if channel == 0:
        if u.page != _id:
            #init
            u.page = _id
            u.cursor = 0
        for index in range(7):
            i = index + u.cursor
            if index == 0:
                u.gui_buffer[index] = "> " + str(wifi.DeviceList()[i][locip:]) if i < wifi.LongestIPItem() else ""
            else:
                u.gui_buffer[index] = "  " + str(wifi.DeviceList()[i]) if i < wifi.LongestIPItem() else "" # [locip:locip+20]

    elif channel == c.KEY_UP_PIN:
        if u.cursor > 0:
            u.cursor -= 1
            u.iploc = 0
            IPMenu(0)

    elif channel == c.KEY_DOWN_PIN:
        if u.cursor < len(wifi.DeviceList()) - 1:
            u.cursor += 1
            u.iploc = 0
            IPMenu(0)

    elif channel == c.KEY_LEFT_PIN:
        if u.iploc > 0:
            u.iploc -= 1
            IPMenu(0)
        
    elif channel == c.KEY_RIGHT_PIN:
        if u.iploc < wifi.LongestIPItem() - 1:
            u.iploc += 1
        IPMenu(0)

    elif channel == c.KEY_PRESS_PIN:
        wifi.ScanForIPs()
        IPMenu(0)

    elif channel == c.KEY1_PIN:
        wifi.ScanForIPs()
        IPMenu(0)

    elif channel == c.KEY2_PIN:
        mainmenu(0)
    elif channel == c.KEY3_PIN:
        return 0
def SSIDDetails(channel):
    _id = 12
    locssid = u.ssidinfoloc
    if channel == 0:
        if u.page != _id:
            #init
            u.page = _id
            u.cursor = 0
        for index in range(7):
            i = index + u.cursor
            if index == 0:
                u.gui_buffer[index] = "> " + str(wifi.SSIDsDetails()[u.details][i][locssid:]) if i < len(wifi.SSIDsDetails()[u.details][i]) else ""
            else:
                u.gui_buffer[index] = "  " + str(wifi.SSIDsDetails()[u.details][i]) if i < len(wifi.SSIDsDetails()[u.details][i]) else "" # [locssid:locssid+20]
    elif channel == c.KEY_UP_PIN:
        if u.cursor > 0:
            u.cursor -= 1
            u.ssidinfoloc = 0
            SSIDDetails(0)

    elif channel == c.KEY_DOWN_PIN:
        if u.cursor < wifi.LongestSSIDItem() - 1:
            u.cursor += 1
            u.ssidinfoloc = 0
            SSIDDetails(0)

    elif channel == c.KEY_LEFT_PIN:
        if u.ssidinfoloc > 0:
            u.ssidinfoloc -= 1
        SSIDDetails(0)
        
    elif channel == c.KEY_RIGHT_PIN:
        if u.ssidinfoloc < wifi.LongestSSIDItem() - 1:
            u.ssidinfoloc += 1
        SSIDDetails(0)

    elif channel == c.KEY_PRESS_PIN:
        return 0

    elif channel == c.KEY1_PIN:
        return 0

    elif channel == c.KEY2_PIN:
        SSIDMenu(0)
    elif channel == c.KEY3_PIN:
        return 0

def SSIDMenu(channel):
    _id = 2
    locessid = u.essidloc
    if channel == 0:
        if u.page != _id:
            #init
            u.page = _id
            u.cursor = 0
        for index in range(7):
            i = index + u.cursor
            if index == 0:
                u.gui_buffer[index] = "> " + str(wifi.eSSIDList()[i][locessid:]) if i < wifi.LongestESSIDItem() else ""
            else:
                u.gui_buffer[index] = "  " + str(wifi.eSSIDList()[i]) if i < wifi.LongestESSIDItem() else "" # [locssid:locssid+20]

    elif channel == c.KEY_UP_PIN:
        if u.cursor > 0:
            u.cursor -= 1
            u.essidloc = 0
            SSIDMenu(0)
        elif u.cursor == 0:
            wifi.ScanForSSIDs()
            u.gui_buffer =  [
                "",
                "Scanning",
                "For",
                "SSIDs",
                "",
                "",
                "Please Wait"
                ]
            time.sleep(0.5)
            SSIDMenu(0)

    elif channel == c.KEY_DOWN_PIN:
        if u.cursor < len(wifi.eSSIDList()) - 1:
            u.cursor += 1
            u.essidloc = 0
            SSIDMenu(0)

    elif channel == c.KEY_LEFT_PIN:
        if u.essidloc > 0:
            u.essidloc -= 1
        SSIDMenu(0)
        
    elif channel == c.KEY_RIGHT_PIN:
        if u.essidloc < wifi.LongestESSIDItem() - 1:
            u.essidloc += 1
        SSIDMenu(0)

    elif channel == c.KEY_PRESS_PIN:
        u.details = u.cursor
        SSIDDetails(0)

    elif channel == c.KEY1_PIN:
        u.details = u.cursor
        SSIDDetails(0)
    elif channel == c.KEY2_PIN:
        mainmenu(0)
    elif channel == c.KEY3_PIN:
        return 0

def select_module(_id):
    if   _id == 0:
        #system info
        sysinfos(0)

    elif _id == 1:
        IPMenu(0)

    elif _id == 2:
        SSIDMenu(0)

    elif _id == 3:
        return 0

    elif _id == 4:
        u.gui_buffer = [
            "",
            "Good Bye",
            "",
            "",
            "Have A Nice Day!",
            "",
            ""
            ]
        time.sleep(1)
        u.gui_buffer = [
            "",
            "",
            "",
            "",
            "",
            "",
            ""
            ]
        time.sleep(0.5)
        exit()

    elif _id == 5:
        shell("sudo poweroff")

    elif _id == 6:
        shell("sudo reboot")

    elif _id == 7:
        auto_hotspot(0)
    elif _id == 12:
        SSIDDetails(0)

def mainmenu(channel):
    _id = -1
    if channel == 0:
        if u.page != _id:
            #init
            u.page = _id
            u.cursor = 0
        for index in range(7):
            i = index + u.cursor
            if index == 0:
                u.gui_buffer[index] = "> " + str(u.mainmenu_list[i] if i < len(u.mainmenu_list) else "")
            else:
                u.gui_buffer[index] = "  " + str(u.mainmenu_list[i] if i < len(u.mainmenu_list) else "")

    elif channel == c.KEY_UP_PIN:
        if u.cursor > 0:
            u.cursor -= 1
            mainmenu(0)

    elif channel == c.KEY_DOWN_PIN:
        if u.cursor < len(u.mainmenu_list) - 1:
            u.cursor += 1
            mainmenu(0)

    elif channel == c.KEY_LEFT_PIN:
        return 0
    elif channel == c.KEY_RIGHT_PIN:
        return 0

    elif channel == c.KEY_PRESS_PIN:
        select_module(u.cursor)

    elif channel == c.KEY1_PIN:
        select_module(u.cursor)

    elif channel == c.KEY2_PIN:
        return 0
    elif channel == c.KEY3_PIN:
        return 0

def key_handler(channel):
    if u.page == -1:
        mainmenu(channel)
    elif u.page == 0:
        sysinfos(channel)
    elif u.page == 1:
        IPMenu(channel)
    elif u.page == 2:
        SSIDMenu(channel)
    elif u.page == 7:
        auto_hotspot(channel)
    elif u.page == 12:
        SSIDDetails(channel)
