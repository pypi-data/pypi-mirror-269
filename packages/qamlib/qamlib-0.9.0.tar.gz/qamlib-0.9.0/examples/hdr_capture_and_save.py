"""
Example of doing "HDR" with a trigger sequence

This uses features from Qtechnology kernel patches
"""
import qamlib
import cv2

exposures = [5000, 15000, 29000, 41000, 50000]

# Defaults to /dev/qtec/video0
cam = qamlib.Camera()

# External trigger sequence
cam.set_control("trigger_mode", 5)

trig_seq = qamlib.TriggerSequenceValue()

# Used to calculate minimal frame delay
fot = cam.get_control("frame_overhead_time")
rot = cam.get_control("read_out_time")

# Create trigger sequence with minimal delay
for i in range(len(exposures)):
    exp = exposures[i]
    if i+1 >= len(exposures):
        delay = max(exp + fot, exp + fot + rot - exposures[0])
    else:
        delay = max(exp + fot, exp + fot + rot - exposures[i+1])

    trig_seq.add_exposure(exp, exp, delay, 0)

# Set trigger sequence
cam.set_ext_control("trigger sequence", trig_seq)

# Set white balance, values from qtec-camera-gwt
cam.set_control("Red Balance", 32604)
cam.set_control("Green Balance", 16384)
cam.set_control("Blue Balance", 30802)

# Use BGR to avoid having to make OpenCV do a RGB -> BGR conversion
cam.set_format("BGR3")

# HDR Fusion merger
merge = cv2.createMergeMertens()

# Start streaming
with cam:
    images = []

    # Trigger capture, since we are in external trigger mode
    cam.set_control("Manual Trigger", 1)

    for exposure in exposures:
        name = f"exposure_{exposure}.png"

        _, img = cam.get_frame(timeout=1, buffered=True)

        cv2.imwrite(name, img)

        images.append(img)

    fusion = merge.process(images)
    cv2.imwrite("fusion.png", fusion*255) # Values after merge are in [0, 1]
