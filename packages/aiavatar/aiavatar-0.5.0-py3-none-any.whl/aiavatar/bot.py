import asyncio
from logging import getLogger, NullHandler
import traceback
# Device
from .device import AudioDevice
# Processor
from .processors import ChatProcessor
from .processors.chatgpt import ChatGPTProcessor
# Listener
from .listeners.voicerequest import VoiceRequestListener, RequestListenerBase
from .listeners.wakeword import WakewordListener, WakewordListenerBase
# Avatar
from .speech import SpeechController
from .speech.voicevox import VoicevoxSpeechController
from .animation import AnimationController, AnimationControllerDummy
from .face import FaceController, FaceControllerDummy
from .avatar import AvatarController

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class AIAvatar:
    def __init__(
        self,
        *,
        openai_api_key: str=None,
        google_api_key: str=None,
        model: str=None,
        system_message_content: str=None,
        voicevox_speaker_id: int=46,
        input_device: int=-1,
        output_device: int=-1,
        audio_devices: AudioDevice=None,
        chat_processor: ChatProcessor=None,
        request_listener: RequestListenerBase=None,
        wakeword_listener: WakewordListenerBase=None,
        speech_controller: SpeechController=None,
        animation_controller: AnimationController=None,
        face_controller: FaceController=None,
        wakewords: list=None,
        start_voice: str=None,
        split_chars: list=None,
        language: str="ja-JP",
        verbose: bool=False
    ):
        # Audio Devices
        if audio_devices:
            self.audio_devices = audio_devices
        else:
            self.audio_devices = AudioDevice(input_device, output_device)
        logger.info(f"Input device: [{self.audio_devices.input_device}] {self.audio_devices.input_device_info['name']}")
        logger.info(f"Output device: [{self.audio_devices.output_device}] {self.audio_devices.output_device_info['name']}")

        # Chat Processor
        if chat_processor:
            self.chat_processor = chat_processor
        else:
            self.chat_processor = ChatGPTProcessor(
                api_key=openai_api_key,
                model=model or "gpt-3.5-turbo",
                system_message_content=system_message_content
            )

        # Request Listener
        if request_listener:
            self.request_listener = request_listener
        else:
            self.request_listener = VoiceRequestListener(
                google_api_key,
                volume_threshold=2000,
                device_index=self.audio_devices.input_device,
                lang=language
            )
        
        # Wakeword Listener
        if wakeword_listener:
            self.wakeword_listener = wakeword_listener
        else:
            async def _on_wakeword(text):
                await self.start_chat(request_on_start=text, skip_start_voice=start_voice is None)

            self.wakeword_listener = WakewordListener(
                api_key=google_api_key,
                wakewords=wakewords or ["こんにちは" if language == "ja-JP" else "Hello"],
                on_wakeword=_on_wakeword,
                volume_threshold=2000,
                device_index=self.audio_devices.input_device,
                lang=language,
                verbose=verbose
            )
        
        # Avatar Controller with Speech, Animation and Face
        self.avatar_controller = AvatarController(
            speech_controller or VoicevoxSpeechController(
                base_url="http://127.0.0.1:50021",
                speaker_id=voicevox_speaker_id,
                device_index=self.audio_devices.output_device
            ),
            animation_controller or AnimationControllerDummy(verbose=verbose),
            face_controller or FaceControllerDummy(verbose=verbose)
        )

        # Chat
        self.start_voice = start_voice
        self.split_chars = split_chars or ["。", "、", "？", "！", ".", ",", "?", "!"]
        self.on_turn_end = self.on_turn_end_default
        self.chat_task = None

    async def on_turn_end_default(self, request_text: str, response_text: str) -> bool:
        return False

    async def chat(self, request_on_start: str=None, skip_start_voice: bool=False):
        if not skip_start_voice:
            try:
                await self.avatar_controller.speech_controller.speak(self.start_voice)
            except Exception as ex:
                logger.error(f"Error at starting chat: {str(ex)}\n{traceback.format_exc()}")

        while True:
            request_text = ""
            response_text = ""
            try:
                if request_on_start:
                    request_text = request_on_start
                    request_on_start = None
                else:
                    request_text = await self.request_listener.get_request()
                    if not request_text:
                        break

                logger.info(f"User: {request_text}")
                logger.info("AI:")

                avatar_task = asyncio.create_task(self.avatar_controller.start())

                stream_buffer = ""
                async for t in self.chat_processor.chat(request_text):
                    stream_buffer += t
                    for spc in self.split_chars:
                        stream_buffer = stream_buffer.replace(spc, spc + "|")
                    sp = stream_buffer.split("|")
                    if len(sp) > 1: # >1 means `|` is found (splited at the end of sentence)
                        sentence = sp.pop(0)
                        stream_buffer = "".join(sp)
                        self.avatar_controller.set_text(sentence)
                        response_text += sentence
                    await asyncio.sleep(0.01)   # wait slightly in every loop not to use up CPU

                if stream_buffer:
                    self.avatar_controller.set_text(stream_buffer)
                    response_text += stream_buffer

                self.avatar_controller.set_stop()
                await avatar_task
            
            except Exception as ex:
                logger.error(f"Error at chatting loop: {str(ex)}\n{traceback.format_exc()}")

            finally:
                if await self.on_turn_end(request_text, response_text):
                    break

    async def start_chat(self, request_on_start: str=None, skip_start_voice: bool=False):
        self.stop_chat()
        self.chat_task = asyncio.create_task(self.chat(request_on_start, skip_start_voice))
        await self.chat_task

    def stop_chat(self):
        if self.chat_task is not None:
            self.chat_task.cancel()

    def start_listening_wakeword(self, wait: bool=True):
        ww_thread = self.wakeword_listener.start()
        if wait:
            ww_thread.join()
        else:
            return ww_thread
