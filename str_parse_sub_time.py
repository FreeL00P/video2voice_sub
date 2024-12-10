import json
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# 读取字幕数据（subtitle_data）
def load_subtitle_data(file_path):
    """
    从指定路径加载字幕数据（JSON格式）。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        subtitle_data = json.load(f)
    return subtitle_data

# 读取原始文本（original_text）
def load_original_text(file_path):
    """
    从指定路径加载原始文本（TXT格式），每行文本为一项。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = [line.strip() for line in f.readlines()]
    return original_text

# 计算每行文本的累计时间
def calculate_total_duration(subtitle_data, original_text):
    """
    计算每行文本的累计时间，返回包含文本和时间的列表。
    """
    result = []
    for line in original_text:
        total_duration = 0
        logging.info(f"处理文本行: '{line}'")

        # 遍历字幕数据，计算每行文本的累计时间
        for subtitle in subtitle_data:
            if subtitle["content"] in line:
                total_duration += subtitle["duration"]  # 累加时间

        result_entry = {"text": line, "total_duration": total_duration}
        result.append(result_entry)
        logging.info(f"累计时间: {total_duration:.3f}秒\n")
    
    return result

# 保存结果到JSON文件
def save_results_to_json(results, output_file):
    """
    将结果保存到指定的JSON文件。
    """
    output_dir = os.path.dirname(output_file)  # 获取输出目录
    if not os.path.exists(output_dir):  # 如果目录不存在，创建目录
        os.makedirs(output_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    logging.info(f"结果已保存到 {output_file}")

# 主函数
def main(subtitle_file, original_text_file, output_file):
    """
    主函数：加载数据，计算时间，保存结果。
    """
    subtitle_data = load_subtitle_data(subtitle_file)  # 加载字幕数据
    original_text = load_original_text(original_text_file)  # 加载原始文本
    results = calculate_total_duration(subtitle_data, original_text)  # 计算累计时间
    save_results_to_json(results, output_file)  # 保存结果到JSON文件

# 配置文件路径
subtitle_file = '字幕转JSON\\字幕_2024年12月09日_写了个可能不那么恰当的比喻.json'  # 字幕数据文件路径
original_text_file = '素材\\文案_2024年12月09日_写了个可能不那么恰当的比喻.txt'  # 原始文本文件路径
result_file = os.path.splitext(os.path.basename(subtitle_file))[0] 
output_file = f'处理结果\{result_file}_result.json'  # 结果输出文件路径

# 调用主函数
if __name__ == "__main__":
    main(subtitle_file, original_text_file, output_file)
