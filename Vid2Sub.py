import os
import ffmpeg
import whisper
import logging
from opencc import OpenCC

# 设置日志输出
logging.basicConfig(level=logging.INFO)

# 设置 OpenCC 转换器
cc = OpenCC("t2s")


class VideoAudioProcessor:
    @staticmethod
    def extract_audio(video_path, audio_path):
        """
        提取视频文件中的音频。
        :param video_path: 视频文件路径
        :param audio_path: 输出音频文件路径
        """
        try:
            ffmpeg.input(video_path).output(audio_path, acodec='mp3', ac=2, ar='44100').run(overwrite_output=True)
            logging.info(f"音频提取完成：{audio_path}")
        except ffmpeg.Error as e:
            logging.error(f"音频提取失败：{e}")
            raise


class AudioToSubtitle:
    def __init__(self, model=None, language="zh"):
        """
        初始化字幕生成器。
        :param model: Whisper 模型实例
        :param language: 语音识别语言
        """
        self.model = model or whisper.load_model("base")
        self.language = language

    def transcribe(self, audio_path, subtitle_path):
        """
        将音频文件转换为字幕。
        :param audio_path: 音频文件路径
        :param subtitle_path: 输出字幕文件路径
        """
        try:
            logging.info("开始语音识别...")
            result = self.model.transcribe(audio_path, language=self.language)
            with open(subtitle_path, "w", encoding="utf-8") as f:
                for segment in result["segments"]:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = cc.convert(segment["text"])
                    f.write(f"{segment['id'] + 1}\n")
                    f.write(f"{self.format_timestamp(start_time)} --> {self.format_timestamp(end_time)}\n")
                    f.write(f"{text}\n\n")
            logging.info(f"字幕文件生成完成：{subtitle_path}")
        except Exception as e:
            logging.error(f"字幕生成失败：{e}")
            raise

    @staticmethod
    def format_timestamp(seconds):
        """
        格式化时间戳为 SRT 格式。
        :param seconds: 秒数
        :return: 格式化的时间戳
        """
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def main(video_file=None, audio_file=None, save_path=None):
    """
    主流程函数。
    :param video_file: 视频文件路径（可选）
    :param audio_file: 音频文件路径（可选）
    :param save_path: 保存路径，必须提供
    """
    if not save_path:
        logging.error("保存路径(save_path)必须提供！")
        return

    if not video_file and not audio_file:
        logging.error("必须提供视频文件或音频文件中的至少一个！")
        return

    try:
        # 确保保存路径存在
        os.makedirs(save_path, exist_ok=True)
        
        # 设置默认音频文件路径（如果未提供音频文件路径）
        if video_file and not audio_file:
            audio_file = os.path.splitext(video_file)[0] + ".mp3"

        # 设置字幕文件路径
        file_base_name = os.path.splitext(os.path.basename(video_file or audio_file))[0]
        subtitle_file = os.path.join(save_path, file_base_name + ".srt")

        # 如果提供了视频文件，则提取音频
        if video_file:
            logging.info(f"从视频文件提取音频：{video_file}")
            VideoAudioProcessor.extract_audio(video_file, audio_file)

        # 转换音频为字幕
        logging.info(f"开始生成字幕文件：{subtitle_file}")
        subtitle_generator = AudioToSubtitle()
        subtitle_generator.transcribe(audio_file, subtitle_file)

        logging.info(f"字幕生成完成，保存路径：{subtitle_file}")
    except Exception as e:
        logging.error(f"处理过程中发生错误：{e}")

if __name__ == "__main__":
    # 示例：从视频生成字幕
    video_input = r"素材\1.mp4"  # 视频文件路径
    main(video_file=video_input)

   # 示例：直接从音频生成字幕
    audio_input = r"素材\文案转音频_写了个可能不那么恰当的比喻.mp3"  # 音频文件路径
    main(audio_file=audio_input)