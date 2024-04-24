# tsty

**tsty** _short for "terminal style"_

A simple command-line utility for quickly switching your terminal colors and styles

## Example usage

~~~sh
# Change background to green
tsty bg green

## by default, the tsty command runs the `bg` subcommand, so this works too:
tsty green

## you can also pass in rgb values, in order of: r g b 
tsty 0 100

# Change text color — both bold and normal — to orange
tsty text orange

# change bold text color to red
tsty text red --bold

# change cursor to lavender
tsty cursor lavender

# list commands and colors
tsty list
~~~


# Current status

- Allows user to change macOS Terminal background, text, and cursor colors

## TODOS

- Add ability to switch themes
- Make it compatible with Windows Powershell/WSL 
- Make it compatible with Linux terminals
- Make separate color presets for background/cursor and text, as the former generally needs to be darker and the latter more brighter
- make aliases, e.g. `tsty t` for `tsty text`
- finish writing tests
    - throw error when user has more than 4 values for color argument
    - throw error when user has more than 1 non-numerical value for color argument
- Replace verbose-by-default with --verbose opt-in flag (i.e. deprecate --quiet)



# Installation and development notes

Install this tool using `pip`:


```sh
pip install tsty
```


## Dev and Testing


```sh
# install locally
pip install -e .


# run all tests
pytest

# run just alpha tests
pytest -m 'alpha'


# skip alpha tests
pytest -m 'not alpha'
```


