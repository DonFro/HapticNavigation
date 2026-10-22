from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.input.motionevent import MotionEvent
from kivy.properties import BooleanProperty


class ButtonGroup(BoxLayout):
    finger_on_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, **kwargs)
        self.button: Button = None
        self.labels: list[Label] = []

    def add_button(self, button: Button) -> None:
        """Adds a button to the Object"""
        self.button = button
        self.add_widget(button)

    def add_label(self, label: Label) -> None:
        """Adds a label to the Object"""
        self.labels.append(label)
        self.add_widget(label)

    def check_status(self, touch: MotionEvent) -> None:
        """Checks if a button is covered by a finger press"""

        # check if the finger is within the button bounds
        if self.button and self.button.collide_point(touch.x, touch.y):
            if not self.finger_on_button:
                self.finger_on_button = True
                self.button.state = "down"
            return

        # check if the finger is not within the bounds
        if self.finger_on_button:
            self.finger_on_button = False
            self.button.state = "normal"

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """Checks if a button is covered by a finger press"""
        self.check_status(touch)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """Checks if a button is covered by a finger press"""
        self.check_status(touch)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """Checks if a button is covered by a finger press"""
        if self.finger_on_button:
            self.finger_on_button = False
            self.button.state = "normal"

            self.button.dispatch("on_release")
            return True
        return super().on_touch_up(touch)
