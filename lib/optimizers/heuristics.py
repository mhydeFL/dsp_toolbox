import logging
from typing import Optional

from dsp.types import PIDGains, T


logging.basicConfig(level=logging.DEBUG)


class ZNTuning:
    """
    Ziegler-Nichols method of PID tuning
    """
    def __init__(
        self,
        Ku: T,
        Tu: T,
        method: str
    ) -> None:
        self.Ku: T = Ku
        self.Tu: T = Tu
        self.method: str = method
        self.eval_function: function
        self.valid = self.validate()

    def __call__(self) -> Optional[PIDGains]:
        if not self.is_valid:
            logging.error("Configuration invalid")
            return None
        logging.info(f"Calculating gains for {self.eval_function.__name__} controller")
        return self.eval_function()
    
    def P(self) -> PIDGains:
        Kp = 0.5 * self.Ku
        return PIDGains(Kp)
    
    def PI(self) -> PIDGains:
        Kp = 0.45 * self.Ku
        Ki = 0.54 * self.Ku/self.Tu
        return PIDGains(Kp, Ki)
    
    def PID(self) -> PIDGains:
        Kp = 0.6*self.Ku
        Ki = 0.12*self.Ku/self.Tu
        Kd = 0.075*self.Ku*self.Tu
        return PIDGains(Kp, Ki, Kd)
    
    def PIDOvershoot(self) -> PIDGains:
        Kp = 0.33*self.Ku
        Ki = 0.66*self.Ku/self.Tu
        Kd = 0.11*self.Ku*self.Tu
        return PIDGains(Kp, Ki, Kd)
    
    def PIDNoOvershoot(self) -> PIDGains:
        Kp = 0.2*self.Ku
        Ki = 0.4*self.Ku/self.Tu
        Kd = 0.066*self.Ku*self.Tu
        return PIDGains(Kp, Ki, Kd)
    
    def validate(self) -> bool:
        if self.Ku <= 0:
            logging.error(f"Ku <= 0: {self.Ku}")
            return False
        if self.Tu <= 0:
            logging.error(f"Tu <= 0: {self.Tu}")
            return False
        if not hasattr(self, self.method):
            logging.error(f"{self.method} not a method of {self.__class__.__name__}")
            return False
        self.eval_function = getattr(self, self.method)
        return True
    
    @property
    def is_valid(self) -> bool:
        return self.valid

    
class CCTuning:
    """
    Cohen-Coon method of PID tuning
    """
    def __init__(self) -> None:
        pass
    
    def evaluate(self) -> PIDGains:
        pass
