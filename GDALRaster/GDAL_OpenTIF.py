from osgeo import gdal
import os


# 读图像函数
def read_image(filename):
    # 打开文件
    dataset = gdal.Open(filename)
    # 获取栅格矩阵的列数
    image_width = dataset.RasterXSize
    # 获取栅格矩阵的行数
    image_height = dataset.RasterYSize
    # 打印栅格矩阵的列数和行数
    print("栅格矩阵的列数为：%d，栅格矩阵的行数为：%d" % (image_width, image_height))
    # 获取地图的投影信息
    image_projection = dataset.GetProjection()
    # 打印栅格文件的投影信息
    print("栅格的投影信息为：%s" % image_projection)
    # 将数据写成数组
    image_data = dataset.ReadAsArray(0, 0, image_width, image_height)
    # 打印栅格影像的属性
    print(image_data.shape)
    # 打印栅格矩阵信息
    print(image_data)
    # 清除数据集缓存
    del image_data
    # 返回获取的数据集
    return dataset


# 读图像函数
def read_tiff(filename):
    # 打开文件
    dataset = gdal.Open(filename)
    # 获取矩阵的列数
    image_width = dataset.RasterXSize
    # 获取矩阵的行数
    image_height = dataset.RasterYSize
    # 获取仿射矩阵
    image_geo_trans = dataset.GetGeoTransform()
    # 获取图像投影函数
    image_projection = dataset.GetProjection()
    # 将数据写成数组
    image_data = dataset.ReadAsArray(0, 0, image_width, image_height)
    # 删除打开的数据集
    del dataset
    # 返回数据集的投影信息、仿射矩阵、数据矩阵、获取图像宽度、获取图像高度
    return image_projection, image_geo_trans, image_data, image_width, image_height


def transfer_to_tiff(in_image, out_image, image_type):
    # 打开要转换的数据
    dataset = gdal.Open(in_image)
    # 转换数据格式
    gdal.Translate(out_image, dataset, format=image_type)
    # 提示转换完成
    print("转换完成！")


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
    # 读取数据获取影像信息
    data = read_image("S2_20190727San.tif")
