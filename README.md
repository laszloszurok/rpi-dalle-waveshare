# Intro

This script should be run on a Raspberry Pi with a Waveshare e-ink display attached to it.

The contents of the `waveshare_epd` directory were copied from here: https://github.com/waveshareteam/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd

The display model that I'm using in this script has a 7.5 inch diameter and a 640x384 resolution. To initialize and use the display I had to import the code from `waveshare_epd/epd7in5bc`. Edit `main.py` with the correct import and resolution settings if you have a different model.

Check out the `img` directory for an example image.

# Usage

## Create a virtual environment

```sh
python -m venv venv
```

## Install requirements

```sh
pip install -r requirements.txt
```

## Set the OPENAI_API_KEY environment variable

```sh
export OPENAI_API_KEY="replce-with-a-valid-api-key"
```

## Run the script
```sh
python main.py
```

You might get a warning similar to this:
```
.../venv/lib/python3.11/site-packages/gpiozero/devices.py:300: PinFactoryFallback: Falling back from lgpio: module 'lgpio' has no attribute 'SET_BIAS_DISABLE'
  warnings.warn(
```
Here is a related gpiozero github issue: https://github.com/gpiozero/gpiozero/issues/1038.
TLDR: The warning should not cause problems and can be ignored.
