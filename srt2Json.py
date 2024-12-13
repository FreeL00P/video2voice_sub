import re
import json
import os

def parse_srt(file_path):
    """解析SRT文件并计算每条字幕的占用时间"""
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_text = file.read()
    
    subtitles = []
    pattern = r"(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+(.*?)\s*(?=\d+\s+\d{2}:\d{2}:\d{2},\d{3}|$)"
    matches = re.findall(pattern, srt_text, re.DOTALL)
    
    for match in matches:
        index = int(match[0])
        start_time = match[1]
        end_time = match[2]
        content = match[3].strip().replace("\n", " ")
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)
        duration = end_seconds - start_seconds
        subtitles.append({
            "index": index,
            "start_time": start_time,
            "end_time": end_time,
            "duration": round(duration, 3),  # 保留三位小数
            "content": content,
        })
    return subtitles

def time_to_seconds(time_str):
    """将时间字符串转换为秒数"""
    hours, minutes, seconds = time_str.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

def save_results_to_json(subtitles, output_file):
    """将解析结果保存到JSON文件"""
    # 获取保存目录
    output_dir = os.path.dirname(output_file)
    # 如果目录不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存到JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(subtitles, file, ensure_ascii=False, indent=4)

def main():
    # 输入SRT文件路径
    srt_file_path = "素材\\字幕_2024年12月09日_写了个可能不那么恰当的比喻.srt"  # 替换为你的SRT文件路径
    subtitle_file = os.path.splitext(os.path.basename(srt_file_path))[0]  # 获取文件名（不带扩展名）
    
    # 构建输出JSON文件路径
    output_file_path = f"字幕转JSON\\{subtitle_file}.json"
    
    # 解析SRT文件
    subtitles = parse_srt(srt_file_path)
    print(subtitles)
    # 保存结果到JSON文件
    save_results_to_json(subtitles, output_file_path)
    
    print(f"字幕解析结果已保存到: {output_file_path}")

if __name__ == "__main__":
    main()
