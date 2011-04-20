import socket
import gobject
import gtk
import appindicator
import netifaces as ni

#######################################################################
import dbus, dbus.service, gobject, threading
from dbus.mainloop.glib import DBusGMainLoop
from dbus.service import method, signal

# This and a few other snippets give a much richer plugin API with DBus
#######################################################################
# start dbus main loop
DBusGMainLoop(set_as_default=True)

# set some dbus options
DBUS_BUSNAME = "org.dosprompt.DOSprompt"
DBUS_IFACE = 'org.dosprompt.DOSpromptAPI'
DBUS_PATH = '/org/dosprompt/DOSprompt/PluginAPI'

class ExampleObject(dbus.service.Object):

    @method(dbus_interface=DBUS_IFACE, in_signature="s")
    def example_method(self, prompt='nochange'):
        print prompt
        return 'prompt set to %s' % prompt

session_bus = dbus.SessionBus()
busname = dbus.service.BusName(DBUS_BUSNAME, bus=session_bus)
eo = ExampleObject(object_path=DBUS_PATH, bus_name=busname)

loop = gobject.MainLoop()

#######################################################################

def start():
    loop.run()
    
def stop():
    loop.quit()
#######################################################################



def getip():
    reload(ni)
    iw = ni.ifaddresses('wlan0')
    try: ip = iw[2][0]['addr']
    except KeyError: ip = 'err'
    if ip == 'err': 
        ind.set_status(appindicator.STATUS_ATTENTION)
        return
    ind.set_status(appindicator.STATUS_ACTIVE)
    return '.'.join(ip.split('.')[2:])

def getfip(): # get the full ip address
    iw = ni.ifaddresses('wlan0')
    try: ip = iw[2][0]['addr']
    except KeyError: ip = 'Disconnected'
    return ip


def update():
  ind.set_label(getip())
  ip_entry.set_label("IP Addr: %s" % getfip())
  hn_entry.set_label("Hostname: %s" % socket.gethostname())
  return True

def menuitem_response(w, buf):
  update()
  
  
ind = appindicator.Indicator ("indicator-ipaddr",
                              "",
                              appindicator.CATEGORY_APPLICATION_STATUS)
ind.set_status (appindicator.STATUS_ACTIVE)
ind.set_attention_icon ("network-offline")

# create a menu
menu = gtk.Menu()

# create some items
buf = "IP Addr: %s" % getfip()
ip_entry = gtk.MenuItem(buf)
ip_entry.set_sensitive(False)
menu.append(ip_entry)
ip_entry.show()
  
buf = "Hostname: %s" % socket.gethostname()
hn_entry = gtk.MenuItem(buf)
hn_entry.set_sensitive(False)
menu.append(hn_entry)
hn_entry.show()
  
  
buf = "Refresh"
menu_items = gtk.MenuItem(buf)

menu.append(menu_items)
  
menu_items.connect("activate", menuitem_response, buf)

# show the items
menu_items.show()

buf = "Quit"
menu_items = gtk.MenuItem(buf)

menu.append(menu_items)
  
def quitter(a, b):
    print "Seeya later!"
    exit()
  
menu_items.connect("activate", quitter, buf)

# show the items
menu_items.show()




ind.set_label(getip())

if __name__ == "__main__":


  ind.set_menu(menu)
  gobject.timeout_add_seconds(5, update)
  gtkloop = gtk.main()
