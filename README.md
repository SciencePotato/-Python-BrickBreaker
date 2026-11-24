# -Python-BrickBreaker
## Creators 
> Skydaz123  
> Cheng Qiu  
> SciencePotato

## Startup

Use Python 3 with Pygame installed (`python3 -m pip install pygame`; Windows:
`py -m pip install pygame`). Run `python3 main.py` from this directory, or
`python3 /path/to/repository/main.py` from another directory.

Keep both bundled WAV files beside `main.py`:

- `acoustic-guitars-ambient-uplifting-background-music-for-videos-5642.wav`
- `drum-hitnormal.wav`

Audio paths are resolved from the script's directory, not the working directory.
The game needs a desktop display and an available audio device; it is not a
headless application. Move with Left/Right or A/D and close the window to quit.

`python3 -m unittest -v test_resources` mocks Pygame, verifies both bundled paths,
and does not open a display or play audio.
