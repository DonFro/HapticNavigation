# Imported libraries
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import BooleanProperty


class ButtonGroup(BoxLayout):
    """A visual container composed of a button and optional labels (does not handle touch events)."""
    finger_on_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        """Initializes layout configuration."""
        # configure default properties
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("spacing", 10)
        super().__init__(**kwargs)

        # initialize references
        self.button: Button = None
        self.labels: list = []

    def add_button(self, button: Button) -> None:
        """Adds a button to the group."""
        self.button = button
        self.add_widget(button)

    def add_label(self, label: Label) -> None:
        """Adds a label to the group."""
        self.labels.append(label)
        self.add_widget(label)

    def contains(self, x: float, y: float) -> bool:
        """Checks if a point is within the button."""
        return self.button is not None and self.button.collide_point(x, y)


class HapticScreen(FloatLayout):
    """Oversees user inputs, swiping, and button release events across ButtonGroups."""
    __events__ = ("on_touch_start", "on_enter_group", "on_leave_group", "on_select")

    def __init__(self, **kwargs):
        """Initializes ButtonGroup tracking, current selection, and active touch."""
        super().__init__(**kwargs)
        self.groups: list = []
        self.current: ButtonGroup = None
        self._active_touch = None

    def add_group(self, group: ButtonGroup) -> None:
        """Adds a new ButtonGroup object to the HapticScreen."""
        self.groups.append(group)
        self.add_widget(group)

    def clear_groups(self) -> None:
        """Clears the current ButtonGroup objects."""
        # remove widgets from screen
        for group in self.groups:
            self.remove_widget(group)

        # reset tracking state
        self.groups = []
        self.current = None
        self._active_touch = None

    def _group_at(self, x: float, y: float) -> ButtonGroup:
        """Returns the ButtonGroup at a given coordinate, if any."""
        # check each group for collision
        for group in self.groups:
            if group.contains(x, y):
                return group
        return None
    
    def _set_current(self, group: ButtonGroup) -> None:
        """Updates the currently interacting button."""
        # ignore if group is unchanged
        if group is self.current:
            return
        
        # reset previous button state
        if self.current is not None:
            old = self.current
            old.finger_on_button = False
            old.button.state = "normal"
            self.current = None
            self.dispatch("on_leave_group", old)
        
        # activate new button state
        if group is not None:
            self.current = group
            group.finger_on_button = True
            group.button.state = "down"
            self.dispatch("on_enter_group", group)

    def on_touch_down(self, touch) -> bool:
        """Tracks starting the touch on the screen."""
        # ignore extra fingers
        if self._active_touch is not None:
            return True

        # register touch and update selection
        self._active_touch = touch.uid
        self.dispatch("on_touch_start")
        self._set_current(self._group_at(*touch.pos))
        return True

    def on_touch_move(self, touch) -> bool:
        """Tracks moving the finger on the screen."""
        # ignore non-active touches
        if touch.uid != self._active_touch:
            return True

        # update selection under finger
        self._set_current(self._group_at(*touch.pos))
        return True

    def on_touch_up(self, touch) -> bool:
        """Tracks releasing the finger off the screen."""
        # ignore non-active touches
        if touch.uid != self._active_touch:
            return True

        # reset touch state and dispatch selection
        self._active_touch = None
        selected = self._group_at(*touch.pos)
        self._set_current(None)
        self.dispatch("on_select", selected)
        return True


    # Default event handlers required by Kivy
    def on_touch_start(self):
        """Default handler for touch start."""
        pass

    def on_enter_group(self, group):
        """Default handler for entering a group."""
        pass

    def on_leave_group(self, group):
        """Default handler for leaving a group."""
        pass

    def on_select(self, group):
        """Default handler for selecting a group."""
        pass