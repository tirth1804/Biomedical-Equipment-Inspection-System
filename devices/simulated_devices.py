import time
import random
from devices.device_interface import MedicalDeviceInterface

class SimulatedDevice(MedicalDeviceInterface):
    def __init__(self, device_name, procedures):
        self.device_name = device_name
        self.procedures = procedures

    def get_test_procedures(self):
        return self.procedures

    def run_tests(self, progress_callback=None):
        results = {}
        total = len(self.procedures)
        
        for i, test in enumerate(self.procedures):
            if progress_callback:
                progress_callback(i + 1, total, f"Running {test}...")
            
            # Simulate processing time
            time.sleep(random.uniform(0.5, 1.5))
            
            # Simulate real-world logic (mostly pass, occasional fail)
            status = "Pass" if random.random() > 0.15 else "Fail"
            results[test] = status
            
        return results

class ECGSimulator(SimulatedDevice):
    def __init__(self):
        procedures = [
            "Power-On Self Test",
            "Lead-Off Detection",
            "Baseline Stability",
            "Common Mode Rejection",
            "Heart Rate Accuracy",
            "Printer Mechanism Check"
        ]
        super().__init__("ECG Machine", procedures)

class VentilatorSimulator(SimulatedDevice):
    def __init__(self):
        procedures = [
            "Oxygen Supply Pressure",
            "Air Supply Pressure",
            "Exhalation Valve Test",
            "Safety Valve Test",
            "Flow Sensor Calibration",
            "Battery Backup Test"
        ]
        super().__init__("Ventilator", procedures)

class PatientMonitorSimulator(SimulatedDevice):
    def __init__(self):
        procedures = [
            "Display Pixel Test",
            "NIBP Pump Test",
            "SpO2 Module Sync",
            "Temperature Probe Continuity",
            "Alarm System Audio",
            "Network Connection"
        ]
        super().__init__("Patient Monitor", procedures)

def get_simulator_for_type(device_type):
    simulators = {
        "ECG": ECGSimulator(),
        "Ventilator": VentilatorSimulator(),
        "Patient Monitor": PatientMonitorSimulator()
    }
    return simulators.get(device_type, SimulatedDevice("Generic", ["General Power Test", "UI Check"]))
