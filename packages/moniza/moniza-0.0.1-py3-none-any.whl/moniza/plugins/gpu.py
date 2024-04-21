#!/usr/bin/env python
# -*- coding: utf-8 -*-
import plugins
import sys
import os

class Plugin(plugins.BasePlugin):
    __name__ = 'gpu'

    def run(self, *unused):
        '''
        expirimental plugin used to collect GPU load from OpenHardWareMonitor (Windows)
        '''
        data = {}

        results = {}

        if sys.platform == "win32":
            try:
                import wmi
            except:
                return 'wmi module not installed.'
            try:
                w = wmi.WMI(namespace="root\OpenHardwareMonitor")
                temperature_infos = w.Sensor()
                for sensor in temperature_infos:
                    if sensor.SensorType==u'Load' and sensor.Name==u'GPU Core':
                        data[sensor.Parent.replace('/','-').strip('-')] = sensor.Value
            except:
                return 'Could not fetch GPU Load data from OpenHardwareMonitor.'
        else:
            if os.path.exists('/usr/bin/nvidia-smi'): # Check for Nvidia GPU tool
                gpu_output = os.popen('nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader').read().strip()
                results['utilization'] = int(gpu_output.split()[0])
            elif os.path.exists('/opt/rocm/bin/rocm-smi'): # Check for AMD GPU tool
                gpu_output = os.popen('/opt/rocm/bin/rocm-smi -u').read().strip()
                results['utilization'] = int(gpu_output.split()[5])
            else:
                return "GPU not found"
            
        self.set_moniza_cache(results)
        return results


if __name__ == '__main__':
    Plugin().execute()
