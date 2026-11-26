---
name: portrait-voice-video
description: 把单张角色图和已有配音做成口播镜头，适用于写实、宣传画和插画的角色试镜，以及讲解照片如何开口的短片。包含 Apple Silicon 本地 FlashHead Lite 的安装、出片和验收方法。
---

# 单图口播与多角色试镜

先确定人物及画风，再写一句话大纲，最后拆镜头。只需一个说话镜头时，直接用现成肖像和原声。多角色短片可以让两位角色说同一句话，复用同一音频文件，观众就能听出换的是脸。将动物或夸张画风先做一两秒测试，近看眼睛、牙齿和下颌；必要时用专门的动物动画或按声音驱动嘴部形变，并如实标记实际做法。

## 本地生成

适用 Apple Silicon Mac、可用的 Metal、Python 3、ffmpeg 和 ffprobe。首次下载约 2.9 GB 到 scripts/.runtime，后续可离线。先进入本技能目录。

```sh
python3 scripts/setup.py
python3 scripts/generate.py portrait.png narration.wav --size 320 --out preview
python3 scripts/generate.py portrait.png narration.wav --size 512 --out final
ffprobe -v error -show_entries stream=codec_name,width,height,duration,nb_frames -of json final/presenter.mp4
```

脚本调用 audio.cpp 的 SoulX-FlashHead Lite 四步 Q8 模型，输出带原声的方形 MP4。保留音频里的停顿；屏幕字幕和其他镜头跟着原声时间走。长稿按句意切镜，只生成角色实际出镜的时段。用新的输出目录保存每次试镜。若日志提示无法创建 Metal 队列，检查当前执行环境能否使用 Mac GPU。

逐段看开口和收口，核对持续时间、读音、头发与轮廓是否稳定。把片段放回最终的小窗或全屏画面再判断效果。希望角色在特定台词上抬手时，另选有动作驱动的底片或可控骨骼；可以用已有声音，动作单独对齐重音。对知识短片，将问题的答案直接演给观众看，例如从同一段嘴部视频抽几帧，先停格，再连续播放。

下载器固定版本并校验 SHA-256。发布或再分发时按所用组件核对许可，Lite VAE 与主模型的许可不同。[FlashHead 模型卡与组件许可](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B#component-licenses) · [推理程序与版本](https://github.com/0xShug0/audio.cpp/releases/tag/v0.9.6)
