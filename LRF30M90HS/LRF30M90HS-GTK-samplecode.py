# =============================================================================
# The example program will use the GTK3 framework. Please use the following command to install the required packages.
# $sudo apt-get install libgtk-3-dev python3-gi
# =============================================================================

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib
from gi.repository import Gtk
import sys
import serial 
import threading
import time


#GTK UI
class SimpleUI(Gtk.Window):              
    def __init__(self):
        Gtk.Window.__init__(self, title="Simple UI")
        self.set_border_width(10)

        # 创建布局
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(self.box)

        # 创建左侧布局
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.pack_start(left_box, True, True, 0)

        # 创建按钮1
        self.button1 = Gtk.Button(label="Start")
        self.button1.connect("clicked", self.on_button1_clicked)
        left_box.pack_start(self.button1, True, True, 0)

        # 创建按钮2
        self.button2 = Gtk.Button(label="Stop")
        self.button2.connect("clicked", self.on_button2_clicked)
        left_box.pack_start(self.button2, True, True, 0)

        # 创建右侧布局
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.pack_start(right_box, True, True, 0)

        # 创建Label
        self.label = Gtk.Label(label="N/A", xalign=0.5)  # xalign 控制文本水平对齐
        self.label.set_size_request(200, -1)  # 设置固定宽度
        right_box.pack_start(self.label, True, True, 0)

    def on_button1_clicked(self, widget):
        cmd=b'~0106003000014805\r\n'
        self.ser.write(cmd)  

    def on_button2_clicked(self, widget):
        cmd=b'~01060030000089C5\r\n'
        self.ser.write(cmd) 
    def update_label(self, text):
        self.label.set_text(text)
        
    ##LRF##
    #Set COM port
    ser = serial.Serial()
    ser.port = '/dev/ttyUSB2'
    ser.baudrate = 115200
    ser.bytesize = 8
    ser.parity = 'N'
    ser.topbits = 1
    ser.timeout = 100
    ser.open()
    
    def receive(self):
        while(True):
            data=self.ser.read_all()
            if(len(data)>0):
                # self.label.set_text(str(data))   
                if(len(data)==19):
                    distance=int(data[9:13].decode('ascii'), 16)
                    if distance == 30000:
                        GLib.idle_add(self.update_label, "N/A")
                    else:
                        GLib.idle_add(self.update_label, f"{distance} mm")

# #main
win = SimpleUI()
win.connect("destroy", Gtk.main_quit)

t = threading.Thread(target=SimpleUI.receive, args=(win,))
t.start()

win.show_all()
Gtk.main()