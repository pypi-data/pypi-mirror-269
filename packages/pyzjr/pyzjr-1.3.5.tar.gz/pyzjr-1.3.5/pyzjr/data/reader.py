import os
import re
from pathlib import Path
import random
from tqdm import tqdm
import cv2
import shutil
import numpy as np
import PIL.Image as Image
import datetime
from os import getcwd

__all__ = ["getPhotopath", "timestr", "pathstr", "natsorted", "natural_key",
           "MultiImageFolderProcessor"]

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', 'tif', 'raw')
IMAGE_EXTENSIONS_SET = set(IMAGE_EXTENSIONS)

def getPhotopath(paths, cd=False, debug=False):
    """
    :param paths: 文件夹路径
    :param cd: 添加当前运行的路径名,这是使用了相对路径才能用的
    :param debug: 开启打印文件名错误的名字
    :return: 包含图片路径的列表
    """
    imgfile = []
    allfile = []
    file_list = os.listdir(paths)
    for i in file_list:
        if debug:
            if i[0] in ['n', 't', 'r', 'b', 'f'] or i[0].isdigit():
                print(f"[pyzjr]: File name:Error occurred at the beginning of {i}!")
        newph = os.path.join(paths, i).replace("\\", "/")
        allfile.append(newph)
        _, file_ext = os.path.splitext(newph)
        if file_ext[1:] in IMAGE_EXTENSIONS:
            imgfile.append(newph)
    if cd:
        # 谨慎使用
        cdd = getcwd()
        imgfile = [os.path.join(cdd, file).replace("\\", "/") for file in imgfile]
        allfile = [os.path.join(cdd, file).replace("\\", "/") for file in allfile]
    return imgfile, allfile

def timestr():
    """Generate a formatted datetime string."""
    return f"{datetime.datetime.now():%Y_%m_%d_%H_%M_%S}".replace(":", "_")

def alphabetlabels(capital=False):
    """字符标签"""
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    uppercase_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    return uppercase_alphabet if capital else alphabet

def pathstr(path_str):
    """
    path_str = 'D:/PythonProject/Torchproject/Lasercenterline/line/20231013-LaserLine_txt/test_2/imges/Image_1.jpg'
    D:\
    PythonProject
    Torchproject
    Lasercenterline
    line
    20231013-LaserLine_txt
    test_2
    imges
    Image_1.jpg
    """
    path = Path(path_str)
    path_parts = path.parts
    return list(path_parts)

def natural_key(st):
    """
    将字符串拆分成字母和数字块
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', st)]

def natsorted(a):
    """
    手写自然排序
    >>> a = ['num9', 'num5', 'num2']
    >>> sorted_a = natsorted(a)
    ['num2', 'num5', 'num9']
    """
    return sorted(a, key=natural_key)

class MultiImageFolderProcessor():
    def __init__(self, imagefolder):
        if self.is_directory_not_empty(imagefolder):
            self.imagefolder = imagefolder
        else:
            raise ValueError("[MultiImageFolderProcessor]:The provided folder path is empty.")

    def is_image_file(self, filename):
        """
        检查文件名是否符合要求
        :param filename: 文件名
        """
        return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

    def is_image_extension(self, ext):
        """
        检查给定的文件扩展名是否为图像扩展名。
        :param ext (str): 要检查的文件扩展名。
        """
        return ext in IMAGE_EXTENSIONS_SET

    def valid_extension(self, ext):
        """
        检查给定的文件扩展名是否是有效的扩展名。
        :param ext (str): 要检查的文件扩展名。
        """
        if ext is not None and isinstance(ext, str) and ext.startswith('.') and len(ext) >= 2:
            return True
        else:
            return False

    def is_directory_not_empty(self, path):
        """
        检查给定路径是否是非空文件夹。
        :param path (str): 要检查的路径。
        """
        return os.path.isdir(path) and len(os.listdir(path)) > 0

    @property
    def list_dirs(self):
        """
        返回给定目录中的所有目录
        """
        return [f for f in Path(self.imagefolder).iterdir() if f.is_dir()]

    @property
    def list_files(self):
        """
        返回给定目录中的所有文件
        """
        return [
            f for f in Path(self.imagefolder).iterdir()
            if f.is_file() and not f.name.startswith(".")
        ]

    @property
    def run_py_path(self):
        """当前运行的py脚本的路径"""
        return os.path.abspath(__file__)

    @property
    def run_py_dir_path(self):
        """当前运行py脚本的文件夹路径"""
        return os.path.dirname(os.path.abspath(__file__))

    def list_files_by_ext(self, ext):
        """
        返回给定目录中指定扩展名的文件列表
        :param ext(str): 指定的文件扩展名。
        """
        return [
            f for f in Path(self.imagefolder).iterdir()
            if f.is_file() and not f.name.startswith(".") and f.suffix == ext
        ]

    @property
    def get_imagepath_list(self):
        """获取符合IMAGE_EXTENSIONS的图像路径"""
        imgpathlist = [
            f for f in Path(self.imagefolder).iterdir()
            if f.is_file() and not f.name.startswith(".") and f.suffix in IMAGE_EXTENSIONS
        ]
        if len(imgpathlist)==0:
            raise ValueError(f"[MultiImageFolderProcessor]:The obtained image list is empty, possibly because the suffix does not match {IMAGE_EXTENSIONS}")
        return imgpathlist

    def split_seg_trainval_txt(self, save_folder, tratio=0.8, vratio=0.1, shuffle=True):
        """
        划分分割任务的训练集、测试集、验证集的脚本
        :param save_folder: 指定的文件保存路径
        :param tratio: 训练集比例
        :param vratio: 验证集比例
        :param shuffle: 打乱写入顺序
        """
        def write_txt(file_list, txt_path, desc):
            total_files = len(file_list)
            with tqdm(total=total_files, desc=desc, unit=" per") as pbar:
                with open(txt_path, 'w') as f:
                    for file_name in file_list:
                        f.write(file_name[:-4] + '\n')
                        pbar.update(1)
        os.makedirs(save_folder, exist_ok=True)

        test_ratio = 1 - tratio - vratio
        if test_ratio < 0 or test_ratio > 1:
            raise ValueError(f"[MultiImageFolderProcessor]:The ratio between tratio={tratio} and vratio={vratio} is incorrect, and the sum of the two should be less than or equal to 1")
        jpg_files = [file for file in os.listdir(self.imagefolder) if file.lower().endswith('.jpg')]
        if len(jpg_files) == 0:
            raise ValueError(f"[MultiImageFolderProcessor]:The {self.imagefolder} has been converted to an empty list, which may be due to images not being in JPG format.")
        if shuffle:
            random.shuffle(jpg_files)
        total_files = len(jpg_files)
        train_files = int(tratio * total_files)
        val_files = int(vratio * total_files)

        train_list = jpg_files[:train_files]
        val_list = jpg_files[train_files:train_files + val_files]
        test_list = jpg_files[train_files + val_files:] if test_ratio > 0 else []
        write_txt(train_list, os.path.join(save_folder, 'train.txt'),desc="Write training file")
        write_txt(val_list, os.path.join(save_folder, 'val.txt'), desc="Write verification file")
        write_txt(test_list, os.path.join(save_folder, 'test.txt'), desc="Write testing file")

    def convert_image_format(self, save_folder, output_format='.png'):
        """
        任意格式转换
        :param save_folder: 指定的文件保存路径
        :param output_format: 指定修改的后缀名
        """
        os.makedirs(save_folder, exist_ok=True)
        image_files = [file for file in os.listdir(self.imagefolder) if file.lower().endswith(IMAGE_EXTENSIONS)]

        for image_file in image_files:
            input_path = os.path.join(self.imagefolder, image_file)
            output_path = os.path.join(save_folder, os.path.splitext(image_file)[0] + output_format)

            img = cv2.imread(input_path)
            cv2.imwrite(output_path, img)

    def copy_image_folder(self, save_folder):
        """
        复制整个文件夹（图像）到另外一个文件夹
        :param save_folder: 指定的文件保存路径
        """
        try:
            os.makedirs(save_folder, exist_ok=True)
            for root, dirs, files in os.walk(self.imagefolder):
                for file in files:
                    if self.is_image_file(file):
                        source_path = os.path.join(root, file)
                        destination_path = os.path.join(save_folder, file)  # Fix: use a different variable for destination path
                        shutil.copy2(source_path, destination_path)
            print(f"[MultiImageFolderProcessor]:Successfully copied folder: {self.imagefolder} to {save_folder}")
        except Exception as e:
            print(f"[MultiImageFolderProcessor]:Error copying folder: {e}")

    def resize_image_folder(self, save_folder, target_size):
        """
        修改图像的大小，并保存到指定的文件夹
        :param save_folder: 指定的文件保存路径
        :param target_size: 指定的图像大小，可以是一个整数，也可以是长度为2的列表或元组
        """
        def check_image_size(target_size):
            if isinstance(target_size, int):
                target_size = (target_size, target_size)
                return target_size
            if isinstance(target_size, (list, tuple)) and len(target_size) == 2:
                return target_size
            else:
                raise ValueError("[MultiImageFolderProcessor]:Invalid target_size format. Please provide a single integer or a tuple/list of two integers.")
        try:
            target_size = check_image_size(target_size)
            os.makedirs(save_folder, exist_ok=True)
            for root, dirs, files in os.walk(self.imagefolder):
                for file in files:
                    if file.lower().endswith(IMAGE_EXTENSIONS):
                        source_path = os.path.join(root, file)
                        output_path = os.path.join(save_folder, file)
                        img = cv2.imread(source_path)
                        resized_img = cv2.resize(img, target_size)
                        cv2.imwrite(output_path, resized_img)

            print(f"[MultiImageFolderProcessor]:Successfully resized and saved images from {self.imagefolder} to {save_folder}")
        except Exception as e:
            print(f"[MultiImageFolderProcessor]:Error resizing and saving images: {e}")

    def check_2_folder_different_names(self, png_folder, save_folder):
        """
        检查两个文件夹当中图片名是否相同,如果不同,移动这些文件到新的文件夹当中(不包含后缀的情况,一般用于检查训练集和测试集),这样就能划分出测试集
        :param target_folder:
        :param save_folder:
        """
        os.makedirs(save_folder, exist_ok=True)
        # 获取两个文件夹中的文件名称（不包括文件扩展名）
        jpg_files = {os.path.splitext(file)[0] for file in os.listdir(self.imagefolder) if file.lower().endswith('.jpg')}
        png_files = {os.path.splitext(file)[0] for file in os.listdir(png_folder) if file.lower().endswith('.png')}
        if len(jpg_files) == 0:
            raise ValueError(f"[MultiImageFolderProcessor]:The file of {self. imagefolder} is recognized, possibly because it does not end in jpg format")
        if len(png_files) == 0:
            raise ValueError(f"[MultiImageFolderProcessor]:The file of {png_folder} is recognized, possibly because it does not end in png format or the file path is incorrect")
        if len(jpg_files) >= len(png_files):
            unmatched_files = jpg_files - png_files
            flag_to_move_jpg_files = True
        else:
            unmatched_files = png_files - jpg_files
            flag_to_move_jpg_files = False

        for file in unmatched_files:
            if flag_to_move_jpg_files:
                shutil.move(os.path.join(self.imagefolder, file + '.jpg'), os.path.join(save_folder, file + '.jpg'))
            else:
                shutil.move(os.path.join(png_folder, file + '.png'), os.path.join(save_folder, file + '.png'))

    @property
    def get_mean_std(self):
        """
        :return: 返回RGB顺序的mean与std
        """
        all_images = [Image.open(os.path.join(self.imagefolder, file)).convert('RGB') for file in
                      os.listdir(self.imagefolder) if file.lower().endswith(IMAGE_EXTENSIONS)]
        num_images = len(all_images)
        mean_sum = [0, 0, 0]
        std_sum = [0, 0, 0]

        for image in all_images:
            img_asarray = np.asarray(image) / 255.0
            individual_mean = np.mean(img_asarray, axis=(0, 1))
            individual_stdev = np.std(img_asarray, axis=(0, 1))
            mean_sum += individual_mean
            std_sum += individual_stdev

        mean = mean_sum / num_images
        std = std_sum / num_images
        return list(mean), list(std)

    def RenameImageFolder(self, save_folder, newbasename='img', type=3, format=None):
        """
        重命名图像文件夹中的所有图像文件
        :param save_folder: 新文件夹的保存路径
        :param type: 数字长度，比如005长度为3
        :param format: 后缀,如果是None就表示用原来的后缀
        """
        os.makedirs(save_folder, exist_ok=True)
        imglist = self.get_imagepath_list
        total_files = len(imglist)
        for i, file in tqdm(enumerate(imglist), total=total_files, desc='Renaming files'):
            properties = os.path.basename(file)
            name, ext = os.path.splitext(properties)
            padded_i = str(i).zfill(type)
            if format is not None:
                newname = f"{newbasename}{padded_i}." + format
            else:
                newname = f"{newbasename}{padded_i}.{ext[1:]}"
            new_path = os.path.join(save_folder, newname)
            shutil.copy(file, new_path)
        print("[MultiImageFolderProcessor]:Batch renaming and saving of files completed!")



if __name__=="__main__":
    folder = r"D:\PythonProject\pythonProject2\dataloader\Pothole\test\images"
    folderimg = MultiImageFolderProcessor(folder)
    # folderimg.split_seg_trainval_txt(save_folder=r"D:\PythonProject\pythonProject2\dataloader\Pothole")
    # a = folderimg.list_files
    # folderimg.resize_image_folder(save_folder=r"D:\PythonProject\pythonProject2\dataloader\Pothole\test3", target_size=512)
    # folderimg.RenameImageFolder(save_folder=r"D:\PythonProject\pythonProject2\dataloader\Pothole\test3")


