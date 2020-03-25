# coding=gbk
import os

try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr


# 注意一个shp文件为shp,layer,feature,field,attr,

def read_vec_file(vec_file):
    # 支持文件中文路径
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 支持文件中文字段
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # 注册所有驱动
    ogr.RegisterAll()
    # 以只读的方式打开数据源
    ds = ogr.Open(vec_file)
    # 判断文件是否存在
    if ds is None:
        # 提示打开文件成功
        print("打开文件【%s】失败！" % vec_file)
        # 退出当前函数
        return
    # 提示文件打开成功
    print("打开文件【%s】成功！" % vec_file)
    # 获取数据源图层个数
    layer_count = ds.GetLayerCount()
    # 打印文件图层个数
    print("文件【%s】的图层个数为：%d" % (vec_file, layer_count))
    # 通过图层序号获取图层
    layer = ds.GetLayerByIndex(0)
    # 判断图层是否获取成功
    if layer is None:
        # 提示获取图层失败
        print("获取第%d个图层失败！" % 0)
        # 退出当前函数
        return
    # 图层初始化
    layer.ResetReading()
    # 获取图层定义信息
    layer_def = layer.GetLayerDefn()
    # 获取字段个数
    field_count = layer_def.GetFieldCount()
    # 打印字段个数
    print("第【%d】个图层的字段个数为：%d" % (0, field_count))
    # 遍历所有字段
    for i_field in range(field_count):
        # 获取第i字段定义
        field_def = layer_def.GetFieldDefn(i_field)
        # 获取该字段的信息：字段名:字段类型(字段长度, 字段精度)
        print("%s:%s(%d.%d)" % (
        field_def.GetNameRef(), field_def.GetFieldTypeName(field_def.GetType()), field_def.GetWidth(),
        field_def.GetPrecision()))
    # 输出图层中要素的个数
    feature_count = layer.GetFeatureCount()
    # 打印图层要素的个数
    print("第【%d】个图层的要素个数为：%d" % (0, feature_count))
    # 获取图层中的第一个要素
    feature = layer.GetNextFeature()
    while feature is not None:
        print("当前要素的序号为：%d \n属性值为：" % feature.GetFID())
        # 遍历该要素的属性信息
        for i_field in range(field_count):
            # 创建字段定义
            field_def = layer_def.GetFieldDefn(i_field)
            # 构建显示的方式：属性字段名称+属性值
            line = "%s (%s) = " % (field_def.GetNameRef(), ogr.GetFieldTypeName(field_def.GetType()))
            # 判断要素当前字段是否赋值
            if feature.IsFieldSet(i_field):
                # 赋值, 获取该字段的属性值
                line = line + "%s" % (feature.GetFieldAsString(i_field))
            else:
                # 未赋值，当前字段的值为null
                line = line + "(null)"
            # 打印属性字段和属性值
            print("line: " + line)
        # 获取下一个图层要素
        feature = layer.GetNextFeature()
    # 销毁数据源
    ds.Destroy()
    # 提示数据集关闭
    print("数据集关闭！")


if __name__ == '__main__':
    # 获取工程根目录路径
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 打印工程根目录路径
    print("root path:" + root_path)
    # 定义数据路径
    data_path = os.path.abspath(root_path + r'\ShpData')
    # 打印数据路径
    print("data path:" + data_path)
    # 切换到数据目录
    os.chdir(data_path)
    # 定义数据文件名
    vec_file = "gis_osm_transport_free_1.shp"
    # 调用读取shp文件函数
    read_vec_file(vec_file)
