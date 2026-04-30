from abc import ABC, abstractmethod

class MedicalDeviceInterface(ABC):
    """
    Base interface for all medical devices. 
    This allows both simulated and real hardware implementations in the future.
    """
    
    @abstractmethod
    def get_test_procedures(self):
        """Returns a list of test names for this device type."""
        pass

    @abstractmethod
    def run_tests(self, progress_callback=None):
        """
        Executes the testing suite.
        progress_callback: A function that takes (current_step, total_steps, message)
        Returns: Dict of {test_name: status}
        """
        pass
