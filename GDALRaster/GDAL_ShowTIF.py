# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from osgeo import gdal
from GDALRaster.GDAL_OpenTIF import read_image

# 正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 显示坐标轴负半轴
plt.rcParams['axes.unicode_minus'] = False
# 设置分辨率
plt.rcParams['figure.dpi'] = 200


# 显示灰度图
def show_grey_tiff(raster_data):
    # 将图片转为数组
    image = raster_data.ReadAsArray()
    # 加载灰度图
    plt.imshow(image, cmap='Greys_r')
    # 显示颜色表
    plt.colorbar()
    # 不显示坐标轴
    plt.axis('off')
    # 显示灰度图像
    plt.show()


# 显示简单数组
def show_short_tiff():
    # 生成6行3列的数组（值范围0-17）
    a = np.arange(18).reshape(6, 3)
    # 打印数组
    print(a)
    # 定义图片框
    plt.figure()
    # 将画板分为1行2列，本幅图位于第一个位置
    plt.subplot(1, 2, 1)
    # 显示图像标题
    plt.title("彩色图片")
    # 显示数组彩色图像
    plt.imshow(a)
    # 显示颜色表
    plt.colorbar()
    # 将画板分为1行2列，本幅图位于第2个位置
    plt.subplot(1, 2, 2)
    # 显示图像标题
    plt.title("灰度图")
    # 加载数组灰度图像
    plt.imshow(a, cmap="Greys_r")
    # 显示颜色表
    plt.colorbar()
    # 显示图像
    plt.show()


# 显示部分图片
def show_short_image():
    # 打开图片
    a = plt.imread("../RasterData/xinghuaduotian.jpg")
    # 打印图片的分辨率(高，宽)和通道数
    print(a.shape)
    # 定义图像的标题
    plt.title("彩色图片")
    # 这部分代码没有用
    # # 获取图像前三行
    # b = a[[0, 1, 2]]
    # # 打印获取的图像部分高，宽和通道数
    # print(b.shape)
    # # 获取图像的前三行
    # c = b[:, [0, 1, 2]]
    # # 打印获取的图像部分高，宽和通道数
    # print(c.shape)
    # 定义图片框
    # plt.figure()
    # 将画板分为1行2列，本幅图位于第1个位置
    plt.subplot(1, 2, 1)
    # 定义图片的标题
    plt.title("彩色图片")
    # 加载图片
    plt.imshow(a)
    # 显示颜色表（颜色表为原来的四分之一）
    plt.colorbar(shrink=0.25)
    # 将画板分为1行2列，本幅图位于第2个位置
    plt.subplot(1, 2, 2)
    # 定义图片的标题
    plt.title("灰度图")
    # 获取图片的第一个通道
    img_r = a[:, :, 0]
    # 打印图片的高度和宽度及通道（只有一个通道时，不打印通道数）
    print(img_r.shape)
    # 加载灰度图
    plt.imshow(img_r, cmap="Greys_r")
    # 显示颜色表（颜色表为原来的四分之一）
    plt.colorbar(shrink=0.25)
    # 显示图像
    plt.show()


def show_color_tiff(raster_data, r, g, b):
    # 将数据集转换为数组
    image_data = raster_data.ReadAsArray()
    # 获取RGB三个波段并转换成数组
    band_r = raster_data.GetRasterBand(r).ReadAsArray()
    band_g = raster_data.GetRasterBand(g).ReadAsArray()
    band_b = raster_data.GetRasterBand(b).ReadAsArray()
    # 判断栅格数据类型
    if 'int8' in image_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in image_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    # 将获取的数组转换成Matplotlib显示的RGB格式的数组
    bands = np.array((band_r, band_g, band_b)).transpose((1, 2, 0))
    # 将数组转换成int8范围，并在plt.函数中加载
    plt.imshow(bands.astype(np.uint8))
    # 显示颜色表
    plt.colorbar()
    # 不显示坐标轴
    plt.axis("off")
    # 显示图片
    plt.show()


# 并排显示单波段的图片
def list_show_tiff(raster_data):
    # 将指定的数据集转换成数组
    image = raster_data.ReadAsArray()
    # 定义图片框
    plt.figure()
    # 将画板分为两行两列，本幅图位于第一个位置
    plt.subplot(2, 2, 1)
    # 定义第一个位置图片的标题
    plt.title("彩色图片")
    # 显示原始图像
    plt.imshow(image)
    # 显示颜色表
    plt.colorbar()
    # 将画板分为两行两列，本幅图位于第二个位置
    plt.subplot(2, 2, 2)
    # 定义第二个位置图片的标题
    plt.title("灰度图")
    # 加载灰度图
    plt.imshow(image, cmap='Greys_r')
    # 显示颜色表
    plt.colorbar()
    # 将画板分为两行两列，本幅图位于第三个位置
    plt.subplot(2, 2, 3)
    # 定义第三个位置图片的标题
    plt.title("直方图")
    # 加载灰度图
    plt.hist(image, facecolor='g', edgecolor='b')
    # 显示图例
    plt.legend()
    # 窗口显示图片
    plt.show()


# 直方图统计
def show_tiff_hist(raster_data):
    # 将图片转为数组
    image = raster_data.ReadAsArray()
    # 显示图片的标题
    plt.title("Histogram(直方图)")
    # 渲染直方图
    plt.hist(image, facecolor='g', edgecolor='b', alpha='0.7')
    # 显示格网
    plt.grid(axis='y', alpha=0.75)
    # 显示x轴标记
    plt.xlabel('Value')
    # 显示y轴标记
    plt.ylabel('Frequency')
    # 显示图例
    plt.legend()
    # 窗口显示图片
    plt.show()


def show_tiff_box_plot(raster_data):
    # 将图片转换成数组
    image = raster_data.ReadAsArray()
    # 给数组田间标签
    df = pd.DataFrame(image)
    # 打印数组的描述
    print(df.describe())
    #
    df.plot.box(title="Box Plot")
    #
    plt.grid(linestyle="--", alpha=0.8)
    #
    plt.show()


def show_multi_bands_tiff_grey(raster_data):
    # 打开指定图片
    image = raster_data.ReadAsArray()
    # 定义图片框
    plt.figure()
    # 获取波段数量
    bands_count = raster_data.ReadAsArray().shape[0]
    # 打印波段数
    print("波段数为：" + str(bands_count))
    # 循环获取所有的波段
    for i_band in range(bands_count):
        # 获取波段
        band = raster_data.GetRasterBand(i_band + 1)
        # 将波段转换成数组
        band_data = band.ReadAsArray()
        # 将画板分为两行多列，本幅图位于第一行的第i_band个位置
        plt.subplot(2, bands_count, i_band + 1)
        # 定义图片标题
        plt.title("band" + str(i_band + 1))
        # 显示原始的图像
        plt.imshow(band_data, cmap="Greys_r")
        # 将画板分为两行多列，本幅图位于第二行的第i_band个位置
        plt.subplot(2, bands_count, bands_count + i_band + 1)
        # 计算平均值
        mean_band_data = np.mean(band_data)
        # 计算2倍标准差
        std_band_data = np.std(band_data)
        # 图像2倍标准差拉伸后的图像
        plt.imshow(band_data, cmap="Greys_r", vmin=mean_band_data - std_band_data, vmax=mean_band_data - std_band_data)
    # 窗口显示图片
    plt.show()


if __name__ == '__main__':
    # 显示简单数组图像
    # show_short_tiff()
    # 显示简单图像
    # show_short_image()
    # 获取工程根目录的路径
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 打印工程根目录的路径
    print("root path: " + root_path)
    # 定义数据文件的路径
    data_path = os.path.abspath(root_path + r'\RasterData')
    # 打印数据文件的路径
    print("data path:" + data_path)
    # 切换目录
    os.chdir(data_path)
    # 影像文件名
    image_name = 'S2_20190727San.tif'
    # 读取图像
    dataset = read_image(image_name)
    # 显示彩色图像
    show_color_tiff(dataset, 4, 3, 2)
