import serial
import plotly.graph_objs as go
from IPython.display import display
from .faultier_pb2 import *
import struct
import subprocess
import os

# Get the directory of the current module
MODULE_DIR = os.path.dirname(os.path.realpath(__file__))

def convert_uint8_samples(input: bytes):
    r = []
    for b in input:
        r.append(b/255)
    return r
"""
    This class is used to control the Faultier.

    All functionality that configures the ADC or the glitcher
    require opening the device first, the OpenOCD debug probe
    is always active and does not use the serial interface.
    Because of this the functions using OpenOCD (such as nrf_flash_and_lock)
    are marked as static and can be called without initializing
    the Faultier first.
"""
class Faultier:
    """
    :param path: The path to the serial device. Note that the Faultier exposes
                 two serial devices - the first one is the control channel.
                 
                 On mac this will be /dev/cu.usbmodemfaultier1.
    """
    def __init__(self, path):
        """
        test
        """
        self.device = serial.Serial(path)
        self.device.timeout = 5
    
    def _read_response(self):
        header = self.device.read(4)
        if(header != b"FLTR"):
            print(header)
            raise ValueError("Invalid header received.")
        length_data = self.device.read(4)
        length = struct.unpack("<I", length_data)[0]
        return self.device.read(length)

    def _check_response(self):
        response = self._read_response()
        resp = Response()
        resp.ParseFromString(response)
        if resp.WhichOneof('type') == 'error':
            raise ValueError("Error: " + resp.error.message)
        if resp.WhichOneof('type') == 'trigger_timeout':
            raise ValueError("Trigger timeout!")
        return resp

    def _check_ok(self):
        response = self._read_response()
        resp = Response()
        resp.ParseFromString(response)
        if resp.ok:
            return
        if resp.error:
            raise ValueError("Error: " + resp.error.message)
        else:
            raise ValueError("No OK or Error received.", resp)

    # def captureADC(self):
    #     # TODO will be replaced by command structure
    #     self.device.write(b"A")
    #     response = self._read_response()
    #     resp = ResponseADC()
    #     resp.ParseFromString(response)
    #     return convert_uint8_samples(resp.samples)
    
    def _send_protobuf(self, protobufobj):
        serialized = protobufobj.SerializeToString()
        length = len(serialized)
        # Header
        self.device.write(b"FLTR")
        self.device.write(struct.pack("<I", length))
        self.device.write(serialized)
        self.device.flush()

    def configure_adc(self, source, sample_count):
        configure_adc = CommandConfigureADC(
            source = source,
            sample_count = sample_count
        )
        cmd = Command()
        cmd.configure_adc.CopyFrom(configure_adc)
        self._send_protobuf(cmd)
        self._check_ok()

    def configure_glitcher(self, trigger_type, trigger_source, glitch_output, delay, pulse, power_cycle_length=1000000, power_cycle_output = GLITCH_OUT_NONE, ):
        """
        Configures the glitcher, i.e. glitch-output, delay, pulse, etc. It does not Arm
        or cause any other change to IOs until glitch() is called.

        :param delay: The delay between Trigger and Glitch.

        :param pulse: The glitch pulse length.

        :param trigger_type: The type of trigger that should be used

            - `TRIGGER_NONE`: No Trigger. The glitch will wait the delay and then glitch.
            - `TRIGGER_LOW`: Waits for the signal to be low. If the signal is low to begin with this will trigger immediately.
            - `TRIGGER_HIGH`: Waits for the signal to be high. If the signal is low to begin with this will trigger immediately.
            - `TRIGGER_RISING_EDGE`: Waits for a rising edge on the trigger input.
            - `TRIGGER_FALLING_EDGE`: Waits for a falling edge on the trigger input.
        
        :param trigger_source: The source - as in physical input - of the trigger.

            - `TRIGGER_IN_NONE`: Ignored, use TRIGGER_NONE to disable triggering.
            - `TRIGGER_IN_EXT0`: Configure EXT0 as digital input and use it for triggering.
            - `TRIGGER_IN_EXT1`: Configure EXT1 as digital input and use it for triggering.

        :param glitch_output: The glitch-output that will be used.

            - `GLITCH_OUT_CROWBAR`: Route the glitch to the gate of the Crowbar MOSFET.
            - `GLITCH_OUT_MUX0`: Route the glitch to control channel 0/X of the analogue switch (the one exposed on the SMA connector).
            - `GLITCH_OUT_MUX1`: Route the glitch to channel 1/Y of the analogue switch (exposed on 20-pin header).
            - `GLITCH_OUT_MUX2`: Route the glitch to channel 2/Z of the analogue switch (exposed on 20-pin header).
            - `GLITCH_OUT_EXT0`: Route the glitch signal to the EXT0 header. Useful to trigger external tools such as a ChipSHOUTER or laser.
            - `GLITCH_OUT_EXT1`: Route the glitch signal to the EXT1 header. Same as above.
            - `GLITCH_OUT_NONE`: Disable glitch generation. Power-cycle, trigger, ADC & co will still run as regular. Good for trigger testing.

        :param power_cycle: Whether a separate output should be toggled before activating the trigger-delay-glitch pipeline. Useful to restart a target.

            - `GLITCH_OUT_CROWBAR`: Route the power-cycle to the gate of the Crowbar MOSFET.
            - `GLITCH_OUT_MUX0`: Route the power-cycle to control channel 0/X of the analogue switch (the one exposed on the SMA connector).
            - `GLITCH_OUT_MUX1`: Route the power-cycle to channel 1/Y of the analogue switch (exposed on 20-pin header).
            - `GLITCH_OUT_MUX2`: Route the power-cycle to channel 2/Z of the analogue switch (exposed on 20-pin header).
            - `GLITCH_OUT_EXT0`: Route the power-cycle signal to the EXT0 header. Useful to trigger external tools such as a ChipSHOUTER or laser.
            - `GLITCH_OUT_EXT1`: Route the power-cycle signal to the EXT1 header. Same as above.
            - `GLITCH_OUT_NONE`: Disable power-cycle generation.

        :param power_cycle_length: The number of clock-cycles for the power cycle.
        """
        configure_glitcher = CommandConfigureGlitcher(
                trigger_type = trigger_type,
                trigger_source = trigger_source,
                glitch_output = glitch_output,
                delay = delay,
                pulse = pulse,
                power_cycle_output = power_cycle_output,
                power_cycle_length = power_cycle_length)
        cmd = Command()
        cmd.configure_glitcher.CopyFrom(configure_glitcher)
        self._send_protobuf(cmd)
        self._check_ok()

    def glitch(self, delay, pulse):
        self.configure_glitcher(
            trigger_type=TRIGGER_NONE,
            trigger_source=TRIGGER_IN_EXT0,
            glitch_output=GLITCH_OUT_CROWBAR,
            power_cycle_output=GLITCH_OUT_MUX0,
            power_cycle_length=1000000,
            delay=delay,
            pulse=pulse)
        self.glitch()

    def glitch(self):
        cmd = Command()
        cmd.glitch.CopyFrom(CommandGlitch())
        self._send_protobuf(cmd)
        self._check_response()

    def swd_check(self):
        cmd = Command()
        cmd.swd_check.CopyFrom(CommandSWDCheck(function = SWD_CHECK_ENABLED))
        self._send_protobuf(cmd)
        response = self._check_response()
        return response.swd_check.enabled

    def nrf52_check(self):
        cmd = Command()
        cmd.swd_check.CopyFrom(CommandSWDCheck(function = SWD_CHECK_NRF52))
        self._send_protobuf(cmd)
        try:
            response = self._check_response()
        except:
            # TODO check for debug errors only
            return False
            pass
        return response.swd_check.enabled

    def read_adc(self):
        cmd = Command()
        cmd.read_adc.CopyFrom(CommandReadADC())
        self._send_protobuf(cmd)
        response = self._check_response()
        return convert_uint8_samples(response.adc.samples)

    @staticmethod
    def nrf_flash_and_lock():
        env = {
            'PATH': "/usr/local/bin:/usr/bin:/opt/homebrew/bin"
        
        }
        print("Erasing...")
        subprocess.run(["openocd", "-s", "/usr/local/share/openocd", "-f", "interface/tamarin.cfg", "-f", "target/nrf52.cfg", "-c", "init; nrf52_recover; exit"], env=env)
        print("Programming softdevice...")
        
        subprocess.run([
            "openocd", "-s", "/usr/local/share/openocd",
            "-f", "interface/tamarin.cfg",
            "-f", "target/nrf52.cfg",
            "-c", f"program {os.path.join(MODULE_DIR, '..', 'example_firmware', 's132_nrf52_7.2.0_softdevice.hex')}; exit"
            ], env=env)
        print("Programming firmware...")
        subprocess.run([
            "openocd", "-f", "interface/tamarin.cfg", "-f", "target/nrf52.cfg",
            "-c", f"program {os.path.join(MODULE_DIR, '..', 'example_firmware', 'nrf52832_xxaa.hex')}; exit"
        ], env=env)
        print("Locking chip...")
        subprocess.run(["openocd", "-f", "interface/tamarin.cfg", "-f", "target/nrf52.cfg", "-c", "init; reset; halt; flash fillw 0x10001208 0xFFFFFF00 0x01; reset;exit"], env=env)
    
    def stm32_lock(self):
        import time
        print("This action is not reversible. Locking in 10 seconds, press stop to interrupt.")
        time.sleep(10)
