import os
import subprocess

def merge_videos_with_audio(video_paths, audio_path, save_dir, save_name):
    """
    使用 ffmpeg 合并视频并添加背景音乐。

    参数：
        video_paths (list): 视频文件路径列表。
        audio_path (str): 背景音乐文件路径。
        save_dir (str): 保存目录路径。
        save_name (str): 保存文件名（包含扩展名，如 output.mp4）。

    返回：
        str: 最终保存的视频路径。
    """
    try:
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 临时合并文件列表
        temp_file = os.path.join(save_dir, "input_videos.txt")
        with open(temp_file, "w", encoding="utf-8") as f:
            for path in video_paths:
                if os.path.exists(path):
                    print(f"加载视频: {path}")
                    f.write(f"file '{os.path.abspath(path)}'\n")
                else:
                    print(f"视频文件不存在: {path}")

        # 检查是否有可用的视频文件
        if os.stat(temp_file).st_size == 0:
            raise ValueError("没有可用的视频文件！")

        # 最终保存路径
        output_path = os.path.join(save_dir, save_name)

        # 合并视频
        print("正在合并视频...")
        merged_video_path = os.path.join(save_dir, "merged_video.mp4")
        merge_command = [
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", temp_file,
            "-c", "copy", merged_video_path
        ]
        subprocess.run(merge_command, check=True)

        # 检查背景音乐文件
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"背景音乐文件不存在: {audio_path}")

        # 添加背景音乐
        print("添加背景音乐...")
        final_command = [
            "ffmpeg", "-i", merged_video_path, "-i", audio_path, "-c:v", "copy",
            "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
        ]
        subprocess.run(final_command, check=True)

        print("视频合并完成!")
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 执行失败: {e}")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)


# 示例调用
if __name__ == "__main__":
    # 假设 video_list 是某个函数的返回值
    video_list = [
        "D:\内容工厂\视频\\1\\1.mp4",
        "D:\内容工厂\视频\\1\\2.mp4",
        "D:\内容工厂\视频\\1\\3.mp4",
        "D:\内容工厂\视频\\1\\4.mp4",
        "D:\内容工厂\视频\\1\\5.mp4",
        "D:\内容工厂\视频\\1\\6.mp4",
    ]  # 替换为你的实际视频路径，注意路径分隔符

    # 使用 os.path.normpath 规范化路径
    video_list = [os.path.normpath(path) for path in video_list]

    background_music = r"C:\Users\Administrator\Desktop\视频提取音频转字幕\video2voice_sub\素材\音频_2024年12月09日_写了个可能不那么恰当的比喻.mp3"  # 替换为你的实际背景音乐路径
    save_directory = os.path.abspath("./")  # 保存目录使用绝对路径
    save_filename = "final_output.mp4"  # 保存文件名

    result_path = merge_videos_with_audio(video_list, background_music, save_directory, save_filename)

    if result_path:
        print(f"视频成功保存到: {result_path}")
    else:
        print("视频合并失败！")
