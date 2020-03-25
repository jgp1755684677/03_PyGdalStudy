import sys
import os
from osgeo import gdal
from osgeo import ogr


def update_shp(path):
    # 支持文件中文路径
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 支持文件中文字段
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # 注册所有驱动
    ogr.RegisterAll()
    # 获取ESRI ShapeFile文件格式驱动
    driver = ogr.GetDriverByName("ESRI ShapeFile")
    # 以可写的方式打开文件(数据源)
    ds = driver.Open(path, 1)
    # 判断数据源是否打开
    if ds is None:
        # 提示打开成功
        print("未成功打开数据源:%s" % path)
        # 有错误退出程序, sys.exit(0) 无错误退出程序
        sys.exit(1)
    # 获取图层
    layer = ds.GetLayerByIndex(0)
    # 获取图层空间信息(投影)
    spatial_ref = layer.GetSpatialRef()
    # 输出图层中的要素个数
    print("该图层的要素个数为: %d" % layer.GetFeatureCount(0))
    # 输出属性表结构信息
    print("属性表结构信息")
    # 获取图层定义
    layer_def = layer.GetLayerDefn()
    # 获取字段索引
    field_name_index = layer_def.GetFieldIndex("FieldName")
    # 通过字段索引获取字段定义
    field_name_def = layer_def.GetFieldDefn(field_name_index)
    # 创建x字段定义,使字段类型与FieldName相同
    x_def = ogr.FieldDefn('x', field_name_def.GetType())
    # 设置x字段的长度
    x_def.SetWidth(100)
    # 将字段添加到图层中
    layer.CreateField(x_def, 1)
    # 获取FieldID字段的索引
    field_id_index = layer_def.GetFieldIndex("FieldID")
    # 获取filedID字段的定义
    field_id_def = layer_def.GetFieldDefn(field_id_index)
    # 创建字段y,字段类型与FieldID相同
    y_def = ogr.FieldDefn('y', field_id_def.GetType())
    # 设置y字段的长度
    y_def.SetWidth(32)
    # 设置y字段的精度
    y_def.SetPrecision(6)
    # 将字段添加到图层中
    layer.CreateField(y_def, 1)
    # 获取图层中的第一个要素
    feature = layer.GetNextFeature()
    # 遍历图层中的所有要素
    while feature is not None:
        # 获取要素FieldName字段的值
        field_name = feature.GetFieldAsString("FieldName")
        # 打印要素字段的值
        print("FieldName:", field_name)
        # 获取要素FiledID字段的值
        field_id = feature.GetFieldAsDouble("FieldID")
        # 打印FieldID字段的值
        print("FieldID:", field_id)
        # 将FieldName对应的属性值赋值给字段x
        feature.SetField("x", field_name)
        # 将FieldID对应的属性值赋值给字段y
        feature.SetField("y", field_id)
        # 重新设置当前要素(刷新)
        layer.SetFeature(feature)
        # 获取下一个要素
        feature = layer.GetNextFeature()
    # 销毁数据源
    ds.Destroy()


if __name__ == '__main__':
    # 获取工程根目录的路径
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 打印工程根目录的路径
    print("root path:" + root_path)
    # 获取数据文件的路径
    data_path = os.path.abspath(root_path + r'\ShpData')
    # 打印数据文件的路径
    print("data path:" + data_path)
    # 切换目录
    os.chdir(data_path)
    # 需要更新文件的名称
    vec_file = "TestPolygon.shp"
    # 调用更新适量文件函数
    update_shp(vec_file)
