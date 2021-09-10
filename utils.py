already = False
display_on_off = True
page = -1
cursor = 0
details = 0 # for detail menus
gui_buffer = []
mainmenu_list = {}
brightness = 0
v6 = 0 # ipv6 len index
iploc = 0 # w/lan info len index
essidloc = 0
ssidinfoloc = 0 # ssid info len index

def init():
    global already, display_on_off, cursor, mainmenu_list, gui_buffer, v6, brightness, details, iploc, essidloc, ssidinfoloc
    already = False
    display_on_off = True
    page = -1
    cursor = 0
    v6 = 0
    brightness = 0
    gui_buffer = ["","","","","","",""]
    mainmenu_list = [
        "System info",               #   0
        "IP List",                   #   1
        "SSID List",                 #   2
        "Games(XOX)(Coming Soon)",   #   3
        "Exit",                      #   4
        "Shutdown",                  #   5
        "Reboot",                    #   6
        "AutoHotSpotN"               #   7
    ]
    details = 0
    iploc = 0
    essidloc = 0
    ssidinfoloc = 0