# Imported libraries
from kivy.utils import platform
from plyer import vibrator, tts as plyer_tts

# Android TTS configuration
if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
    Locale = autoclass("java.util.Locale")

    class _TTSInitListener(PythonJavaClass):
        """Java listener interface for Android TTS initialization."""
        __javainterfaces__ = ["android/speech/tts/TextToSpeech$OnInitListener"]
        __javacontext__ = "app"

        def __init__(self, callback):
            """Initializes the listener with a status callback."""
            super().__init__()
            self.callback = callback

        @java_method("(I)V")
        def onInit(self, status):
            """Triggers the callback upon TTS engine initialization."""
            self.callback(status)


class CoreVibrationAudioModule:
    """Manages device vibration and text-to-speech output."""

    def __init__(self):
        """Initializes hardware interfaces and the Android TTS engine."""
        # initialize default state
        self.vibrator = vibrator
        self.isActive = False
        self.ttsReady = False
        self.engine = None

        # setup android tts engine
        if platform == "android":
            try:
                self._listener = _TTSInitListener(self._on_tts_init)  # keep reference
                self.engine = TextToSpeech(PythonActivity.mActivity, self._listener)
            except Exception as e:
                print(f"TTS engine setup failed, using plyer: {e}")

    def _on_tts_init(self, status) -> None:
        """Configures TTS language upon successful engine initialization."""
        # set language on success
        if status == TextToSpeech.SUCCESS:
            self.engine.setLanguage(Locale.US)
            self.ttsReady = True
            print("TTS ready")
            
        # log initialization failure
        else:
            print(f"TTS init failed ({status}), using plyer")

    def activateVibration(self) -> None:
        """Activates continuous vibration until explicitly cancelled."""
        self.isActive = True
        
        # start continuous vibration loop
        try:
            self.vibrator.pattern(pattern=[0, 1], repeat=0)
        except NotImplementedError:
            print("[PC Test] Vibration ON")
            
        # fallback to single long pulse
        except Exception as e:
            print(f"Continuous vibration failed, using long pulse: {e}")
            try:
                self.vibrator.vibrate(60)
            except Exception as e2:
                print(f"Vibration failed: {e2}")

    def deactivateVibration(self) -> None:
        """Stops any active device vibration."""
        self.isActive = False
        
        # cancel active vibration
        try:
            self.vibrator.cancel()
        except NotImplementedError:
            print("[PC Test] Vibration OFF")
        except Exception as e:
            print(f"Vibration cancel failed: {e}")

    def playAudio(self, text: str) -> None:
        """Synthesizes and plays speech from text, interrupting active audio."""
        # speak using active engine or fallback
        try:
            if self.ttsReady:
                self.engine.speak(text, TextToSpeech.QUEUE_FLUSH, None)
            else:
                plyer_tts.speak(text)
                
        # handle desktop testing and errors
        except NotImplementedError:
            print(f"[PC Test] Playing Audio: '{text}'")
        except Exception as e:
            print(f"TTS speak failed: {e}")