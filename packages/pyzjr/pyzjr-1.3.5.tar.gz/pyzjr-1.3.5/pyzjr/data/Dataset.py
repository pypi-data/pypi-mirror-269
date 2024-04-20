import os
import numpy as np
from PIL import Image
import cv2
from pyzjr.nn import get_one_hot
from pyzjr.data.basedataset import BaseDataset

__all__ = ["BaseClsDataset", "SegmentTwoDataset", "VOCSegmentation"]


class BaseClsDataset(BaseDataset):

    def __init__(self, file_txt, image_transform=None):
        """
        Supports txt file paths that match the format, or have been processed into the format list below.
        file_txt format: [path/to/xxx.jpg 0,
                          path/to/xxx.jpg 1,           OR           path/to/xxx.txt
                          path/to/xxx.jpg 2,
                          ...]
        """
        super().__init__()
        file_txt_result = self.load_txt_path_or_list(file_txt)
        if self._check_file_txt_format(file_txt_result):
            self.file_txt = file_txt_result
        self.image_transform = image_transform

    def __len__(self):
        return len(self.file_txt)

    def _check_file_txt_format(self, file_txt):
        for line in file_txt:
            parts = line.split()
            assert len(parts) == 2, f"BaseClsDataset: Invalid format in line: {line}"
            file_path, digit_label = parts
            assert os.path.exists(file_path), f"BaseClsDataset: File not found: {file_path}"
            assert digit_label.isdigit(), f"BaseClsDataset: Invalid digit label: {digit_label}"
        return True

    def __getitem__(self, idx):
        print(self.file_txt[idx])
        file_path, digit_label = self.file_txt[idx].split()
        raw_image = Image.open(file_path)
        image = raw_image.convert("RGB")
        if self.image_transform is not None:
            image = self.image_transform(image)
        return image, int(digit_label)

class VOCSegmentation(BaseDataset):

    def __init__(
            self,
            root,
            year="2012",
            image_set="train",
            transforms=None,
    ):
        super(VOCSegmentation, self).__init__()
        assert year in ["2007", "2008", "2009", "2010", "2011", "2012"], \
            "year can only choose 2007 to 2012"
        if year == "2007" and image_set == "test":
            year = "2007-test"
        self.year = year
        self.transforms = transforms
        voc_root = os.path.join(root, f"VOC{year}")
        txt_name = image_set + ".txt"

        assert os.path.exists(voc_root), "path '{}' does not exist.".format(voc_root)

        image_dir = os.path.join(voc_root, 'JPEGImages')
        mask_dir = os.path.join(voc_root, 'SegmentationClass')
        txt_path = os.path.join(voc_root, "ImageSets", "Segmentation", txt_name)

        assert os.path.exists(txt_path), "file '{}' does not exist.".format(txt_path)

        file_names = self.load_txt_path_or_list(txt_path)
        self.images = [os.path.join(image_dir, x + ".jpg") for x in file_names]
        self.masks = [os.path.join(mask_dir, x + ".png") for x in file_names]
        assert (len(self.images) == len(self.masks))

    def __getitem__(self, index: int):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is the image segmentation.
        """
        img = Image.open(self.images[index]).convert('RGB')
        target = Image.open(self.masks[index]).convert('L')

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.images)

class SegmentTwoDataset(BaseDataset):
    """
    二分类专用 Dataset ,目录结构请参照以下所示
    Example:
        pneumonia
            - image
            - label
            - test
            - train.txt
            - val.txt
            - test.txt
    """
    def __init__(self, file_path, input_shape=(512, 512), num_classes=2, train=True):
        super(SegmentTwoDataset, self).__init__()
        self.num_classes = num_classes
        self.input_shape = input_shape
        TXT = 'train.txt' if train else 'val.txt'
        txt_path = os.path.join(file_path, TXT)
        self.train = train

        self.image_paths = self.load_txt_path_or_list(txt_path)
        self.image_file_path = os.path.join(file_path, "image")
        self.label_file_path = os.path.join(file_path, "label")
        self.osmkdirs(file_path, self.label_file_path, self.image_file_path)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        one_image_name = self.image_paths[index]
        jpg = os.path.join(self.image_file_path, one_image_name) + '.jpg'
        png = os.path.join(self.label_file_path, one_image_name) + '.png'
        jpg, png = Image.open(jpg).convert("RGB"), Image.open(png).convert("L")
        jpg, png = self.get_random_data(jpg, png, self.input_shape, random=self.train)
        jpg, modify_png = self.imlabel2tensor(jpg, png, num_classes=2, sigmoid=False)
        seg_labels = modify_png
        # 在这里需要 + 1, 是因为数据集有些标签具有白边部分, 我们需要将白边部分进行忽略，+1的目的是方便忽略。
        seg_labels = get_one_hot(seg_labels, num_classes=self.num_classes + 1)
        return jpg, modify_png, seg_labels

    def get_image_name_list(self):
        return self.image_paths

    def get_random_data(self, image, label, input_shape, jitter=.3, hue=.1, sat=0.7, val=0.3, random=True):
        label = Image.fromarray(np.array(label))
        iw, ih = image.size
        h, w = input_shape

        if not random:
            iw, ih = image.size
            scale = min(w / iw, h / ih)
            nw = int(iw * scale)
            nh = int(ih * scale)

            image = image.resize((nw, nh), Image.BICUBIC)
            new_image = Image.new('RGB', (w, h), (128, 128, 128))
            new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))

            label = label.resize((nw, nh), Image.NEAREST)
            new_label = Image.new('L', (w, h), (0))
            new_label.paste(label, ((w - nw) // 2, (h - nh) // 2))
            return new_image, new_label

        new_ar = iw / ih * self.rand(1 - jitter, 1 + jitter) / self.rand(1 - jitter, 1 + jitter)
        scale = self.rand(0.25, 2)
        if new_ar < 1:
            nh = int(scale * h)
            nw = int(nh * new_ar)
        else:
            nw = int(scale * w)
            nh = int(nw / new_ar)
        image = image.resize((nw, nh), Image.BICUBIC)
        label = label.resize((nw, nh), Image.NEAREST)

        flip = self.rand() < .5
        if flip:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            label = label.transpose(Image.FLIP_LEFT_RIGHT)

        dx = int(self.rand(0, w - nw))
        dy = int(self.rand(0, h - nh))
        new_image = Image.new('RGB', (w, h), (128, 128, 128))
        new_label = Image.new('L', (w, h), (0))
        new_image.paste(image, (dx, dy))
        new_label.paste(label, (dx, dy))
        image = new_image
        label = new_label

        image_data = np.array(image, np.uint8)
        r = np.random.uniform(-1, 1, 3) * [hue, sat, val] + 1
        hue, sat, val = cv2.split(cv2.cvtColor(image_data, cv2.COLOR_RGB2HSV))
        dtype = image_data.dtype
        x = np.arange(0, 256, dtype=r.dtype)
        lut_hue = ((x * r[0]) % 180).astype(dtype)
        lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
        lut_val = np.clip(x * r[2], 0, 255).astype(dtype)
        image_data = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val)))
        image_data = cv2.cvtColor(image_data, cv2.COLOR_HSV2RGB)

        return image_data, label

class YOLOv5Dataset(BaseDataset):
    def __init__(self,
                 path,
                 img_size=640,
                 batch_size=2,
                 image_transform=None,
                 ):
        super().__init__()
        self.path = path
        self.img_size = img_size
        self.batch_size = batch_size
        self.transform = image_transform
        self.img_files = self._check_path_is_list(self.path)
        self.label_files = self.img_to_label_paths(self.img_files)

    def img_to_label_paths(self, img_paths):
        """
        1 Replace '/images/' with '/labels/'.
        2 Remove the file extension by calling. split ('.', 1) [0].
        3 Finally, add. txt to obtain the final label path.
        """
        sa, sb = f'{os.sep}images{os.sep}', f'{os.sep}labels{os.sep}'  # /images/, /labels/ substrings
        return [sb.join(x.rsplit(sa, 1)).rsplit('.', 1)[0] + '.txt' for x in img_paths]

    def _check_path_is_list(self, _path):
        img_path_list = []
        if isinstance(_path, list):
            img_path_list.extend(item.strip() for item in _path)

if __name__ == "__main__":
    from torch.utils.data import DataLoader

    dataset_path = r"D:\PythonProject\uhrnet\data\pneumonia"
    train_dataset = SegmentTwoDataset(dataset_path, train=True)
    val_dataset = SegmentTwoDataset(dataset_path, train=False)

    train_loader = DataLoader(train_dataset, shuffle=True, batch_size=2, num_workers=8, pin_memory=True,
                              drop_last=True)
    val_loader = DataLoader(val_dataset, shuffle=True, batch_size=1, num_workers=4, pin_memory=True,
                            drop_last=True)

    for im, label, seglabel in train_loader:
        print(im.shape, label.shape, seglabel.shape)