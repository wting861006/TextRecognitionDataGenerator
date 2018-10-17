"""
     create pictures look like your real scence
     this project mainly use to some bakground ,some text
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import glob
import numpy as np
import os
import cv2


# 从文字库中随机选择n个字符
def sto_choice_from_info_str(info_str):
    x = random.randint(0, len(info_str)-1)

    random_word = info_str[x]

    return random_word


def random_word_color():
    font_color_choice = [[54, 54, 54], [54, 54, 54], [105, 105, 105]]
    font_color = random.choice(font_color_choice)

    noise = np.array([random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)])
    font_color = (np.array(font_color) + noise).tolist()

    # print('font_color：',font_color)

    return tuple(font_color)



# 生成一张图片
def create_an_image(bground_path, width, height):
    bground_list = os.listdir(bground_path)
    bground_choice = random.choice(bground_list)
    bground = Image.open(bground_path + bground_choice)
    # print('background:',bground_choice)
    # print(bground.size[0],bground.size[1])
    x, y = random.randint(0, bground.size[0] - width), random.randint(0, bground.size[1] - height)
    bground = bground.crop((x, y, x + width, y + height))
    return bground


# 模糊函数
def darken_func(image):
    # .SMOOTH
    # .SMOOTH_MORE
    # .GaussianBlur(radius=2 or 1)
    # .MedianFilter(size=3)
    # 随机选取模糊参数
    filter_ = random.choice(
        [ImageFilter.SMOOTH,
         ImageFilter.SMOOTH_MORE,
         ImageFilter.GaussianBlur(radius=1.3)]
    )
    image = image.filter(filter_)
    # image = img.resize((290,32))

    return image


# 随机选取文字贴合起始的坐标, 根据背景的尺寸和字体的大小选择
def random_x_y(bground_size, font_size):
    width, height = bground_size
    # print(bground_size)
    # 为防止文字溢出图片，x，y要预留宽高
    x = random.randint(0, width - font_size * 10)
    y = random.randint(0, int((height - font_size) / 4))

    return x, y


def random_font_size():
    #font_size = random.randint(24, 27)
    font_size = random.randint(12, 27)
    return font_size


def random_font(font_path):
    font_list = os.listdir(font_path)
    random_font = random.choice(font_list)

    return font_path + random_font


def padding_data_gen(save_path, num, file, info_str):
    # 随机选取10个字符
    random_word = sto_choice_from_info_str(info_str)
    # 生成一张背景图片，已经剪裁好，宽高为32*280
    raw_image = create_an_image('./pictures/', 280, 32)

    # 随机选取字体大小
    font_size = random_font_size()
    # 随机选取字体
    font_name = random_font('./font/')
    # 随机选取字体颜色
    font_color = random_word_color()

    # 随机选取文字贴合的坐标 x,y
    draw_x, draw_y = random_x_y(raw_image.size, font_size)

    # 将文本贴到背景图片
    font = ImageFont.truetype(font_name, font_size)
    draw = ImageDraw.Draw(raw_image)
    draw.text((draw_x, draw_y), random_word, fill=font_color, font=font)

    # 随机选取作用函数和数量作用于图片
    # random_choice_in_process_func()
    raw_image = darken_func(raw_image)
    # raw_image = raw_image.rotate(0.3)

    # 保存文本信息和对应图片名称
    raw_image.save(save_path + str(num) + '.png')
    f1 = open(file, 'a')
    f1.write(str(num) + " " + str(random_word) + '\n')

    print(num)


def is_chinese(self, uchar):
    """判断一个unicode是否是汉字"""
    alnum = np.array([ch.isalnum() for ch in uchar])
    if not alnum.all():
        return True
    else:
        return False


if __name__ == '__main__':
    info_str = []

    #  newwords.txt is a char datasets contain amounts of chars sequnences
    with open('/home/rice/PycharmProjects/TextRecognitionDataGenerator/newwords.txt', 'r', encoding="utf8") as f:
        lines = [l.strip()[0:100] for l in f.readlines()]
        # for l in lines:
        #     print(l)
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        i = 0
        for i in range(len(lines)):
            strx = ''
            chars = lines[i]
            length = len(chars)
            if length < 5:
                continue
            if (length > 4) & (length < 10):
                info_str.append(chars)
                continue
            for i in range(0, length - 10):
                strx = ''
                strx += chars[i:10 + i]

                info_str.append(strx)
            # print(str)
                info_str.append(chars[length - 10:length])
    print(info_str)
    for i in range(0,1000000):
        padding_data_gen('/run/media/rice/DATA/test_text/data/', i, '/run/media/rice/DATA/test_text/labels.txt', info_str)




