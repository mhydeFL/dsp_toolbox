import os
from project_manager.config import Config


def main():
    """
    Simple example to demonstrate how the Config object can be used
    to load a YAML file and access fields using DOT notation.
    
    Sample file in config/sample.yaml
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config = Config().from_file("sample.yaml")

    controller = config.controller
    log = config.log
    plotting = config.plotting
    
    kp = controller.initial_gains.kp
    ki = controller.initial_gains.ki
    kd = controller.initial_gains.kd
    
    print(f"Kp: {kp} Ki: {ki} Kd: {kd}")
    
    print(log)
    print(plotting)


if __name__ == "__main__":
    main()