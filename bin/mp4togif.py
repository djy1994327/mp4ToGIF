import os
import shutil
import subprocess

def add_mp4_suffix_and_copy(src_dir, dest_dir):
    # 确保目标目录存在
    os.makedirs(dest_dir, exist_ok=True)

    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dest_path = os.path.join(dest_dir, filename + '.mp4')

        # 如果目标目录中已经存在同名文件，则跳过
        if not os.path.exists(dest_path):
            shutil.copyfile(src_path, dest_path)
            print(f'复制并添加后缀: {src_path} -> {dest_path}')
        else:
            print(f'文件已存在，跳过: {dest_path}')


# 定义一个函数，用于将单个视频文件转换为GIF，使用NVENC硬件加速
def convert_video_to_gif(input_path, output_path, fps=24, bitrate='5M'):
    try:
        # 构建FFmpeg命令，使用NVENC硬件加速
        command = [
            'ffmpeg.exe',  # 使用相对路径访问ffmpeg.exe
            '-hwaccel', 'cuda',  # 使用CUDA硬件加速
            '-i', input_path,
            '-vf', f'fps={fps},format=rgb24',
            '-c:v', 'h264_nvenc',  # 使用NVENC编码器
            '-b:v', bitrate,  # 设置比特率
            '-c:v', 'gif',
            output_path
        ]

        # 运行FFmpeg命令
        subprocess.run(command, check=True)
        print(f'成功将 {input_path} 转换为 {output_path}')
    except subprocess.CalledProcessError as e:
        print(f'转换 {input_path} 时出错: {e}')


# 定义一个函数，用于批量转换目录中的所有视频文件为GIF
def batch_convert_videos_to_gif(input_directory, output_directory, fps=24, bitrate='5M'):
    # 确保输出目录存在
    os.makedirs(output_directory, exist_ok=True)

    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_directory):
        if filename.endswith('.mp4'):  # 你可以根据需要添加更多的视频文件扩展名
            input_path = os.path.join(input_directory, filename)
            output_filename = os.path.splitext(filename)[0] + '.gif'
            output_path = os.path.join(output_directory, output_filename)

            # 如果GIF文件不存在，则进行转换
            if not os.path.exists(output_path):
                convert_video_to_gif(input_path, output_path, fps, bitrate)
            else:
                print(f'GIF文件已存在，跳过: {output_path}')


if __name__ == '__main__':
    # 使用相对路径
    src_directory = '../yuanshi'  # 原始文件夹路径
    video_directory = '../video_files'  # 视频文件夹路径
    gif_directory = '../gif_files'  # 保存GIF文件的路径

    # 复制并添加后缀
    add_mp4_suffix_and_copy(src_directory, video_directory)

    # 批量将输入目录中的所有视频转换为GIF
    batch_convert_videos_to_gif(video_directory, gif_directory)