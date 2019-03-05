#https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.characteristic.heart_rate_measurement.xml
import gatt
from datetime import datetime
import argparse
#import mac
from UUIDmappings import ser_to_name, char_to_name

manager = gatt.DeviceManager(adapter_name='hci0')

from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="172.20.10.4", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.UDPClient(args.ip, args.port)
# client = udp_client.SimpleUDPClient(args.ip, args.port)


class AnyDevice(gatt.Device):
    _UUID_SERVICE_DEV_INFO = '0000180a-0000-1000-8000-00805f9b34fb'
    _UUID_SERVICE_BATT = '0000180f-0000-1000-8000-00805f9b34fb'
    _UUID_SERVICE_HR = '0000180d-0000-1000-8000-00805f9b34fb'

    _UUID_CHARACTER_FIRMWARE_VER = '00002a26-0000-1000-8000-00805f9b34fb'
    _UUID_CHARACTER_BAT_LVL = '00002a19-0000-1000-8000-00805f9b34fb'
    _UUID_CHARACTER_HR_MEASURE = '00002a37-0000-1000-8000-00805f9b34fb'

    buff = []
    BUFF_SIZE = 300

    def print_out_services(self):
        """Walks through all self.servies printing out the uuids and their
        names. Should only be called *after* services_resolved() has been
        called."""
        print("RESOLVED SERVICES:")
        for s in self.services:
            print(s.uuid, "  " + ser_to_name.get(s.uuid[4:8], "Unknown"))
            if s.characteristics:
                for c in s.characteristics:
                    print(" -", c.uuid, char_to_name.get(c.uuid[4:8],
                          "Unknown"))

    def services_resolved(self):
        "Called after working out what services are offered"
        super().services_resolved()

        self.print_out_services()

        for s in self.services:
            if s.uuid == self._UUID_SERVICE_DEV_INFO:
                for c in s.characteristics:
                    if c.uuid == self._UUID_CHARACTER_FIRMWARE_VER:
                        c.read_value()
            elif s.uuid == self._UUID_SERVICE_BATT:
                for c in s.characteristics:
                    if c.uuid == self._UUID_CHARACTER_BAT_LVL:
                        c.read_value()
            elif s.uuid == self._UUID_SERVICE_HR:
                for c in s.characteristics:
                    if c.uuid == self._UUID_CHARACTER_HR_MEASURE:
                        c.enable_notifications()

    def characteristic_value_updated(self, characteristic, value):
        "Callback after reading a value or notification of value"
        if characteristic.uuid == self._UUID_CHARACTER_FIRMWARE_VER:
            print("Firmware version:", value.decode("utf-8"))
        elif characteristic.uuid == self._UUID_CHARACTER_BAT_LVL:
            print("Battery level:", value[0])
        elif characteristic.uuid == self._UUID_CHARACTER_HR_MEASURE:
            # TODO: There is much more information. See example code.
            print("\t\t\traw ", value )
            print("HR Rec:", value[1], "rr?: ", chr(value[2])  )
            for v in value:
                print("\t ", '{:f}'.format(v) )
            self.send(value[1])
        else:
            print("Unrecognised value:", value, "from:", characteristic.uuid,
                  char_to_name.get(characteristic.uuid[4:8],
                                   "Char name unrecognised."))

    def send(self, val):
        ## osc stuff
        # client.send_message("/hrm", val)
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        msg = osc_message_builder.OscMessageBuilder(address="/hrm")


        msg.add_arg(val)
        bundle.add_content(msg.build())

        client.send(bundle.build())


device = AnyDevice(mac_address='00:22:D0:8D:7D:98', manager=manager)
device.connect()



callOnce = True
########################################################################################

def loop():
    global callOnce

    if callOnce:
        print("call once")
        manager.run()
        callOnce = False

def exit():
    print("\n\n\n<3 Adios Corazon\n")
    manager.stop()



















########################################################################################
if __name__ == "__main__":
    try:
        while True:
            loop()
            # pass
    except KeyboardInterrupt:
        exit()
        pass
