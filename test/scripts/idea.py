from argparse import ArgumentParser

from formlabs.task_engine.client import Leash


DESCRIPTION = ""


# Thanks Chat GPT

# Collect System Response Data
# Analyze the Response Data
# Tune PID Parameters
# Iterative Loop
# Automate the Process (Optional)
# Consider Robustness
# Safety Precautions
# Final Validation


def main():
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("host", help="IP Address of intended Diesel Printer")
    parser.add_argument("--kp", type=float, default=18.0, help="Initial Kp")
    parser.add_argument("--ki", type=float, default=0.5, help="Initial Ki")
    parser.add_argument("--kd", type=float, default=0.02, help="Initial Kd")
    args = parser.parse_args()
    
    host = args.host
    kp = args.kp
    ki = args.ki
    kd = args.kd
    
    p = Leash(host=host)
    
    for idx in range(10):
        p.RunSettingsFile("Homing.json")
        p.StartNewDBLog(f"HeaterTune{idx}.sqlite")
        p.MCUStartLogging()
        p.HeaterInit(
            heater_filter_cutoff_Hz=0.1,
            heater_i_limits=[0,25],
            heater_kd=0,
            heater_ki=5,
            heater_kp=30,
            heater_max_overshoot_C=10,
            heater_sample_rate_Hz=1,
            heater_shutoff_temperature_C=100,
            heater_temperature_limits_C=[0,80],
            minimum_plausible_reading_C=1,
            reading_timeout_s=20,
            resin_filter_cutoff_Hz=0.03,
            resin_i_limits=[0,40],
            resin_kd=kd,
            resin_ki=ki,
            resin_kp=kp,
            resin_max_overshoot_C=5,
            resin_sample_rate_Hz=0.2,
            resin_shutoff_temperature_C=60,
        )
        p.HeaterSetPoint(35)
        p.MCUSetFanDutyCycle("LED", 0)
        p.MCUSetFanDutyCycle("LCD", 0)
        p.HeaterWaitToReachTemperature(
            move_positions_mm=[
                0,
                0.07498875056250001,
                0.29997750056249994,
                0.6749662505624999,
                1.1999550005625002,
                1.8749437505624995,
                3.6749212505625013,
                4.7999100005625,
                7.499887500562499,
                10.799865000562498,
                14.699842500562506,
                19.199820000562497,
                27.0747862505625,
                36.2997525005625,
                50.69970750056251,
                146.66636666666665,
                158.00631503906195,
                164.816336414062,
                171.02635778906196,
                176.636379164062,
                181.64640053906194,
                186.05642191406199,
                189.866443289062,
                193.07646466406197,
                195.68648603906198,
                197.69650741406198,
                198.47651810156202,
                199.10652878906203,
                199.58653947656197,
                199.916550164062,
                200.12663741666665,
                244.72663741666665,
                244.9198939961719,
                244.99991593367184,
                244.92995961619377,
                244.7100040536938,
                244.34004849119373,
                243.82009292869373,
                243.15013736619375,
                241.3602262411938,
                240.24027067869383,
                237.55035955369385,
                234.2604484286938,
                230.37053730369388,
                225.8806261786939,
                218.02075949119387,
                208.8108928036939,
                194.43107055369393,
                98.46785166666695,
                87.11305630655767,
                80.29296855655764,
                74.0728808065576,
                68.45279305655757,
                63.43270530655755,
                59.012617556557515,
                55.19252980655748,
                51.972442056557455,
                49.35235430655744,
                47.33226655655741,
                46.54722268155741,
                45.91217880655738,
                45.42713493155738,
                45.092091056557365,
                44.880073500000016,
                0.280073500000005,
                0.08539214360318272,
                0.0003370186031767513
            ],
            move_times_s=[
                0,
                0.01,
                0.02,
                0.03,
                0.04,
                0.05,
                0.07,
                0.08,
                0.1,
                0.12,
                0.14,
                0.16,
                0.19,
                0.22,
                0.26,
                0.5,
                0.53,
                0.55,
                0.5700000000000001,
                0.59,
                0.61,
                0.63,
                0.65,
                0.67,
                0.6900000000000001,
                0.71,
                0.72,
                0.73,
                0.74,
                0.75,
                0.76,
                2.99,
                3,
                3.0100000000000002,
                3.02,
                3.0300000000000002,
                3.04,
                3.0500000000000003,
                3.06,
                3.08,
                3.09,
                3.11,
                3.13,
                3.15,
                3.17,
                3.2,
                3.23,
                3.27,
                3.5100000000000002,
                3.54,
                3.56,
                3.58,
                3.6,
                3.62,
                3.64,
                3.66,
                3.68,
                3.7,
                3.72,
                3.73,
                3.74,
                3.75,
                3.7600000000000002,
                3.77,
                6,
                6.01,
                6.0200000000000005
            ],
            reading_timeout_s=20,
            threshold_C=31,
            warmup_timeout_s=1200
        )
        # Steady state for some time
        # Finish and collect data
        # Process data
        # Calculate/Set new PID gains
        p.HeaterShutoff()
        # Turn on cooling peripheral
        # Wait for cool


if __name__ == "__main__":
    main()