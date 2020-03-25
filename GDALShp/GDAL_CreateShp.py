# -*- coding: utf-8 -*-
import os

try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr
    import osr


def write_vec_file(vec_file):
    # 支持文件中文路径
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 支持文件中文字段
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 定义驱动名称
    drive_name = "ESRI ShapeFile"
    # 通过名称获取驱动
    drive = ogr.GetDriverByName(drive_name)
    # 判断获取驱动是否成功
    if drive is None:
        # 提示获取驱动不可用
        print("【%s】驱动不可以！" % drive_name)
        # 跳出当前函数
        return
    # 创建数据源
    ds = drive.CreateDataSource(vec_file)
    # 判断数据源是否创建成功
    if ds is None:
        # 提示创建文件失败
        print("创建文件【%s】失败" % vec_file)
        # 跳出当前函数
        return
    # 创建空间参考对象
    spatial_ref = osr.SpatialReference()
    # 导入坐标系统
    spatial_ref.ImportFromEPSG(4326)
    # 创建图层
    layer = ds.CreateLayer("TestPolygon", spatial_ref, ogr.wkbPolygon)
    # 判断图层是否创建成功
    if layer is None:
        # 提示图层创建失败
        print("图层创建失败！")
        # 跳出当前函数
        return
    # 定义一个名为FieldID的整型属性
    field_id_def = ogr.FieldDefn("FieldID", ogr.OFTInteger)
    # 创建Field属性（这里的1是干什么的）
    layer.CreateField(field_id_def, 1)
    # 定义名为FieldName的字符型属性
    field_name_def = ogr.FieldDefn("FieldName", ogr.OFTString)
    # 设置FieldName的字符长度为100
    field_name_def.SetWidth(100)
    # 创建字段FieldName
    layer.CreateField(field_name_def, 1)
    print("创建成功")
    # 获取图层定义
    layer_def = layer.GetLayerDefn()
    # 定义三角形要素对象
    feature_triangle = ogr.Feature(layer_def)
    # 设置FieldID字段属性
    feature_triangle.SetField(0, 0)
    # 设置FieldName字段属性
    feature_triangle.SetField(1, "三角形")
    # 创建几何形状
    geom_triangle = ogr.CreateGeometryFromWkt("POLYGON ((0 0, 20 0, 10 15, 0 0))")
    # 设置三角形要素的几何形状
    feature_triangle.SetGeometry(geom_triangle)
    # 将三角形要素对象添加到图层中
    layer.CreateFeature(feature_triangle)
    # 定义矩形要素对象
    feature_rectangle = ogr.Feature(layer_def)
    # 设置FieldId字段属性
    feature_rectangle.SetField(0, 1)
    # 设置FieldName字段属性
    feature_rectangle.SetField(1, "矩形")
    # 创建几何形状
    geom_rectangle = ogr.CreateGeometryFromWkt("POLYGON ((30 0, 60 0, 60 30, 30 30, 30 0))")
    # 设置矩形对象的几何形状
    feature_rectangle.SetGeometry(geom_rectangle)
    # 将矩形要素添加到图层中
    layer.CreateFeature(feature_rectangle)
    # 关闭数据源
    ds.Destroy()
    # 提示适量文件创建完成
    print("数据创建完成！")


if __name__ == '__main__':
    # 获取工程的根目录的路径
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 打印工程根目录的路径
    print("root path:" + root_path)
    # 定义数据文件路径
    data_path = os.path.abspath(root_path + r'\ShpData')
    # 打印数据文件路径
    print("data path:" + data_path)
    # 切换目录
    os.chdir(data_path)
    # 定义创建文件名称
    vec_file = "TestPolygon.shp"
    # 调用矢量文件写函数
    write_vec_file(vec_file)
