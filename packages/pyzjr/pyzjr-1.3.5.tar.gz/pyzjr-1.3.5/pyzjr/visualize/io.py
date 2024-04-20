"""
Copyright (c) 2023, Auorui.
All rights reserved.

This module is applied to image reading and display.
"""
import os
import cv2
import imghdr
import torch
import numpy as np
from urllib import request
from matplotlib import pyplot as plt
from pyzjr.core import is_url
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pathlib import Path
from pyzjr.core import is_gray_image, is_pil

__all__ = ["ImagesReader", "imwrite", "imshowplt", "StackedCV2", "StackedImages", "Stackedplt",
           "Stackedtorch", "plot_line", "bar_chart", "scatter_plot", "url2cvImage"]

RGB2BGR  = cv2.COLOR_RGB2BGR
BGR2RGB  = cv2.COLOR_BGR2RGB
BGR2GRAY = cv2.COLOR_BGR2GRAY
RGB2GRAY = cv2.COLOR_RGB2GRAY
GRAY2BGR = cv2.COLOR_GRAY2BGR
BGR2HSV  = cv2.COLOR_BGR2HSV
RGB2HSV  = cv2.COLOR_RGB2HSV
HSV2BGR  = cv2.COLOR_HSV2BGR
HSV2RGB  = cv2.COLOR_HSV2RGB

class ImagesReader(object):
    def __init__(self, filename, is_gray=False, flip=None):
        """
         Initialize ImagesReader object.

        :param filename: Path to the image file.
        :param is_gray: If True, read the image in grayscale.
        :param flip: 0: Flip vertically.
                    1: Flip horizontally.
                   -1: Flip both vertically and horizontally.
        """
        if not os.path.isfile(filename):
            raise ValueError(f"[ImagesReader]: The file {filename} does not exist.")
        if isinstance(filename, Path):
            filename = str(filename.resolve())
        self.filename = filename
        self.flags = cv2.IMREAD_COLOR
        self.is_gray = is_gray
        self.torgb = False
        if flip in [-1, 0, 1]:
            self.flip = flip
        else:
            raise ValueError("[ImagesReader]:The flip parameter should be -1, 0, or 1")

    def imread(self, mode=None):
        if mode is None or mode == "BGR":
            self.flags = cv2.IMREAD_COLOR
        elif self.is_gray or mode == "L":
            self.flags = cv2.IMREAD_GRAYSCALE
        elif mode == "RGB":
            self.torgb = True
        else:
            raise ValueError(f"[ImagesReader]: Unsupported mode: {mode}")

        self.image = cv2.imdecode(np.fromfile(self.filename, np.uint8), self.flags)

        if self.flip is not None:
            self.image = cv2.flip(self.image, self.flip)
        if self.torgb:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return self.image

    def display(self, winname, param=False):
        """Displays an image in the specified window."""
        _imshow = cv2.imshow  # copy to avoid recursion errors
        _imshow(winname.encode('unicode_escape').decode(), self.image)
        if param:
            print(f"\033[94m{self.param()}")
        cv2.waitKey(0)

    def param(self, idx=None):
        properties = {}
        if isinstance(self.filename, str):
            properties['name'] = os.path.basename(self.filename)
            properties['format'] = imghdr.what(self.filename)
            properties['fsize'] = os.path.getsize(self.filename)
        properties["shape"] = self.image.shape
        properties["dtype"] = self.image.dtype
        properties["channels"] = self.image.shape[2] if len(self.image.shape) == 3 else 1
        properties["resolution"] = (self.image.shape[1], self.image.shape[0])
        return properties if idx is None else properties[idx]

def url2cvImage(url):
    if is_url(url):
        res = request.urlopen(url, timeout=3)
    else:
        raise ValueError("[url2imgcv2]:The current input parameter does not conform to the URL format")
    try:
        image = np.asarray(bytearray(res.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    except:
        print ('[url2imgcv2]: Load read - Image timeout!')
        image = []
    h, w, c = image.shape
    if c == 4:
        image = image[:,:,:3]
    return image

def imwrite(filename: str, img: np.ndarray, params=None):
    """Write the image to a file."""
    try:
        cv2.imencode(Path(filename).suffix, img, params)[1].tofile(filename)
        return True
    except Exception:
        return False

def imshowplt(image, title=None):
    """显示图像并添加标题"""
    import matplotlib
    matplotlib.use("TkAgg")
    cmap = None
    if is_pil:
        if image.mode == 'L' or (image.mode == 'LA' and image.getbands()[1] == 'L'):
            cmap = 'gray'
    else:
        if is_gray_image(image):
            cmap = 'gray'
    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    if title:
        plt.title(title)
    plt.show()

def StackedImages(scale, imgArray):
    """
    :param scale:图片的规模,可使用小数,1为原始图像
    :param imgArray: 图像组成的列表，来表示行列排列
    :return: 生成的图像可按输入列表的行列排序展示,拼接展示图像
    """
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def StackedCV2(scale, imgList, cols):
    """
    将多张图像堆叠在一起并在单个窗口中显示
    :param scale: 图像的缩放比例,大于1表示放大,小于1表示缩小
    :param imgList: 要堆叠的图像列表
    :param cols: 每行显示的图像数量
    :return: 堆叠后的图像
    """
    totalImages = len(imgList)
    rows = totalImages // cols if totalImages // cols * cols == totalImages else totalImages // cols + 1
    blankImages = cols * rows - totalImages

    width = imgList[0].shape[1]
    height = imgList[0].shape[0]
    imgBlank = np.zeros((height, width, 3), np.uint8)
    imgList.extend([imgBlank] * blankImages)
    for i in range(cols * rows):
        imgList[i] = cv2.resize(imgList[i], (0, 0), None, scale, scale)
        if len(imgList[i].shape) == 2:
            imgList[i] = cv2.cvtColor(imgList[i], cv2.COLOR_GRAY2BGR)
    hor = [imgBlank] * rows
    for y in range(rows):
        line = []
        for x in range(cols):
            line.append(imgList[y * cols + x])
        hor[y] = np.hstack(line)
    ver = np.vstack(hor)
    return ver

def Stackedplt(images, shape, spacing=0.1):
    """
    按照指定形状堆叠并显示多张图片——plt
    :param images: 包含多张图片数据的列表或数组。每张图片的形状应相同
    :param shape: 展示的图片的行列数,如(2, 3)
    :param spacing: 图片之间的间隔,默认为0.1
    :return:
    """
    rows, cols = shape
    image_height, image_width, _ = images[0].shape
    stacked_height = int(rows * image_height + (rows - 1) * image_height * spacing)
    stacked_width = int(cols * image_width + (cols - 1) * image_width * spacing)
    stacked_image = np.ones((stacked_height, stacked_width, 3), dtype=np.uint8) * 255
    for i, image in enumerate(images):
        row = i // cols
        col = i % cols

        x = int(col * (image_width + spacing * image_width))
        y = int(row * (image_height + spacing * image_height))

        stacked_image[y:y+image_height, x:x+image_width, :] = image

    plt.imshow(stacked_image)
    plt.axis('off')  # 关闭坐标轴显示
    plt.show()

def Stackedtorch(imgs, num_rows, num_cols, titles=None, scale=None, camp=None):
    """
    堆叠显示Tensor图像或PIL图像
    :param imgs: 包含图像的列表,可以包含Tensor图像或PIL图像
    :param num_rows: 图像的行数
    :param num_cols: 图像的列数
    :param titles: 图像的标题列表,默认为None
    :param scale: 图像的缩放比例,默认为None
    :param camp: 'gray'
    :return:
    example:
        imgs = [image1, image2, image3, image4]
        titles = ['Image 1', 'Image 2', 'Image 3','Image 4']
        axes = Stackedtorch(imgs, 2, 2, titles=titles, scale=5)
        plt.savefig('my_plot.jpg')
        plt.show()
    """
    if scale:
        figsize = (num_cols * scale, num_rows * scale)
        _, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    else:
        _, axes = plt.subplots(num_rows, num_cols)
    axes = axes.flatten()
    for i, (ax, img) in enumerate(zip(axes, imgs)):
        if torch.is_tensor(img):
            # Tensor Image
            ax.imshow(img.numpy(),cmap=camp)
        else:
            # PIL Image
            ax.imshow(img,cmap=camp)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        if titles:
            ax.set_title(titles[i])
    return axes

def plot_line(x, y, xlabel, ylabel, title):
    """
    绘制折线图
    :param x: x轴的数据列表
    :param y: y轴的数据列表
    :param xlabel: x轴的标签
    :param ylabel: y轴的标签
    :param title: 图形的标题
    :return:
    """
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def bar_chart(x, y, xlabel, ylabel, title):
    """绘制柱状图"""
    plt.bar(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def scatter_plot(x, y, xlabel, ylabel, title):
    """绘制散点图"""
    plt.scatter(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


if __name__=="__main__":
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    xlabel = 'X'
    ylabel = 'Y'
    title = '折线图示例'
    plot_line(x, y, xlabel, ylabel, title)
    bar_chart(x, y, xlabel, ylabel, title)
    scatter_plot(x, y, xlabel, ylabel, title)
