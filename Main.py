from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock
import random


class RainDrop:
    def __init__(self, label, speed):
        self.label = label
        self.speed = speed


class CalculatorApp(App):

    def build(self):

        root = FloatLayout()

        # Very dark background
        with root.canvas.before:
            Color(0.005, 0.01, 0.005, 1)
            self.bg = Rectangle(
                pos=root.pos,
                size=root.size
            )

        root.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

        # Matrix rain container
        self.rain = FloatLayout(
            size_hint=(1, 1)
        )

        root.add_widget(self.rain)

        # Create Matrix rain
        self.drops = []

        for i in range(25):

            x = random.uniform(0, 0.98)
            y = random.uniform(0, 1)

            label = Label(
                text=random.choice(["0", "1"]),
                font_size=random.randint(14, 24),
                color=(0.0, 0.8, 0.15, 0.35),
                size_hint=(None, None),
                size=(dp(25), dp(25)),
                pos_hint={"x": x, "y": y}
            )

            self.rain.add_widget(label)

            speed = random.uniform(0.08, 0.25)

            self.drops.append(
                RainDrop(label, speed)
            )

        # Main calculator
        main = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10),
            size_hint=(0.94, 0.90),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.48
            }
        )

        # Display
        self.display = TextInput(
            text="",
            font_size=40,
            readonly=True,
            multiline=False,
            halign="right",
            foreground_color=(0.2, 1, 0.3, 1),
            background_color=(0.01, 0.04, 0.015, 0.95),
            cursor_color=(0.2, 1, 0.3, 1),
            size_hint_y=0.23
        )

        main.add_widget(self.display)

        # Buttons
        buttons = GridLayout(
            cols=4,
            spacing=dp(7),
            size_hint_y=0.77
        )

        button_list = [
            "C", "⌫", "(", ")",
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        for text in button_list:

            if text == "C":
                bg_color = (0.25, 0.02, 0.02, 1)
                text_color = (1, 0.3, 0.3, 1)

            elif text == "=":
                bg_color = (0.02, 0.35, 0.08, 1)
                text_color = (0.3, 1, 0.4, 1)

            elif text in ["/", "*", "-", "+"]:
                bg_color = (0.03, 0.20, 0.07, 1)
                text_color = (0.2, 1, 0.3, 1)

            else:
                bg_color = (0.025, 0.08, 0.035, 1)
                text_color = (0.4, 1, 0.45, 1)

            button = Button(
                text=text,
                font_size=29,
                background_normal="",
                background_color=bg_color,
                color=text_color
            )

            button.bind(on_press=self.button_click)
            buttons.add_widget(button)

        main.add_widget(buttons)

        root.add_widget(main)

        # Start Matrix animation
        Clock.schedule_interval(
            self.update_rain,
            1 / 30
        )

        return root

    def update_rain(self, dt):

        for drop in self.drops:

            label = drop.label

            x, y = label.pos_hint["x"], label.pos_hint["y"]

            y -= drop.speed * dt

            if y < -0.05:

                y = 1.05
                x = random.uniform(0, 0.98)

                label.text = random.choice(["0", "1"])
                label.font_size = random.randint(14, 24)

                label.pos_hint = {
                    "x": x,
                    "y": y
                }

            else:

                label.pos_hint = {
                    "x": x,
                    "y": y
                }

    def update_bg(self, instance, value):

        self.bg.pos = instance.pos
        self.bg.size = instance.size

    # --------------------------------
    # RESULT GLITCH ANIMATION
    # --------------------------------

    def result_animation(self, final_result):

        # Final answer ki length
        length = len(final_result)

        # Glitch characters
        symbols = ["0", "1"]

        # Total glitch frames
        steps = 8

        for i in range(steps):

            def change_display(dt, i=i):

                if i < steps - 1:

                    glitch = ""

                    # Final answer jitne characters
                    for j in range(length):
                        glitch += random.choice(symbols)

                    self.display.text = glitch

                else:

                    # Last frame mein real answer
                    self.display.text = final_result

            Clock.schedule_once(
                change_display,
                i * 0.06
            )

    # --------------------------------
    # BUTTON FUNCTION
    # --------------------------------

    def button_click(self, instance):

        value = instance.text

        if value == "C":

            self.display.text = ""

        elif value == "⌫":

            self.display.text = self.display.text[:-1]

        elif value == "=":

            try:

                result = eval(self.display.text)

                # Glitch animation ke baad result
                self.result_animation(str(result))

            except:

                self.display.text = "Error"

        else:

            self.display.text += value


CalculatorApp().run()
