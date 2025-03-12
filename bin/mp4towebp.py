import os
import shutil
import subprocess

def add_mp4_suffix_and_copy(src_dir, dest_dir):
    # 保持原样，无需修改
    os.makedirs(dest_dir, exist_ok=True)
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dest_path = os.path.join(dest_dir, filename + '.mp4')
        if not os.path.exists(dest_path):
            shutil.copyfile(src_path, dest_path)
            print(f'复制并添加后缀: {src_path} -> {dest_path}')
        else:
            print(f'文件已存在，跳过: {dest_path}')

def convert_video_to_webp(input_path, output_path, quality=80, fps=24, loop=0, lossless=False):
    try:
        # 核心修改：构建WebP转换命令
        command = [
            'ffmpeg.exe',
            '-hwaccel', 'cuda',      # 保持CUDA硬件加速
            '-i', input_path,
            '-vf', f'fps={fps},scale=iw:-1:flags=lanczos',  # 保持原比例，使用高质量缩放
            '-c:v', 'libwebp',       # 使用WebP编码器
            '-quality', str(quality), # 质量参数（0-100）
            '-loop', str(loop),      # 循环次数（0=无限循环）
            '-preset', 'default',   # 编码预设（default, picture, photo, drawing, icon, text）
            '-lossless' if lossless else '',  # 无损模式（谨慎使用，体积极大）
            '-y',                   # 覆盖输出文件（可选）
            output_path
        ]
        # 过滤空参数（例如当lossless=False时）
        command = [arg for arg in command if arg != '']

        subprocess.run(command, check=True)
        print(f'成功转换: {input_path} -> {output_path}')
    except subprocess.CalledProcessError as e:
        print(f'转换失败: {input_path} - 错误: {e}')

def batch_convert_videos_to_webp(input_directory, output_directory, quality=80, fps=24, loop=0, lossless=False):
    os.makedirs(output_directory, exist_ok=True)
    for filename in os.listdir(input_directory):
        if filename.endswith('.mp4'):
            input_path = os.path.join(input_directory, filename)
            output_filename = os.path.splitext(filename)[0] + '.webp'
            output_path = os.path.join(output_directory, output_filename)
            if not os.path.exists(output_path):
                convert_video_to_webp(input_path, output_path, quality, fps, loop, lossless)
            else:
                print(f'文件已存在，跳过: {output_path}')

if __name__ == '__main__':
    src_directory = '../yuanshi'
    video_directory = '../video_files'
    webp_directory = '../webp_files'  # 修改输出目录为WebP

    add_mp4_suffix_and_copy(src_directory, video_directory)
    batch_convert_videos_to_webp(video_directory, webp_directory)