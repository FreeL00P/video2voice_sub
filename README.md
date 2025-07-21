# video2voice_sub

## 项目简介

本项目用于视频与音频的处理，包括视频分割、音频提取、字幕生成与转换、视频合并等功能，适用于内容创作、短视频剪辑、自动字幕生成等场景。

## 主要功能

- 视频分割与裁剪
- 视频音频提取
- Whisper 语音识别自动生成字幕（SRT）
- SRT 字幕转 JSON
- 统计字幕与原文案的时间
- 多视频合并并添加背景音乐
- 视频添加封面、PNG 边框（预留脚本）

## 目录结构

```
video2voice_sub/
  ├── add_cover_to_video.py           # 视频添加封面脚本（待完善）
  ├── add_png_border_to_video.py      # 视频添加PNG边框脚本（待完善）
  ├── merge_video_with_audio.py       # 多视频合并并添加音频
  ├── srt2Json.py                     # SRT字幕转JSON
  ├── str_parse_sub_time.py           # 统计字幕与原文案的时间
  ├── Vid2Sub.py                      # 视频/音频转字幕（Whisper）
  ├── video_split.py                  # 视频分割脚本
```

## 依赖环境

- Python 3.7+
- ffmpeg
- whisper
- opencc
- 其他依赖见各脚本头部注释

安装依赖（示例）：

```bash
pip install opencc-python-reimplemented
pip install git+https://github.com/openai/whisper.git
pip install ffmpeg-python
```

## 各脚本说明

- `Vid2Sub.py`  
  视频/音频转字幕（SRT），基于 OpenAI Whisper，支持简繁转换。

- `srt2Json.py`  
  将 SRT 字幕文件解析为 JSON，统计每条字幕的时间。

- `str_parse_sub_time.py`  
  统计原文案每行在字幕中的累计出现时间，输出 JSON。

- `merge_video_with_audio.py`  
  合并多个视频片段并添加背景音乐，输出新视频。

- `video_split.py`  
  按时间段分割视频，输出新视频片段。

- `add_cover_to_video.py`、`add_png_border_to_video.py`  
  预留脚本，用于视频添加封面、PNG 边框。

## 使用方法

1. **视频转字幕**
   ```bash
   python Vid2Sub.py
   ```
   按需修改脚本内的文件路径。

2. **SRT 转 JSON**
   ```bash
   python srt2Json.py
   ```

3. **统计文案时间**
   ```bash
   python str_parse_sub_time.py
   ```

4. **合并视频与音频**
   ```bash
   python merge_video_with_audio.py
   ```

5. **分割视频**
   ```bash
   python video_split.py
   ```

## 注意事项

- 路径请根据实际文件位置修改，支持相对和绝对路径。
- 需提前安装好 ffmpeg 并配置环境变量。
- Whisper 需较新显卡支持，或可用 CPU 推理（速度较慢）。 