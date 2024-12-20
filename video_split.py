import subprocess
import os

def split_video(input_video, output_folder, output_filename, start_time_seconds, end_time_seconds):
    """
    使用 ffmpeg 切分视频并保留原格式编码，支持以秒为单位的时间
    :param input_video: 原视频文件路径
    :param output_folder: 保存剪辑后视频的文件夹路径
    :param output_filename: 剪辑后视频的文件名（不带扩展名）
    :param start_time_seconds: 剪辑开始时间（秒数）
    :param end_time_seconds: 剪辑结束时间（秒数）
    :return: 切分后视频的保存路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 设置输出视频路径
    output_path = os.path.join(output_folder, f"{output_filename}.mp4")

    # 使用 ffmpeg 命令切分视频
    command = [
        'ffmpeg',
        '-ss', str(start_time_seconds),  # 剪辑开始时间（秒）
        '-i', input_video,               # 输入视频文件
        '-to', str(end_time_seconds),    # 剪辑结束时间（秒）
        '-c', 'copy',                    # 复制视频和音频流，不重新编码
        '-y',                            # 自动覆盖输出文件
        output_path                      # 输出文件路径
    ]

    try:
        # 执行命令
        subprocess.run(command, check=True)
        print(f"视频剪辑成功，保存路径：{output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"视频剪辑失败: {e}")
        return None


input_video = r"D:\内容工厂\视频\视频素材库_示例\传统水洗石\【视频】_4_【12.38】秒.mp4"  # 原视频文件路径
output_folder = "output"  # 保存剪辑后视频的文件夹路径
output_filename = "output_video"        # 剪辑后视频的文件名（不带扩展名）
start_time = "0"                 # 开始剪辑时间，格式为 hh:mm:ss
end_time = "0.9"                   # 结束剪辑时间，格式为 hh:mm:ss

# 调用函数进行视频切分
output_video_path = split_video(input_video, output_folder, output_filename, start_time, end_time)
print(output_video_path)
