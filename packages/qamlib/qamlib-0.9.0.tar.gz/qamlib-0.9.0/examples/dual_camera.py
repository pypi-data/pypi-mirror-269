"""Dual camera example

This is an example of using a Qtec dual head camera setup, in which the the
secondary head (/dev/qtec/video1) is triggered by the main head, in order to
have the frames from the two sensors be syncronized. The example is based on
having one RGB sensor and one SWIR sensor.
"""
import qamlib
import cv2

SAVE_DIR = "/home/root/test"


# Frame capture
def stream_on(rgb_cam, swir_cam):
    i1 = 0
    i2 = 0

    print("Starting Streaming")
    try:
        rgb_cam.start()
        swir_cam.start()
        while True:
            # Using 'buffered=True' will return the next frame in the queue
            # and throw a 'DroppedFrameException' if the queue gets filled up
            # set 'overflow_exception=False' in the Camera constructor
            # if you want to disable this exception, but then it will be necessary
            # to check for dropped frames using the sequence nr from the metadata
            rgb_meta, rgb_frame = rgb_cam.get_frame(timeout=1, buffered=True)
            swir_meta, swir_frame = swir_cam.get_frame(timeout=1, buffered=True)

            # all this sequence nr checks shouldn't be necessary
            # since we will get a 'DroppedFrameException' if frames are dropped
            # but are present to illustrate how to check for dropped frames under other circunstances

            n1 = rgb_meta.sequence - i1
            if n1 > 0:
                print(f"rgb_cam skipped {n1} frames")
                break
            i1 = rgb_meta.sequence + 1

            n2 = swir_meta.sequence - i2
            if n2 > 0:
                print(f"swir_cam skipped {n2} frames")
                break
            i2 = swir_meta.sequence + 1

            if rgb_meta.sequence != swir_meta.sequence:
                print(f"Error, heads are out of sync: {rgb_meta.sequence} != {swir_meta.sequence}")
                break

            if rgb_meta.sequence % fps == 0:
                print(f"rgb_cam: {rgb_meta.sequence}")

            if swir_meta.sequence % fps == 0:
                print(f"swir_cam: {swir_meta.sequence}")

            cv2.imwrite(f'{SAVE_DIR}/rgb_{rgb_meta.sequence:09d}.png', rgb_frame)
            cv2.imwrite(f'{SAVE_DIR}/swir_{swir_meta.sequence:09d}.png', swir_frame)
    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
    finally:
        rgb_cam.stop()
        swir_cam.stop()

    print("Done Streaming")


if __name__ == "__main__":
    # Open video capture device
    try:
        rgb_cam = qamlib.Camera("/dev/qtec/video0")
        swir_cam = qamlib.Camera("/dev/qtec/video1")
    except Exception as e:
        print(e)
        exit(-1)

    # V4l2 "Settings"
    fps = 5.0

    # Use BGR so we don't have to do the conversion to save with OpenCV
    rgb_cam.set_format("BGR3")
    rgb_cam.set_framerate(fps)

    swir_cam.set_format("GREY")
    # set swir head for "external trigger" so the other head drives it (fps)
    swir_cam.set_control("trigger mode", 1)

    img_format1 = rgb_cam.get_format()
    px_format1 = img_format1.pixelformat

    img_format2 = swir_cam.get_format()
    px_format2 = img_format2.pixelformat

    print(f"FPS: {rgb_cam.get_framerate()}")
    print(f"Frame Size: {rgb_cam.get_resolution()} , {swir_cam.get_resolution()}")
    print(f"Crop: {rgb_cam.get_crop()} , {swir_cam.get_crop()}")
    print(f"Pixel format: {img_format1} , {img_format2}")
    print("\n")

    # adjust exposure time
    rgb_cam.set_control("Exposure Time, Absolute", 5000)
    swir_cam.set_control("Exposure Time, Absolute", 5000)
    print(f"Exposure: {rgb_cam.get_control('Exposure Time, Absolute')} , {swir_cam.get_control('Exposure Time, Absolute')}")

    # restart streaming on errors
    while True:
        stream_on(rgb_cam, swir_cam)

