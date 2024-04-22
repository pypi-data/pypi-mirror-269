# PyGerm
PyGerm is a free, open-source, cross-platform library built for the development of 2D, component based games using Python. It is built on top of the Simple DirectMedia Layer library (SDL2) and other popular libraries to abstract away the most tedious tasks of game development. With PyGerm, you can focus on building your game, your way, without worrying about cross-platform support, physics, and more.

To get started, check out the [installation](#installation) instructions below, or dive into the [documentation](#documentation) to learn more about the features and capabilities of PyGerm.

## Why PyGerm?
PyGerm is the first Python-based game engine that delivers a true component-based architecture. This means that logic that you write once can always be reused, no matter where it needs to go. Coupled with powerful integrated functions to handle entity management, physics, and rendering, PyGerm is the perfect choice for developers who want to focus on building their game, not the engine.  

## Installation
1. Install the PyGerm library using pip:
```bash
$ pip install pygerm
```

2. Import the library in your Python code and get started!
```python
import pygerm

game = pygerm.Game()
game.game_config = pygerm.GameConfig(game_title="My New Game")
game.rendering_config = pygerm.RenderingConfig(x_resolution=800, y_resolution=600)

game.run()
```

Keep in mind, Python 3.7 or higher is required to use PyGerm.

## Documentation
The full documentation for PyGerm can be found [here](https://pygerm.readthedocs.io/en/latest/).

## Examples

## Building from Source
If you are interested in modifying or building this library from source, you can clone the repository and build it using the following steps:

1. Clone the repository:
```bash
$ git clone $REPO_URL
```

2. Install the required dependencies:
```bash
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer
```

3. Use the build.sh script to quickly build and mount the library:
```bash
$ ./build.sh
```

or...

4. Build the library using the setup.py:
```bash
python setup.py bdist_wheel
```

5. Mount the wheel file:
```bash
pip install dist/${wheel_name}.whl
```