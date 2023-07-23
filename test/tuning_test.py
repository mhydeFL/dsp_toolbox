from dsp_toolbox.optimization.heuristics import ZNTuning, CCTuning


def test_controller_options():
    p = ZNTuning(1, 1, "P")
    pi = ZNTuning(1, 1, "PI")
    pid = ZNTuning(1, 1, "PID")
    pid_overshoot = ZNTuning(1, 1, "PIDOvershoot")
    pid_no_overshoot= ZNTuning(1, 1, "PIDNoOvershoot")
    
    assert p() is not None
    assert pi() is not None
    assert pid() is not None
    assert pid_overshoot() is not None
    assert pid_no_overshoot() is not None
    
    p = CCTuning(1, 1, 1, 1, 1, "P")
    pi = CCTuning(1, 1, 1, 1, 1, "PI")
    pid = CCTuning(1, 1, 1, 1, 1, "PID")

    assert p() is not None
    assert pi() is not None
    assert pid() is not None

def main():
    test_controller_options()


if __name__ == "__main__":
    main()
