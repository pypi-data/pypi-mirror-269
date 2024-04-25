# pgpyui

pgpyui is an add-on module for pygame to create a user interface.
It has a button and text area.

## Installation

```
pip install pgpyui
```

## Usage

```python
import pgpyui
import pygame

# Initialize pygame
pygame.init()

# Create a window
window = pygame.display.set_mode((800, 600))

# Create a button
button = pgpyui.Button((100, 100), (200, 50), "Click me!", lambda: print("Button clicked!"))

# Create a text area
text_area = pgpyui.TextArea((100, 200), (200, 200), 20, 100)

# Game loop
running = True
while running:
# Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check events for button
    button.check_events(event)

    # Check events for text area
    text_area.check_events(event)

    # Draw the button and text area
    button.draw(window)
    text_area.draw(window)

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
```

## Documentation

### Button

**Parameters:**

* `position`: The position of the button.
* `size`: The size of the button.
* `text`: The text on the button.
* `function`: The function to be called when the button is clicked.
* `sprite`: A sprite to use for the button (optional).

### TextArea

**Parameters:**

* `position`: The position of the text area.
* `size`: The size of the text area.
* `font_size`: The size of the font.
* `max_symbols`: The maximum number of symbols that can be entered.
* `is_enter`: Whether or not the enter key should be allowed.
* `font`: The name of the font to use (optional).

## License

MIT