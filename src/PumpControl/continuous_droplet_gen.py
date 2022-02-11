import new_era
import serial
import time

ser = serial.Serial('/dev/ttyUSB1',19200,timeout=.1)

if __name__ == "__main__":
    pump1_rates = [44,42,40,38,36,34,32,30]
    pump1_rate_idx = 0

    pumps = new_era.find_pumps(ser)
    for idx in pumps:
        print("Pump #%d is online"%idx)
    assert(len(pumps) != 0)

    syringes = {'0.1 ml Hamilton':'1.47',
                '0.25 ml Hamilton':'2.30',
                '1 ml Hamilton':'4.61',
                '5 ml Hamilton':'10.30',
                '10 ml Hamilton':'14.60'}

    dia1 = syringes["10 ml Hamilton"]
    dia2 = syringes["5 ml Hamilton"]
    dia3 = syringes["5 ml Hamilton"]

    assert(new_era.set_diameter(ser,pumps[0],dia1) == 0)
    assert(new_era.set_diameter(ser,pumps[1],dia2) == 0)
    assert(new_era.set_diameter(ser,pumps[2],dia3) == 0)


    print("Start pumping. S5011 rate from 44 to 30 uL/hr with a step size of 2 uL/hr, each run for 2 min.")

    while (pump1_rate_idx != 10):
        rate = [pump1_rates[pump1_rate_idx], 60 - pump1_rates[pump1_rate_idx], 12000]

        # set flow rates
        assert(new_era.set_rates(ser,rate) == 0)

        # read flow rate, assure setting completion
        actual_rates = new_era.get_rates(ser,pumps)
        print("Cycle %d: Pumping rate: Pump1: %s uL/hr, Pump2: %s uL/hr"%(pump1_rate_idx,actual_rates[pumps[0]],actual_rates[pumps[1]]))

        # start pumps
        assert(new_era.run_all(ser) == 0)
        time.sleep(120)

        # stop pumps
        assert(new_era.stop_all(ser) == 0)
        
        pump1_rate_idx += 1

        
        


