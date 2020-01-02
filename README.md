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
```bash
python launch_pipeline/pipeline_with_factory.py
```

```bash
python launch_pipeline/pipeline_with_parse_launch.py -p "videotestsrc num-buffers=100 pattern=1 ! autovideosink"
```
