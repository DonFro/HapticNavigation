# Imported Libraries
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

# Imported Modules
import coreVibrationAudioModule as cva
import experimentModule as exp
from uiElementModule import ButtonGroup, HapticScreen

CONDITIONS = {
    "haptic_audio": "Haptic + Audio",
    "audio_only": "Audio only",
}


class MyApp(App):
    def build(self) -> FloatLayout:
        self.coreVibrationAudio = cva.CoreVibrationAudioModule()
        self.root_screen = FloatLayout()
        self.show_start_screen()
        return self.root_screen

    def on_pause(self) -> bool:
        return True  # don't lose the session if the screen turns off

    # ================= Start / end / rating screens (facilitator) =================
    def show_start_screen(self) -> None:
        self.root_screen.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=40, spacing=20)
        box.add_widget(Label(text="Haptic Navigation Study\nChoose a condition to start",
                             halign="center", font_size="22sp"))
        for key, name in CONDITIONS.items():
            btn = Button(text=name, font_size="22sp")
            btn.bind(on_release=lambda _b, k=key: self.start_session(k))
            box.add_widget(btn)
        self.root_screen.add_widget(box)

    def show_rating_screen(self) -> None:
        self.root_screen.clear_widgets()
        question = "How comfortable was this level?"
        box = BoxLayout(orientation="vertical", padding=40, spacing=15)
        box.add_widget(Label(
            text=f"Level {self.level} complete\n\n{question}\n"
                 "1 = very uncomfortable   5 = very comfortable",
            halign="center", font_size="20sp"))
        row = BoxLayout(spacing=10)
        for rating in range(1, 6):
            btn = Button(text=str(rating), font_size="28sp")
            btn.bind(on_release=lambda _b, r=rating: self.submit_rating(r))
            row.add_widget(btn)
        box.add_widget(row)
        self.root_screen.add_widget(box)
        self.coreVibrationAudio.playAudio(
            f"Level {self.level} complete. {question} Pick a number from 1 to 5.")

    def show_end_screen(self) -> None:
        self.root_screen.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=40, spacing=20)
        box.add_widget(Label(
            text=f"Session complete\nSession ID: {self.logger.session_id}\n\n"
                 f"Results saved in:\n{self.user_data_dir}",
            halign="center", font_size="18sp"))
        again = Button(text="New session", font_size="22sp", size_hint_y=0.3)
        again.bind(on_release=lambda _b: self.show_start_screen())
        box.add_widget(again)
        self.root_screen.add_widget(box)
        self.coreVibrationAudio.playAudio("Session complete. Thank you.")

    # ================= Session flow =================
    def start_session(self, condition: str) -> None:
        self.condition = condition
        self.logger = exp.ResultLogger(self.user_data_dir, condition)
        self.level = 0
        self.haptic_screen = HapticScreen()
        self.haptic_screen.bind(
            on_touch_start=self.on_touch_start,
            on_enter_group=self.on_enter_group,
            on_leave_group=self.on_leave_group,
            on_select=self.on_select,
        )
        self.start_next_level()

    def start_next_level(self) -> None:
        self.level += 1
        if self.level > exp.NUM_LEVELS:
            self.show_end_screen()
            return
        self.trials = exp.build_level_trials(self.level)
        self.trial_index = 0
        self.root_screen.clear_widgets()
        self.root_screen.add_widget(self.haptic_screen)
        self.start_trial(announce_level=True)

    def start_trial(self, announce_level: bool = False) -> None:
        self.trial = self.trials[self.trial_index]
        self.haptic_screen.clear_groups()

        for label, slot in self.trial["layout"].items():
            cx, cy = exp.SLOTS[slot]
            group = ButtonGroup(size_hint=exp.BUTTON_SIZE,
                                pos_hint={"center_x": cx, "center_y": cy})
            group.add_button(Button(text=label, font_size="22sp"))
            self.haptic_screen.add_group(group)

        # per-trial counters
        self.trial_active = True
        self.prompt_time = time.perf_counter()
        self.first_touch_time = None
        self.wrong_selections = 0
        self.empty_lifts = 0
        self.buttons_entered = 0
        self.timeout_event = Clock.schedule_once(self.on_trial_timeout, exp.TRIAL_TIMEOUT_S)

        prefix = f"Level {self.level}. " if announce_level else ""
        self.coreVibrationAudio.playAudio(f"{prefix}Find {self.trial['target']}")

    def finish_trial(self, completed: bool) -> None:
        self.trial_active = False
        self.timeout_event.cancel()
        self.coreVibrationAudio.deactivateVibration()
        now = time.perf_counter()
        from_touch = "" if self.first_touch_time is None else round(now - self.first_touch_time, 3)
        self.logger.log_trial({
            "level": self.level,
            "num_buttons": self.level,
            "trial": self.trial["trial"],
            "target": self.trial["target"],
            "target_slot": self.trial["layout"][self.trial["target"]],
            "completed": completed,
            "time_from_prompt_s": round(now - self.prompt_time, 3),
            "time_from_first_touch_s": from_touch,
            "wrong_selections": self.wrong_selections,
            "empty_lifts": self.empty_lifts,
            "buttons_entered": self.buttons_entered,
        })
        Clock.schedule_once(self.next_trial, exp.PAUSE_BETWEEN_TRIALS_S)

    def next_trial(self, _dt) -> None:
        self.trial_index += 1
        if self.trial_index >= len(self.trials):
            self.show_rating_screen()
        else:
            self.start_trial()

    def on_trial_timeout(self, _dt) -> None:
        if self.trial_active:
            self.coreVibrationAudio.playAudio("Time is up. Moving on.")
            self.finish_trial(completed=False)

    def submit_rating(self, rating: int) -> None:
        self.logger.log_rating(self.level, rating)
        self.start_next_level()

    # ================= Touch events from HapticScreen =================
    def on_touch_start(self, _screen) -> None:
        if self.trial_active and self.first_touch_time is None:
            self.first_touch_time = time.perf_counter()

    def on_enter_group(self, _screen, group: ButtonGroup) -> None:
        if not self.trial_active:
            return
        self.buttons_entered += 1
        if self.condition == "haptic_audio":
            self.coreVibrationAudio.activateVibration()
        self.coreVibrationAudio.playAudio(group.button.text)

    def on_leave_group(self, _screen, group: ButtonGroup) -> None:
        self.coreVibrationAudio.deactivateVibration()

    def on_select(self, _screen, group) -> None:
        if not self.trial_active:
            return
        target = self.trial["target"]
        if group is None:
            self.empty_lifts += 1
            self.coreVibrationAudio.playAudio(f"Find {target}")
        elif group.button.text == target:
            self.coreVibrationAudio.playAudio("Correct")
            self.finish_trial(completed=True)
        else:
            self.wrong_selections += 1
            self.coreVibrationAudio.playAudio(f"Wrong. Find {target}")


if __name__ == "__main__":
    MyApp().run()
