import av
import base64,uuid
from io import BytesIO
from server.utils.logUtils import log
from PIL import Image

def extractImgFromVideo(file,filename='video'):
    content = "jinhua-nj-8.mp4"
    content=file

    b64list=[]
    seq=0
    try:
        with av.open(content,mode='r') as container:
            # Signal that we only want to look at keyframes.
            stream = container.streams.video[0]
            stream.codec_context.skip_frame = "NONKEY"

            # 获取旋转元数据
            rotation = int(stream.metadata.get('rotate', 0))
            if rotation==0:
                rotation=int(stream.side_data.get('DISPLAYMATRIX',0))

            for frame in container.decode(stream):
                seq+=1
                log.info(frame)

                img=frame.to_image()

                #zhujinhua 20240725 frame 对象无旋转方法，需对 img 旋转。
                #针对本测试视频来说，metadata 无值， 取自 side_data中的值，为 -90
                #针对metadata中rotate值为90的情况是未测试的，如果为90则旋转后或许会变为朝下的图片
                if rotation!=0:
                    img=img.rotate(rotation,expand=True)

                buffer = BytesIO()
                img.save(buffer, format='jpeg', quality=80)

                base64_encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')

                # # 保存图片测试
                '''import os
                tmpdata='tmpdata/'
                if not os.path.exists(tmpdata):
                    os.makedirs(tmpdata)
                Image.open(buffer).save(f"{tmpdata}{filename}.{frame.pts}.jpg".format(frame.pts))'''

                # #待发送base64解码存图片测试
                # byte_data = base64.b64decode(base64_encoded)
                # image_data = BytesIO(byte_data)
                # Image.open(image_data).save("jpgfrombase64.{:04d}.jpg".format(frame.pts))

                # 智子接口 必须带imageUuid eventTime eventAddress， 不带就会500 JSONDecodeError
                img = {
                    "imageId": seq,
                    "imageBase64": base64_encoded,
                    "imageUuid": str(uuid.uuid4()),
                    "eventTime": "",
                    "eventAddress": "",
                }
                b64list.append(img)
    except Exception as e:
        log.error(f'av.open video catch exception:{e}')

    return b64list

