### Description
- Simple examples running Gstreamer pipeline with Python

### Installation
```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade wheel pip setuptools
pip install --upgrade --requirement requirements.txt
```

### Run examples

#### Run Gstreamer pipeline in Python using Gst.ElementFactory
```bash
python launch_pipeline/pipeline_with_factory.py
```

#### Run Gstreamer pipeline in Python using Gst.parse_launch
```bash
python launch_pipeline/pipeline_with_parse_launch.py -p "videotestsrc num-buffers=100 pattern=1 ! autovideosink"
```

#### Capture frames (np.ndarray) from any Gstreamer pipeline
```bash
python launch_pipeline/run_appsink.py -p "videotestsrc num-buffers=100 ! capsfilter caps=video/x-raw,format=RGB,width=640,height=480 ! appsink emit-signals=True"
```

#### Push images (np.ndarray) to any Gstreamer pipeline
```bash
python launch_pipeline/run_appsrc.py -p "appsrc emit-signals=True is-live=True caps=video/x-raw,format=RGB,width=640,height=480 ! queue ! videoconvert ! autovideosink"  -n 1000
```
