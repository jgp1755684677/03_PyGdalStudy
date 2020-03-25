# -*- coding: utf-8 -*-
import os
import numpy as np
from GDALRaster.GDAL_OpenTIF import read_image, read_tiff
from GDALRaster.GDAL_WriteTIF import write_image, write_tiff
import GDALRaster.GDAL_ShowTIF as showTIFF


# 计算图像的NDVI
def NDVI_cal(filename):
    # 读取图像
    dataset = read_image(filename)
    # 获取文件名，不含后缀
    filename_prefix = filename.split('.')[0]
    # 将栅格数组转为数组并将数组转换成float格式
    image_data = dataset.ReadAsArray().astype(np.float)
    # 计算ndvi
    ndvi = (image_data[3] - image_data[2])/(image_data[3] + image_data[2])
    # 定义输出ndvi文件名
    out_filename = filename_prefix + "_NDVI.tif"
    # 打印输出的文件名
    print("out_filename：" + out_filename)
    # 将计算的结果写入文件中
    write_image(dataset, out_filename, ndvi, "GTiff")
    # 提示文件写入完成
    print(out_filename + "写入完成！")
    # 读取写入的文件
    ndvi_data = read_image(out_filename)
    # 窗口显示读取的数组
    showTIFF.list_show_tiff(ndvi_data)


# 波段重组
def combine_bands_tiff(in_filename, out_filename):
    # 读取图像
    projection, geo_transform, image_data, image_height, image_width = read_tiff(in_filename)
    # 获取图像的所有波段数据
    image_data1 = image_data[0]
    image_data2 = image_data[1]
    image_data3 = image_data[2]
    image_data4 = image_data[3]
    # 定义输出波段数组组合
    bands_array = np.array((image_data2, image_data3, image_data4), dtype=image_data2.dtype)
    # 打印输出波段数组组合
    print(bands_array)
    # 将波段重组后的图像写入文件
    write_tiff(out_filename, projection, geo_transform, bands_array)


if __name__ == '__main__':
    # 获取工程根目录的路径
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 打印工程根目录的路径
    print("root path:" + root_path)
    # 定义数据文件的路径
    data_path = os.path.abspath(root_path + r'\RasterData')
    # 打印数据文件的路径
    print("data path:" + data_path)
    # 切换目录
    os.chdir(data_path)
    image_name = "S2_20190727San.tif"
    # # 调用函数
    # NDVI_cal(image_name)
    filename = 'S2_20190727San_234.tif'
    combine_bands_tiff(image_name, filename)
