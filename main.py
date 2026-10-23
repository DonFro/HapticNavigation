# Imported libraries
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

# Imported modules
import coreVibrationAudioModule as cva
import experimentModule as exp
from uiElementModule import ButtonGroup, HapticScreen

# Configuration
CONDITIONS = {
    "haptic_audio": "Haptic + Audio",
    "audio_only": "Audio only",
}


class MyApp(App):
    """Main application class managing state, UI transitions, and trial logic."""

    def build(self) -> FloatLayout:
        """Initializes the main application layout and triggers the start screen."""
        self.coreVibrationAudio = cva.CoreVibrationAudioModule()
        self.root_screen = FloatLayout()
        self.show_start_screen()
        return self.root_screen

    def on_pause(self) -> bool:
        """Deactivates vibration during application pause state."""
        self.coreVibrationAudio.deactivateVibration()
        return True
    
    def show_start_screen(self) -> None:
        """Renders the initial condition selection interface."""
        # clear previous ui
        self.root_screen.clear_widgets()

        # setup main container
        box = BoxLayout(orientation="vertical", padding=40, spacing=20)
        box.add_widget(Label(text="Haptic Navigation Study\nChoose a condition to start",
                             halign="center", font_size="22sp"))

        # generate condition buttons
        for key, name in CONDITIONS.items():
            btn = Button(text=name, font_size="22sp")
            btn.bind(on_release=lambda _b, k=key: self.start_session(k))
            box.add_widget(btn)

        # display interface
        self.root_screen.add_widget(box)

    def show_rating_screen(self) -> None:
        """Renders the comfort rating interface for the current level."""
        # clear previous ui
        self.root_screen.clear_widgets()
        self.rating_question = "How comfortable was this level? 1 is very uncomfortable, 5 is very comfortable."
        screen = HapticScreen()

        # setup screen
        screen.add_widget(Label(
            text=f"Level {self.level} complete\n\nHow comfortable was this level?\n"
                 "1 = very uncomfortable   5 = very comfortable",
            halign="center", font_size="20sp",
            size_hint=(1, 0.4), pos_hint={"center_x": 0.5, "top": 1}))

        # generate rating buttons
        for rating in range(1, 6):
            group = ButtonGroup(size_hint=(0.17, 0.3),
                                pos_hint={"center_x": 0.1 + 0.2 * (rating - 1), "center_y": 0.35})
            group.add_button(Button(text=str(rating), font_size="32sp"))
            group.rating = rating
            screen.add_group(group)

        # bind touch events
        screen.bind(on_enter_group=self.on_rating_enter,
                    on_leave_group=self.on_leave_group,
                    on_select=self.on_rating_select)
        self.rating_active = True

        # display interface and play audio
        self.root_screen.add_widget(screen)
        self.coreVibrationAudio.playAudio(f"Level {self.level} complete. {self.rating_question}")

    def on_rating_enter(self, _screen, group: ButtonGroup) -> None:
        """Triggers feedback when interacting with a rating button."""
        # ignore if inactive
        if not self.rating_active:
            return
        
        # trigger haptic and audio feedback
        if exp.RATING_SCREEN_VIBRATES:
            self.coreVibrationAudio.activateVibration()
        self.coreVibrationAudio.playAudio(group.button.text)

    def on_rating_select(self, _screen, group) -> None:
        """Processes the submitted rating and advances the state."""
        # ignore if inactive
        if not self.rating_active:
            return
        
        # handle empty selection
        if group is None:
            self.coreVibrationAudio.playAudio(self.rating_question)
            return
        
        # process valid rating
        self.rating_active = False
        self.coreVibrationAudio.deactivateVibration()
        self.coreVibrationAudio.playAudio(f"You chose {group.rating}")
        self.submit_rating(group.rating)

    def show_end_screen(self) -> None:
        """Displays final session metrics and completion options."""
        # clear previous ui
        self.root_screen.clear_widgets()

        # setup results display
        box = BoxLayout(orientation="vertical", padding=40, spacing=20)
        box.add_widget(Label(
            text=f"Session complete\nSession ID: {self.logger.session_id}\n\n"
                 f"Results saved in:\n{self.user_data_dir}",
            halign="center", font_size="18sp"))

        # generate restart button
        again = Button(text="New session", font_size="22sp", size_hint_y=0.3)
        again.bind(on_release=lambda _b: self.show_start_screen())
        box.add_widget(again)

        # display interface and play audio
        self.root_screen.add_widget(box)
        self.coreVibrationAudio.playAudio("Session complete. Thank you.")


    def start_session(self, condition: str) -> None:
        """Initializes trial progression for the selected condition."""
        # configure session state
        self.condition = condition
        self.logger = exp.ResultLogger(self.user_data_dir, condition)
        self.level = 0

        # setup interaction screen
        self.haptic_screen = HapticScreen()
        self.haptic_screen.bind(
            on_touch_start=self.on_touch_start,
            on_enter_group=self.on_enter_group,
            on_leave_group=self.on_leave_group,
            on_select=self.on_select,
        )

        # begin sequence
        self.start_next_level()

    def start_next_level(self) -> None:
        """Prepares trial data for the next difficulty level."""
        # advance level and check completion
        self.level += 1
        if self.level > exp.NUM_LEVELS:
            self.show_end_screen()
            return
        
        # configure new level trials
        self.trials = exp.build_level_trials(self.level)
        self.trial_index = 0

        # update interface
        self.root_screen.clear_widgets()
        self.root_screen.add_widget(self.haptic_screen)
        self.start_trial(announce_level=True)

    def start_trial(self, announce_level: bool = False) -> None:
        """Configures UI and tracking variables for a single trial."""
        # reset screen state
        self.trial = self.trials[self.trial_index]
        self.haptic_screen.clear_groups()

        # render target buttons
        for label, slot in self.trial["layout"].items():
            cx, cy = exp.SLOTS[slot]
            group = ButtonGroup(size_hint=exp.BUTTON_SIZE,
                                pos_hint={"center_x": cx, "center_y": cy})
            group.add_button(Button(text=label, font_size="22sp"))
            self.haptic_screen.add_group(group)

        # initialize counters
        self.trial_active = True
        self.prompt_time = time.perf_counter()
        self.first_touch_time = None
        self.wrong_selections = 0
        self.empty_lifts = 0
        self.buttons_entered = 0

        # set timeout and audio prompt
        self.timeout_event = Clock.schedule_once(self.on_trial_timeout, exp.TRIAL_TIMEOUT_S)
        prefix = f"Level {self.level}. " if announce_level else ""
        self.coreVibrationAudio.playAudio(f"{prefix}Find {self.trial['target']}")

    def finish_trial(self, completed: bool) -> None:
        """Logs performance metrics and transitions out of the current trial."""
        # stop active tracking
        self.trial_active = False
        self.timeout_event.cancel()
        self.coreVibrationAudio.deactivateVibration()

        # calculate duration
        now = time.perf_counter()
        from_touch = "" if self.first_touch_time is None else round(now - self.first_touch_time, 3)

        # log metrics
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

        # schedule next trial
        Clock.schedule_once(self.next_trial, exp.PAUSE_BETWEEN_TRIALS_S)

    def next_trial(self, _dt) -> None:
        """Evaluates condition limits to dispatch the next trial or rating screen."""
        self.trial_index += 1
        if self.trial_index >= len(self.trials):
            self.show_rating_screen()
        else:
            self.start_trial()

    def on_trial_timeout(self, _dt) -> None:
        """Handles failure state when trial exceeds permitted duration."""
        if self.trial_active:
            self.coreVibrationAudio.playAudio("Time is up. Moving on.")
            self.finish_trial(completed=False)

    def submit_rating(self, rating: int) -> None:
        """Logs the user rating and delays transition to the next level."""
        self.logger.log_rating(self.level, rating)
        Clock.schedule_once(lambda _dt: self.start_next_level(), exp.PAUSE_BETWEEN_TRIALS_S)
        
    def on_touch_start(self, _screen) -> None:
        """Records interaction commencement timestamp."""
        if self.trial_active and self.first_touch_time is None:
            self.first_touch_time = time.perf_counter()

    def on_enter_group(self, _screen, group: ButtonGroup) -> None:
        """Executes feedback protocols when touch enters button bounds."""
        # ignore if inactive
        if not self.trial_active:
            return
        
        # trigger feedback
        self.buttons_entered += 1
        if self.condition == "haptic_audio":
            self.coreVibrationAudio.activateVibration()
        self.coreVibrationAudio.playAudio(group.button.text)

    def on_leave_group(self, _screen, group: ButtonGroup) -> None:
        """Terminates vibration when touch exits button bounds."""
        self.coreVibrationAudio.deactivateVibration()

    def on_select(self, _screen, group) -> None:
        """Evaluates touch release location against the trial target."""
        # ignore if inactive
        if not self.trial_active:
            return
        
        target = self.trial["target"]

        # handle empty release
        if group is None:
            self.empty_lifts += 1
            self.coreVibrationAudio.playAudio(f"Find {target}")
            
        # handle correct selection
        elif group.button.text == target:
            self.coreVibrationAudio.playAudio("Correct")
            self.finish_trial(completed=True)
            
        # handle incorrect selection
        else:
            self.wrong_selections += 1
            self.coreVibrationAudio.playAudio(f"Wrong. Find {target}")

# Execution entry point
if __name__ == "__main__":
    MyApp().run()