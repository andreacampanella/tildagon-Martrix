import app
from events.input import Buttons, BUTTON_TYPES
import random
from tildagonos import tildagonos  # Import the LEDs module

class MatrixApp(app.App):
    def __init__(self):
        # Initialize button states and drops for matrix effect
        self.button_states = Buttons(self)
        self.columns = 30
        self.drops = [0 for _ in range(self.columns)]
        self.trail_length = 10  # Length of the trail
        self.characters = [[None for _ in range(240)] for _ in range(self.columns)]
        self.rainbow_mode = False  # Flag to toggle rainbow mode
        self.speed = 1  # Initial speed of the falling symbols

    def update(self, delta):
        # Check if the CANCEL button is pressed to minimize the app
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        
        # Toggle rainbow mode when button "CONFIRM" is pressed
        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.rainbow_mode = not self.rainbow_mode
            self.button_states.clear()
            self.update_leds()
        
        # Increase speed when button "UP" is pressed
        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.speed = min(self.speed + 0.1, 10)
            self.button_states.clear()
        
        # Decrease speed when button "DOWN" is pressed
        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.speed = max(self.speed - 0.1, 0.1)
            self.button_states.clear()

    def update_leds(self):
        # Define LGBT flag colors
        lgbt_colors = [
            (255, 0, 0),    # Red
            (255, 128, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (74, 0, 130)    # Violet
        ]
        
        # Set LEDs to the respective colors
        if self.rainbow_mode:
            for i, color in enumerate(lgbt_colors):
                tildagonos.leds[i + 1] = color  # Set each LED to a color from the LGBT flag
        else:
            for i in range(1, 13):
                tildagonos.leds[i] = (0, 0, 0)  # Turn off LEDs when not in rainbow mode

    def draw(self, ctx):
        ctx.save()
        # Fill the background with black color
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        # Set the font for drawing text
        ctx.font = ctx.get_font_name(5)
        
        # Define LGBT flag colors
        lgbt_colors = [
            (1, 0, 0),    # Red
            (1, 0.5, 0),  # Orange
            (1, 1, 0),    # Yellow
            (0, 1, 0),    # Green
            (0, 0, 1),    # Blue
            (0.29, 0, 0.51)  # Violet
        ]
        
        # Draw the matrix effect by iterating over columns
        for i in range(len(self.drops)):
            char = chr(random.randint(33, 126))  # Generate a random character
            x = i * 8 - 120  # Calculate x position
            y = int(self.drops[i] * 16 * self.speed) - 120  # Calculate y position with speed factor
            
            # Store the character for trail effect
            self.characters[i][int(self.drops[i] % 240)] = char
            
            # Draw the trail
            for j in range(self.trail_length):
                trail_y = y - j * 16
                if -120 <= trail_y <= 120:
                    brightness = 1 - j / self.trail_length  # Adjust brightness for trail
                    if self.rainbow_mode:
                        color = lgbt_colors[int((self.drops[i] - j) % len(lgbt_colors))]
                        ctx.rgb(color[0] * brightness, color[1] * brightness, color[2] * brightness)
                    else:
                        ctx.rgb(0, brightness, 0)
                    
                    if self.characters[i][int((self.drops[i] - j) % 240)]:
                        ctx.move_to(x, trail_y).text(self.characters[i][int((self.drops[i] - j) % 240)])
            
            # Reset the drop if it goes off the screen with some randomness
            if y > 120 and random.random() > 0.975:
                self.drops[i] = 0
            self.drops[i] += self.speed
        
        ctx.restore()

__app_export__ = MatrixApp
