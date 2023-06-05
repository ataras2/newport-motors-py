# turn jogging on and see what happens

import pyvisa
from newport_motors.Motors.motor import M100D
import time
import matplotlib.pyplot as plt
import numpy as np

is_short = False

motor2_port = "ASRL/dev/ttyUSB0::INSTR"
resource_manager = pyvisa.ResourceManager(visa_library="@_py")

m = M100D(motor2_port, resource_manager)


if is_short:
    jog_values = [0.5]
    jog_time = 3.0
else:
    jog_values = [0.01, 0.1, 1.0]
    jog_time = 15.0


def run_jog_exp(jv):
    m.write_str("01ST")

    m.write_str("01JAU0.0")

    print("########### start motion")
    m.write_str(f"01JAU{jv}")

    times = []
    pos = []

    start_1 = time.time()
    while time.time() - start_1 < jog_time:
        times.append(time.time())
        pos.append(m.read_pos(M100D.AXES.U))

    print("########### stop motion")
    m.write_str("01ST")

    start = time.time()
    while time.time() - start < 1.0:
        times.append(time.time())
        pos.append(m.read_pos(M100D.AXES.U))

    print("########### reset motion")
    m.set_to_zero()

    start = time.time()
    while time.time() - start < 1.0:
        times.append(time.time())
        pos.append(m.read_pos(M100D.AXES.U))

    pos = np.array(pos)
    t = np.array(times) - start_1

    return t, pos


m.write_str("01ST")
m.set_to_zero()
time.sleep(2.0)


# for jv in jog_values:
#     t, pos = run_jog_exp(jv)

#     # calculate slope
#     jogging_indicies = t < jog_time
#     slope, _ = np.polyfit(t[jogging_indicies], pos[jogging_indicies],1)

#     plt.plot(t, pos, label=f'{jv}%, slope={slope:.2e}deg/s')

# plt.legend()
# plt.xlabel('time(s)')
# plt.ylabel('position(deg)')
# plt.savefig('jog_pos_vs_t.png')


# repeat the above for many jogging values and just get the slopes
jog_vals = np.linspace(0.01, 1, 5)
slopes = np.zeros(len(jog_vals))
for i, jv in enumerate(jog_vals):
    t, pos = run_jog_exp(jv)

    jogging_indicies = t < jog_time
    slopes[i], _ = np.polyfit(t[jogging_indicies], pos[jogging_indicies], 1)

    if pos.max() > 0.7:
        raise Warning("Reached near saturation")


plt.figure()
plt.plot(jog_vals, slopes, "x")
plt.xlabel("Input jog value")
plt.ylabel("Slope (deg/s)")
# plt.show()
plt.savefig("jog_pos_vs_t.png")
