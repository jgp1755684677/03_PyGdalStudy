# coding=gbk
import os
import pandas as pd

try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr
    import osr


# 读取Excel表格数据
def read_excel(filename, sheet_name):
    # 使用pandas读取excel文件
    df = pd.read_excel(filename, sheet_name)
    # 读取df行标志的值
    cols = df.columns.values
    # 打印读取到的数据
    print("输出列标题:", cols)
    # 读取df的值
    data = df.values
    # 格式化打印所有获取的值
    print("获取到的所有的值为:\n{0}".format(data))
    # 返回行标志的值和数据
    return cols, data


def excel_to_shp(data_path, excel_name, vec_file, lng_col_num, lat_col_num):
    # 支持文件中文路径
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 支持文件中文字段
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 获取ESRI ShapeFile文件驱动
    driver = ogr.GetDriverByName("ESRI ShapeFile")
    # 切换到数据路径下
    os.chdir(data_path)
    # 判断该路径下是否存在该文件名的shp文件
    if os.path.exists(vec_file):
        # 存在,删除该shp文件
        driver.DeleteDataSource(vec_file)
    # 创建shp文件
    out_ds = driver.CreateDataSource(vec_file)
    # 判断文件是否创建成功
    if out_ds is None:
        # 提示创建文件失败
        print("创建文件失败！")
        # 跳出当前函数
        return
    # 创建空间参考对象
    spatial_ref = osr.SpatialReference()
    # 导入投影信息
    spatial_ref.ImportFromEPSG(4326)
    # 获取shp文件名称，并将其赋值给图层
    layer_name = os.path.splitext(vec_file)[0]
    # 创建输出的图层
    out_layer = out_ds.CreateLayer(layer_name, spatial_ref, ogr.wkbPoint)
    # 获取excel的表头及数据
    cols, data = read_excel(excel_name, "Sheet1")
    # 获取表头的个数
    cols_count = len(cols)
    # 遍历多有的表头并创建属性字段
    for i_col in range(cols_count):
        # 定义字段的名称
        field_name = cols[i_col]
        # 字段定义
        field_def = ogr.FieldDefn(field_name, ogr.OFTString)
        # 定义字段的长度
        field_def.SetWidth(100)
        # 将字段定义添加到图层中
        out_layer.CreateField(field_def)
    # 获取输出图层定义
    out_layer_def = out_layer.GetLayerDefn()
    # 获取数据的行数
    rows_count = len(data)
    # 遍历所有的数据并写入的字段中
    for i_row in range(rows_count):
        # 获取经度
        lng = float(data[i_row][lng_col_num - 1])
        # 获取纬度
        lat = float(data[i_row][lat_col_num - 1])
        # 创建点要素对象
        feature_point = ogr.Feature(out_layer_def)
        for i_col in range(cols_count):
            # 获取字段名
            field_name = cols[i_col]
            # 获取每个字段对应的值
            field_value = data[i_row][i_col]
            # 给字段赋值
            feature_point.SetField(field_name, field_value)
        # 定义要素为点对象
        geom_point = ogr.Geometry(ogr.wkbPoint)
        # 添加点的坐标值
        geom_point.AddPoint(lng, lat)
        # 设置点的几何信息
        feature_point.SetGeometry(geom_point)
        # 创建要素点
        out_layer.CreateFeature(feature_point)
    # 销毁数据源
    out_ds.Destroy()
    # 提示数据转换成功
    print("Excel 转点成功！")


if __name__ == '__main__':
    # 获取工程根目录的路径
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 打印工程根目录的路径
    print("root path:", root_path)
    # 定义数据文件路径
    data_path = os.path.abspath(root_path + r'\ShpData')
    # 打印数据文件路径
    print("data path:", data_path)
    # 切换目录
    os.chdir(data_path)
    # 定义要转换的Excel文件名
    excel_name = "SpecialTownList.xlsx"
    # 定义输出shp的文件名
    vec_file = "SpecialTown.shp"
    # 调用excel转shp文件函数
    excel_to_shp(data_path, excel_name, vec_file, 23, 24)
