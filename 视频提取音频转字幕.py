import os
import ffmpeg
import whisper
import logging

# 设置日志输出，日志级别为INFO
logging.basicConfig(level=logging.INFO)

# 提取视频文件中的音频
def extract_audio(video_path, audio_path):
    try:
        # 使用ffmpeg提取音频，输出为MP3格式，设置音频通道数为2（立体声），采样率为44100
        ffmpeg.input(video_path).output(audio_path, acodec='mp3', ac=2, ar='44100').run(overwrite_output=True)
        logging.info(f"音频提取完成：{audio_path}")  # 提取成功后记录日志
    except ffmpeg.Error as e:
        # 如果音频提取过程中出错，记录错误信息
        logging.error(f"音频提取失败：{e}")
        raise  # 抛出异常以便后续处理

# 将音频转换为字幕文件
def audio_to_subtitle(audio_path, subtitle_path, model):
    try:
        logging.info("开始语音识别...")  # 提示开始语音识别过程
        result = model.transcribe(audio_path, language="zh-CN")  # 使用Whisper模型进行语音识别，指定语言为中文
        # 打开字幕文件准备写入
        with open(subtitle_path, "w", encoding="utf-8") as f:
            # 遍历识别结果的每一段
            for segment in result["segments"]:
                start_time = segment["start"]  # 获取该段音频的起始时间
                end_time = segment["end"]      # 获取该段音频的结束时间
                text = segment["text"]         # 获取该段音频的文本内容
                # 将字幕的格式写入文件：字幕编号、时间戳和文本
                f.write(f"{segment['id'] + 1}\n")
                f.write(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n")
                f.write(f"{text}\n\n")
        logging.info(f"字幕文件生成完成：{subtitle_path}")  # 成功生成字幕文件后记录日志
    except Exception as e:
        # 如果字幕生成过程中出错，记录错误信息
        logging.error(f"字幕生成失败：{e}")
        raise  # 抛出异常以便后续处理

# 时间戳格式化函数，将秒数转换为 SRT 字幕要求的时间格式 (hh:mm:ss,SSS)
def format_timestamp(seconds):
    milliseconds = int((seconds % 1) * 1000)  # 获取毫秒部分
    seconds = int(seconds)                    # 获取秒部分
    minutes, seconds = divmod(seconds, 60)    # 将秒转换为分钟和秒
    hours, minutes = divmod(minutes, 60)      # 将分钟转换为小时和分钟
    # 格式化输出时间戳，保留三位毫秒
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# 主流程
if __name__ == "__main__":
    # 设置输入的视频文件路径
    video_file = r"素材\【工厂招聘😊【平哥】】#工厂平哥 #搞笑段子 出门务工的朋友们，自己的贵重物品要好好保管哦，如有困难平哥可以帮助一二.mp4"  # 输入视频文件
    # 设置音频输出路径（与视频文件同名，但扩展名为 .mp3）
    audio_file = os.path.splitext(video_file)[0] + ".mp3"
    # 设置字幕输出路径（与视频文件同名，但扩展名为 .srt）
    subtitle_file = os.path.splitext(video_file)[0] + ".srt"

    # 加载 Whisper 模型
    model = whisper.load_model("base")
    logging.info("模型加载完成")  # 加载完成后记录日志

    # 提取音频
    extract_audio(video_file, audio_file)

    # 转换音频为字幕
    audio_to_subtitle(audio_file, subtitle_file, model)
