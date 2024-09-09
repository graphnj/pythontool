import os
import av
from av.video.frame import VideoFrame

def images_to_video(image_folder, output_file, fps=1):
    # 获取图片文件列表
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))])

    # 计算视频的总帧数
    total_frames = len(image_files) * 2 * fps

    # 创建视频容器
    with av.open(output_file, 'w') as container:
        # 获取第一张图片的尺寸
        first_image_path = os.path.join(image_folder, image_files[0])
        first_image = av.open(first_image_path).next().to_image()
        width, height = first_image.size

        # 添加视频流
        stream = container.add_stream('h264', rate=fps)
        stream.width = width
        stream.height = height

        # 遍历所有图片
        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)

            # 打开图片
            with av.open(image_path) as frame_container:
                frame = frame_container.next().to_image()

            # 为每张图片创建两个帧（每个帧持续一秒）
            for _ in range(2 * fps):
                # 将 PIL.Image 转换为 av.VideoFrame
                video_frame = VideoFrame.from_pil_image(frame, format='rgb24')
                packet = stream.encode(video_frame)
                if packet:
                    container.mux(packet)

        # 写入尾部数据
        for packet in stream.encode(None):
            container.mux(packet)

if __name__ == "__main__":
    # 设置图片文件夹路径和输出视频文件名
    image_folder = '预置图片/暴露垃圾'
    output_file = 'video_baolulaji.mp4'

    # 调用函数
    images_to_video(image_folder, output_file, fps=1)