# hsr_pic_parser

## Introduction

This is a Python library for getting pictures of characters, light cones, relics and planetaries with names from [starrail.mana](https://starrail.mana.wiki/).


## Installation

```python
pip install hsr-pic-parcer
```

## Available functionality

```python
get_char_pic(name) # returns binary picture of the character and full name of the character
get_char_icon_pic(name) # returns binary icon picture of the character and full name of the character
get_cone_pic(number) # returns binary picture of the light cone and full name of the light cone
get_cone_icon_pic(number) # returns binary icon picture of the light cone and full name of the light cone
get_relic_icon_pic(number) # returns binary icon picture of the relic or planetary and full name of the relic or planetary
get_character_prydwen(name) # returns binary picture of the character from prydwen
```

## Examples

You can get picture of character using the following code:

```python
from hsr_pic_parser import get_char_pic

picture, name = get_char_pic('argenti')
```
The name of the character should be identical to the one used on [starrail.mana](https://starrail.mana.wiki/).

You can get picture and the name of the light cone:

```python
from hsr_pic_parser import get_cone_pic

picture, name = get_cone_pic(20000)
```
The code of the light cone should be equivalent to the one used on [starrail.mana](https://starrail.mana.wiki/).

```python
from hsr_pic_parser import get_relic_icon_pic

picture, name = get_relic_icon_pic(101)

def save_image_as_png(image_data, output_file_path):
    with open(output_file_path, "wb") as png_file:
        png_file.write(image_data)

save_image_as_png(picture, f"${name}.png")
```

You can get the name and the picture of the charater from prydwen [prydwen.gg](https://www.prydwen.gg/star-rail/characters/).

```python
from hsr_pic_parser import get_character_prydwen

picture, name = get_character_prydwen('argenti')
```