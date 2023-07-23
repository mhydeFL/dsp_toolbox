import logging
from typing import Optional
from abc import ABC
import numpy as np

from dsp_toolbox.dsp.types import PIDGains, T


logging.basicConfig(level=logging.INFO)


class BaseHeuristic(ABC):
    def __call__(self) -> Optional[PIDGains]:
        if not self.is_valid:
            logging.error("Configuration invalid")
            return None
        logging.info(f"Calculating gains for {self.eval_function.__name__} controller")
        return self.eval_function()

    def validate(self) -> bool:
        raise RuntimeError("Cannot call Base Heuristic class")

    @property
    def is_valid(self) -> bool:
        raise RuntimeError("Cannot call Base Heuristic class")


class ZNTuning(BaseHeuristic):
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

    
class CCTuning(BaseHeuristic):
    """
    Cohen-Coon method of PID tuning
    """
    def __init__(
        self,
        A: T,
        B: T,
        t0: T,
        t2: T,
        t3: T,
        method: str
    ) -> None:
        self.A: T = A
        self.B: T = B
        self.t0: T = t0
        self.t2: T = t2
        self.t3: T = t3
        
        self.t1: T = None
        self.tau: T = None
        self.tau_del: T = None
        self.K: T = None
        self.r: T = None
        
        self.method: str = method
        self.eval_function: function
        self.valid = self.validate()
    
        if self.is_valid:
            self.generate_process_params()

    def P(self) -> PIDGains:
        Kp = (1/(self.r*self.K))*(1+self.r/3)
        return PIDGains(Kp)
    
    def PI(self) -> PIDGains:
        Kp = (1/(self.r*self.K))*(0.9 + self.r/12)
        Ki = self.tau_del*((30+3*self.r)/(9+20*self.r))
        return PIDGains(Kp, Ki)
    
    def PID(self) -> PIDGains:
        Kp = (1/(self.r*self.K))*((4/3)+(self.r/4))
        Ki = self.tau_del*((32+6*self.r)/(13+8*self.r))
        Kd = self.tau_del*(4/(11+2*self.r))
        return PIDGains(Kp, Ki, Kd)
    
    def generate_process_params(self) -> None:
        self.t1 = (self.t2 - self.t3*np.log(2)) / (1 - np.log(2))
        self.tau = self.t3 - self.t1
        self.tau_del = self.t1 - self.t0
        self.K = self.B / self.A
        self.r = self.tau_del / self.tau
    
    def validate(self) -> bool:
        if not all([self.A, self.B, self.t0, self.t2, self.t3]):
            return False
        if not hasattr(self, self.method):
            logging.error(f"{self.method} not a method of {self.__class__.__name__}")
            return False
        self.eval_function = getattr(self, self.method)
        return True
     
    @property
    def is_valid(self) -> bool:
        return self.valid
