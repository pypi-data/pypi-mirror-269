# auto-audio-rec

This will allow user to start the microphone after certain period of time and can stop the microphone with a button.

## Installation instructions 

```sh
pip install auto-audio-rec
```

## Usage instructions

```python
import streamlit as st

from auto_audio_rec import auto_audio_rec

value = auto_audio_rec()

st.write(value)
