import numpy as np
import torch
from ovos_config.locale import get_valid_languages
from ovos_plugin_manager.templates.transformers import AudioLanguageDetector
from ovos_utils.xdg_utils import xdg_data_home
from speech_recognition import AudioData
from speechbrain.inference import EncoderClassifier


class SpeechBrainLangClassifier(AudioLanguageDetector):
    def __init__(self, config=None):
        config = config or {}
        super().__init__("ovos-audio-transformer-plugin-speechbrain-langdetect", 10, config)
        model = self.config.get("model") or "speechbrain/lang-id-commonlanguage_ecapa"
        if self.config.get("use_cuda"):
            self.engine = EncoderClassifier.from_hparams(source=model, savedir=f"{xdg_data_home()}/speechbrain",
                                                         run_opts={"device": "cuda"})
        else:
            self.engine = EncoderClassifier.from_hparams(source=model, savedir=f"{xdg_data_home()}/speechbrain")

    @staticmethod
    def audiochunk2array(audio_data):
        # Convert buffer to float32 using NumPy
        audio_as_np_int16 = np.frombuffer(audio_data, dtype=np.int16)
        audio_as_np_float32 = audio_as_np_int16.astype(np.float32)

        # Normalise float32 array so that values are between -1.0 and +1.0
        max_int16 = 2 ** 15
        data = audio_as_np_float32 / max_int16
        return torch.from_numpy(data).float()

    def signal2probs(self, signal):
        probs, _, _, _ = self.engine.classify_batch(signal)
        probs = torch.softmax(probs[0], dim=0)
        labels = self.engine.hparams.label_encoder.decode_ndim(range(len(probs)))
        results = {}
        for prob, label in sorted(zip(probs, labels), reverse=True):
            results[label.split(":")[0]] = prob.item()

        # the labels are the language name in english, map to lang-codes
        langmap = {'Arabic': 'ar-SA',
                   'Basque': 'eu-ES',
                   'Breton': 'br-FR',
                   'Catalan': 'ca-ES',
                   'Chinese_China': 'zh-CN',
                   'Chinese_Hongkong': 'zh-HK',
                   'Chinese_Taiwan': 'zh-TW',
                   'Chuvash': 'cv-RU',
                   'Czech': 'cs-CZ',
                   'Dhivehi': 'dv-MV',
                   'Dutch': 'nl-NL',
                   'English': 'en-US',
                   'Esperanto': 'eo',
                   'Estonian': 'et-EE',
                   'French': 'fr-FR',
                   'Frisian': 'fy-NL',
                   'Georgian': 'ka-GE',
                   'German': 'de-DE',
                   'Greek': 'el-GR',
                   'Hakha_Chin': 'cnh',
                   'Indonesian': 'id-ID',
                   'Interlingua': 'ia',
                   'Italian': 'it-IT',
                   'Japanese': 'ja-JP',
                   'Kabyle': 'kab-DZ',
                   'Kinyarwanda': 'rw-RW',
                   'Kyrgyz': 'ky-KG',
                   'Latvian': 'lv-LV',
                   'Maltese': 'mt-MT',
                   'Mongolian': 'mn-MN',
                   'Persian': 'fa-IR',
                   'Polish': 'pl-PL',
                   'Portuguese': 'pt-PT',
                   'Romanian': 'ro-RO',
                   'Romansh_Sursilvan': 'rm-Sursilvan',
                   'Russian': 'ru-RU',
                   'Sakha': 'sah-RU',
                   'Slovenian': 'sl-SI',
                   'Spanish': 'es-ES',
                   'Swedish': 'sv-SE',
                   'Tamil': 'ta-IN',
                   'Tatar': 'tt-RU',
                   'Turkish': 'tr-TR',
                   'Ukrainian': 'uk-UA',
                   'Welsh': 'cy-GB'}

        return {langmap[k].lower(): v for k, v in results.items()}

    # plugin api
    def detect(self, audio_data: bytes, valid_langs=None):
        if isinstance(audio_data, AudioData):
            audio_data = audio_data.get_wav_data()

        signal = self.audiochunk2array(audio_data)

        valid = valid_langs or get_valid_languages()
        if len(valid) == 1:
            # no classification needed
            return audio_data, {}

        probs = self.signal2probs(signal)
        valid2 = [l.split("-")[0] for l in valid]
        probs = [(k, v) for k, v in probs.items()
                 if k.split("-")[0] in valid2]
        total = sum(p[1] for p in probs) or 1
        probs = [(k, v / total) for k, v in probs]

        lang, prob = max(probs, key=lambda k: k[1])
        return lang, prob


if __name__ == "__main__":
    from speech_recognition import Recognizer, AudioFile

    jfk = "/home/miro/PycharmProjects/ovos-stt-plugin-fasterwhisper/jfk.wav"
    with AudioFile(jfk) as source:
        audio = Recognizer().record(source)

    s = SpeechBrainLangClassifier()
    lang, prob = s.detect(audio.get_wav_data(), valid_langs=["en-us", "es-es"])
    print(lang, prob)
    # en-us 0.5979952496320518
