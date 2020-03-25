# -*- coding: utf-8 -*-
import os
import numpy as np
import gdal
from GDALRaster.GDAL_OpenTIF import read_image
from GDALRaster.GDAL_ShowTIF import list_show_tiff, show_grey_tiff, show_multi_bands_tiff_grey


def write_image(in_image, out_filename, out_image, datatype):
    # 获取栅格投影信息
    projection = in_image.GetProjection()
    # 获取栅格仿射转换信息
    geo_transform = in_image.GetGeoTransform()
    # 获取栅格的列数
    image_width = in_image.RasterXSize
    # 获取栅格的行数
    image_height = in_image.RasterYSize
    # 通过输出格式获取驱动
    driver = gdal.GetDriverByName(datatype)
    # 创建输出栅格并赋参数
    out_ds = driver.Create(out_filename, image_width, image_height, 1, gdal.GDT_Float32)
    # 定义输出栅格的仿射转换信息
    out_ds.SetGeoTransform(geo_transform)
    # 定义输出栅格的投影信息
    out_ds.SetProjection(projection)
    # 执行输出栅格
    out_ds.GetRasterBand(1).WriteArray(out_image)
    # 清楚缓存
    del out_ds


def write_tiff(filename, image_projection, image_geo_transform, image_data):
    # 判断栅格数据的类型
    if 'int8' in image_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in image_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    # 判断数组的维数
    if len(image_data.shape) == 3:
        image_bands, image_height, image_width = image_data.shape
    else:
        image_bands, (image_height, image_width) = 1, image_data.shape
    # 创建文件驱动
    driver = gdal.GetDriverByName("GTiff")
    # 创建输出数据源
    out_ds = driver.Create(filename, image_width, image_height, image_bands, datatype)
    # 设置仿射变换参数
    out_ds.SetGeoTransform(image_geo_transform)
    # 设置投影信息
    out_ds.SetProjection(image_projection)
    # 写入数据
    if image_bands == 1:
        out_ds.GetRasterBand(1).WriteArray(image_data)
    else:
        for i_band in range(image_bands):
            out_ds.GetRasterBand(i_band + 1).WriteArray(image_data[i_band])
    # 清除缓存
    del out_ds


# 获取所有印象的波段并写入文件夹
def get_band_from_tiff(path, filename):
    # 切换路径到待处理图像所在文件夹
    os.chdir(path)
    # 读取影像数据集
    dataset = read_image(filename)
    # 获取文件名（不含文件名）
    filename_prefix = filename.split('.')[0]
    # 获取波段数量
    bands_count = dataset.ReadAsArray().shape[0]
    # 打印波段数
    print("波段数量为：" + str(bands_count))
    # 循环获取所有波段
    for i_band in range(bands_count):
        # 打印目前所处的波段
        print(i_band + 1)
        # 通过序号获取波段
        band = dataset.GetRasterBand(i_band + 1)
        # 将获取的波段转换成数组
        band_data = band.ReadAsArray()
        # 定义输出的文件名
        out_filename = filename_prefix + "_band" + str(i_band + 1) + ".tif"
        # 打印输出的文件名
        print("out_filename：" + out_filename)
        # 调用栅格写入函数
        write_image(dataset, out_filename, band_data, "GTiff")
    # 显示各波段的图片
    show_multi_bands_tiff_grey(dataset)


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
    # 调用函数
    get_band_from_tiff(data_path, image_name)
