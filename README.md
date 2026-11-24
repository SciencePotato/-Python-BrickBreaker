# -Python-BrickBreaker
## Creators 
> Skydaz123  
> Cheng Qiu  
> SciencePotato

## Game boundaries

Move the paddle with Left/Right or A/D. Its position is clamped after movement.
Clearing the bricks or losing the ball ends the loop before Pygame shuts down,
so no rendering continues after `pygame.quit()`. Close the window to stop early.
There is no in-game restart key; launch the script again for a fresh game.

`python3 -m unittest -v test_boundaries` uses mocked Pygame and audio APIs.
It checks both paddle edges and clean win/loss termination without opening a
window or playing audio.
