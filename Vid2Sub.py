from datetime import datetime

# 解析时间字符串为秒数
def parse_time_to_seconds(srt_time):
    time_format = "%H:%M:%S,%f"
    parsed_time = datetime.strptime(srt_time, time_format)
    return parsed_time.hour * 3600 + parsed_time.minute * 60 + parsed_time.second + parsed_time.microsecond / 1_000_000

# 解析 SRT 文件
def parse_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.read().strip().split("\n")
    srt_data = []
    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            time_range = lines[i + 1]
            text = lines[i + 2]
            start_time, end_time = time_range.split(" --> ")
            srt_data.append({
                "start": parse_time_to_seconds(start_time),
                "end": parse_time_to_seconds(end_time),
                "text": text
            })
    return srt_data

# 累计时间计算
def calculate_cumulative_time(srt_data, text_lines):
    cumulative_time = 0.0  # 总时间
    line_times = []  # 存储每行文字的累计时间

    for line in text_lines:
        for entry in srt_data:
            if line in entry["text"]:
                duration = entry["end"] - entry["start"]
                cumulative_time += duration
                break
        line_times.append((line, cumulative_time))

    return line_times

# 主程序
def main():
    # 提供文件路径
    srt_file_path = "素材\字幕_2024年12月09日_写了个可能不那么恰当的比喻.srt"  # 替换为你的 SRT 文件路径
    lines_file_path = "素材\文案_2024年12月09日_写了个可能不那么恰当的比喻.txt"  # 替换为你的文字行文件路径

    # 读取 SRT 文件
    srt_data = parse_srt_file(srt_file_path)

    # 读取文字文件
    with open(lines_file_path, 'r', encoding='utf-8') as file:
        text_lines = [line.strip() for line in file if line.strip()]

    # 计算每行文字的累计时间
    line_times = calculate_cumulative_time(srt_data, text_lines)

    # 输出结果
    for line, cumulative_time in line_times:
        print(f"Line: '{line}' | Cumulative Time: {cumulative_time:.3f} seconds")

if __name__ == "__main__":
    main()
