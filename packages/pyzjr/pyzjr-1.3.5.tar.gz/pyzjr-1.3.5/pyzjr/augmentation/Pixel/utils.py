import cv2
import numpy as np

from skimage.morphology import medial_axis
from scipy.ndimage import distance_transform_edt

__all__ = ["DistanceTransform"]


class DistanceTransform():
    # 距离变换
    def distance(self, image):
        # 使用OpenCV中的距离变换函数
        dist_transform = cv2.distanceTransform(image, cv2.DIST_L2, 3)
        return dist_transform

    def chamfer(self,image, weight=None):
        # Chamfer距离变换
        if weight is None:
            weights = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]], dtype=np.uint8)
        else:
            weights = weight
        dist_transform = cv2.filter2D(image, cv2.CV_32F, weights)
        return dist_transform

    def fast_marching(self, image):
        # Fast-Marching距离变换
        _, medial_axis_image = medial_axis(image, return_distance=True)   # 使用medial_axis函数计算中轴线
        dist_transform = distance_transform_edt(medial_axis_image)
        return dist_transform


if __name__=="__main__":
    image = np.zeros((10, 10), dtype=np.uint8)
    image[2:8, 2:8] = 255
    print(image)

    # 调用距离变换算法
    dis = DistanceTransform()
    dist_transform = dis.distance(image)
    chamfer_dist_transform = dis.chamfer(image)
    fast_marching_dist_transform = dis.fast_marching(image)
    # 打印距离变换结果
    print("Distance Transform:")
    print(dist_transform)
    print("\nChamfer Distance Transform:")
    print(chamfer_dist_transform)
    print("\nFast-Marching Distance Transform:")
    print(fast_marching_dist_transform)