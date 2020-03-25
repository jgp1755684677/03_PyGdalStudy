# -*- coding: utf-8 -*-
import os
try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr


def open_vector_file(vec_file):
    # 支持文件中文路径
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 支持文件中文字段
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # 注册驱动
    ogr.RegisterAll()
    # 打开数据源(以只读的方式)
    ds = ogr.Open(vec_file, 0)
    # 判断文件是否打开成功
    if ds is None:
        # 提出文件打开失败
        print("打开文件【%s】失败！" % vec_file)
        # 跳出循环
        return
    # 提示文件打开成功
    print("打开文件【%s】成功！" % vec_file)


if __name__ == '__main__':
    # 获取工程根目录的路径
    root_path = os.path.abspath((os.path.dirname(os.path.dirname(__file__))))
    # 打印工程根目录的路径
    print("root path:" + root_path)
    # 数据文件路径
    data_path = os.path.abspath(root_path + r'\ShpData')
    # 打印数据文件所在路径
    print("data path:" + data_path)
    # 切换数据文件目录
    os.chdir(data_path)
    # 要打开的shp文件名称
    vec_file = "gis_osm_transport_free_1.shp"
    # 调用测试函数
    open_vector_file(vec_file)