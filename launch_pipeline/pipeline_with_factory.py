import traceback
import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject


# Initializes Gstreamer, it's variables, paths
Gst.init(sys.argv)


def on_message(bus, message, loop):
    mtype = message.type
    """
        Gstreamer Message Types and how to parse
        https://lazka.github.io/pgi-docs/Gst-1.0/flags.html#Gst.MessageType
    """
    if mtype == Gst.MessageType.EOS:
        print("End of stream")
        
    elif mtype == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(err, debug)     
    elif mtype == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print(err, debug)             
        
    return True 

# Gst.Pipeline https://lazka.github.io/pgi-docs/Gst-1.0/classes/Pipeline.html
pipeline = Gst.Pipeline()

# Creates element by name
# https://lazka.github.io/pgi-docs/Gst-1.0/classes/ElementFactory.html#Gst.ElementFactory.make
src_name = "my_video_test_src"
src = Gst.ElementFactory.make("videotestsrc", name="my_video_test_src")
src.set_property("num-buffers", 50)
src.set_property("pattern", "ball")


sink = Gst.ElementFactory.make("gtksink")

pipeline.add(src, sink)

src.link(sink)

assert src == pipeline.get_by_name(src_name)

# https://lazka.github.io/pgi-docs/Gst-1.0/classes/Bus.html
bus = pipeline.get_bus() 

# allow bus to emit messages to main thread 
bus.add_signal_watch()

# Add handler to specific signal
# https://lazka.github.io/pgi-docs/GObject-2.0/classes/Object.html#GObject.Object.connect
bus.connect("message", on_message, None)

# Start pipeline
pipeline.set_state(Gst.State.PLAYING)

# Init GObject loop to handle Gstreamer Bus Events
loop = GObject.MainLoop()

try:
    loop.run()
except:
    traceback.print_exc()
    
# Stop Pipeline
pipeline.set_state(Gst.State.NULL)