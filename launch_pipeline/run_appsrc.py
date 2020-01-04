import sys
import traceback
import argparse
import typing as typ
import time

import numpy as np

from gstreamer import GstContext, GstPipeline, GstApp, Gst, GstVideo
import gstreamer.utils as utils

VIDEO_FORMAT = "RGB"
WIDTH, HEIGHT = 640, 480
GST_VIDEO_FORMAT = GstVideo.VideoFormat.from_string(VIDEO_FORMAT)

CAPS = f"video/x-raw,format={VIDEO_FORMAT},width={WIDTH},height={HEIGHT}"

# Converts list of plugins to gst-launch string
# ['plugin_1', 'plugin_2', 'plugin_3'] => plugin_1 ! plugin_2 ! plugin_3
DEFAULT_PIPELINE = utils.to_gst_string([
    f"appsrc emit-signals=True is-live=True caps={CAPS}",
    "queue",
    "videoconvert",
    "autovideosink"
])


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--pipeline", required=False,
                default=DEFAULT_PIPELINE, help="Gstreamer pipeline without gst-launch")

ap.add_argument("-n", "--num_buffers", required=False,
                default=1000, help="Num buffers to pass")

args = vars(ap.parse_args())

command = args["pipeline"]

NUM_BUFFERS = int(args['num_buffers'])
CHANNELS = utils.get_num_channels(GST_VIDEO_FORMAT)
DTYPE = utils.get_np_dtype(GST_VIDEO_FORMAT)

with GstContext():  # create GstContext (hides MainLoop)
    # create GstPipeline (hides Gst.parse_launch)
    with GstPipeline(command) as pipeline:
        appsrc = pipeline.get_by_cls(GstApp.AppSrc)[0]  # get AppSrc

        # instructs appsrc that we will be dealing with timed buffer
        appsrc.set_property("format", Gst.Format.TIME)
        appsrc.set_caps(Gst.Caps.from_string(CAPS))  # set caps
        for _ in range(NUM_BUFFERS):

            # create random np.ndarray
            array = np.random.randint(low=0, high=255,
                                      size=(HEIGHT, WIDTH, CHANNELS), dtype=DTYPE)
            # emit <push-buffer> event with Gst.Buffer
            appsrc.emit("push-buffer", utils.numpy_to_gst_buffer(array))

        # emit <end-of-stream> event
        appsrc.emit("end-of-stream")
