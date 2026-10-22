from kivy.utils import platform
from plyer import vibrator, tts as plyer_tts

if platform == "android":
    from jnius import autoclass, PythonJavaClass, java_method

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
    Locale = autoclass("java.util.Locale")

    class _TTSInitListener(PythonJavaClass):
        __javainterfaces__ = ["android/speech/tts/TextToSpeech$OnInitListener"]
        __javacontext__ = "app"

        def __init__(self, callback):
            super().__init__()
            self.callback = callback

        @java_method("(I)V")
        def onInit(self, status):
            self.callback(status)


class CoreVibrationAudioModule:
    """Manages vibration and text-to-speech.

    On Android it creates ONE speech engine at startup so speaking is fast and
    doesn't freeze the app (important when timing participants). If that
    engine fails, it falls back to plyer's tts, which you already know works.
    """

    def __init__(self, vibration_duration: float = 0.15):
        self.vibrator = vibrator
        self.isActive = False
        self.vibrationStrength = vibration_duration  # seconds
        self.ttsReady = False
        self.engine = None

        if platform == "android":
            try:
                self._listener = _TTSInitListener(self._on_tts_init)  # keep a reference
                self.engine = TextToSpeech(PythonActivity.mActivity, self._listener)
            except Exception as e:
                print(f"TTS engine setup failed, using plyer: {e}")

    def _on_tts_init(self, status) -> None:
        if status == TextToSpeech.SUCCESS:
            self.engine.setLanguage(Locale.US)
            self.ttsReady = True
            print("TTS ready")
        else:
            print(f"TTS init failed ({status}), using plyer")

    def activateVibration(self) -> None:
        self.isActive = True
        try:
            self.vibrator.vibrate(self.vibrationStrength)
        except NotImplementedError:
            print("[PC Test] Vibration ON")
        except Exception as e:
            print(f"Vibration failed: {e}")

    def deactivateVibration(self) -> None:
        self.isActive = False
        try:
            self.vibrator.cancel()
        except NotImplementedError:
            print("[PC Test] Vibration OFF")
        except Exception as e:
            print(f"Vibration cancel failed: {e}")

    def playAudio(self, text: str) -> None:
        """Speak text, interrupting anything currently being spoken"""
        try:
            if self.ttsReady:
                self.engine.speak(text, TextToSpeech.QUEUE_FLUSH, None)
            else:
                plyer_tts.speak(text)
        except NotImplementedError:
            print(f"[PC Test] Playing Audio: '{text}'")
        except Exception as e:
            print(f"TTS speak failed: {e}")
