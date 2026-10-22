from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import BooleanProperty


class ButtonGroup(BoxLayout):
    """A button plus optional labels.

    This is now only a visual container. All touch handling happens in
    HapticScreen, so several groups on one screen don't fight over touches.
    """
    finger_on_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("spacing", 10)
        super().__init__(**kwargs)
        self.button: Button = None
        self.labels: list = []

    def add_button(self, button: Button) -> None:
        """Adds a button to the group"""
        self.button = button
        self.add_widget(button)

    def add_label(self, label: Label) -> None:
        """Adds a label to the group"""
        self.labels.append(label)
        self.add_widget(label)

    def contains(self, x: float, y: float) -> bool:
        """True if the point is inside this group's button"""
        return self.button is not None and self.button.collide_point(x, y)


class HapticScreen(FloatLayout):
    """Explore-by-touch screen that manages every ButtonGroup on it.

    Slide your finger around: entering a button fires on_enter_group,
    leaving fires on_leave_group. Lifting the finger fires on_select with
    the group under the finger, or None if it was lifted on empty space.

    Events:
        on_touch_start()          finger first touches the screen
        on_enter_group(group)
        on_leave_group(group)
        on_select(group_or_None)
    """
    __events__ = ("on_touch_start", "on_enter_group", "on_leave_group", "on_select")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.groups: list = []
        self.current: ButtonGroup = None
        self._active_touch = None  # only track one finger at a time

    # ---------- group management ----------
    def add_group(self, group: ButtonGroup) -> None:
        self.groups.append(group)
        self.add_widget(group)

    def clear_groups(self) -> None:
        for group in self.groups:
            self.remove_widget(group)
        self.groups = []
        self.current = None
        self._active_touch = None

    # ---------- touch handling ----------
    def _group_at(self, x: float, y: float):
        for group in self.groups:
            if group.contains(x, y):
                return group
        return None

    def _set_current(self, group) -> None:
        if group is self.current:
            return
        if self.current is not None:
            old = self.current
            old.finger_on_button = False
            old.button.state = "normal"
            self.current = None
            self.dispatch("on_leave_group", old)
        if group is not None:
            self.current = group
            group.finger_on_button = True
            group.button.state = "down"
            self.dispatch("on_enter_group", group)

    def on_touch_down(self, touch) -> bool:
        if self._active_touch is not None:
            return True  # ignore extra fingers
        self._active_touch = touch.uid
        self.dispatch("on_touch_start")
        self._set_current(self._group_at(*touch.pos))
        return True  # don't pass to child Buttons; we handle everything

    def on_touch_move(self, touch) -> bool:
        if touch.uid != self._active_touch:
            return True
        self._set_current(self._group_at(*touch.pos))
        return True

    def on_touch_up(self, touch) -> bool:
        if touch.uid != self._active_touch:
            return True
        self._active_touch = None
        selected = self._group_at(*touch.pos)
        self._set_current(None)
        self.dispatch("on_select", selected)
        return True

    # default event handlers (required by Kivy)
    def on_touch_start(self): pass
    def on_enter_group(self, group): pass
    def on_leave_group(self, group): pass
    def on_select(self, group): pass
