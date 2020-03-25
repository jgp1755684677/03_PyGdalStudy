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


# ��ȡExcel�������
def read_excel(filename, sheet_name):
    # ʹ��pandas��ȡexcel�ļ�
    df = pd.read_excel(filename, sheet_name)
    # ��ȡdf�б�־��ֵ
    cols = df.columns.values
    # ��ӡ��ȡ��������
    print("����б���:", cols)
    # ��ȡdf��ֵ
    data = df.values
    # ��ʽ����ӡ���л�ȡ��ֵ
    print("��ȡ�������е�ֵΪ:\n{0}".format(data))
    # �����б�־��ֵ������
    return cols, data


def excel_to_shp(data_path, excel_name, vec_file, lng_col_num, lat_col_num):
    # ֧���ļ�����·��
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # ֧���ļ������ֶ�
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # ע�����е�����
    ogr.RegisterAll()
    # ��ȡESRI ShapeFile�ļ�����
    driver = ogr.GetDriverByName("ESRI ShapeFile")
    # �л�������·����
    os.chdir(data_path)
    # �жϸ�·�����Ƿ���ڸ��ļ�����shp�ļ�
    if os.path.exists(vec_file):
        # ����,ɾ����shp�ļ�
        driver.DeleteDataSource(vec_file)
    # ����shp�ļ�
    out_ds = driver.CreateDataSource(vec_file)
    # �ж��ļ��Ƿ񴴽��ɹ�
    if out_ds is None:
        # ��ʾ�����ļ�ʧ��
        print("�����ļ�ʧ�ܣ�")
        # ������ǰ����
        return
    # �����ռ�ο�����
    spatial_ref = osr.SpatialReference()
    # ����ͶӰ��Ϣ
    spatial_ref.ImportFromEPSG(4326)
    # ��ȡshp�ļ����ƣ������丳ֵ��ͼ��
    layer_name = os.path.splitext(vec_file)[0]
    # ���������ͼ��
    out_layer = out_ds.CreateLayer(layer_name, spatial_ref, ogr.wkbPoint)
    # ��ȡexcel�ı�ͷ������
    cols, data = read_excel(excel_name, "Sheet1")
    # ��ȡ��ͷ�ĸ���
    cols_count = len(cols)
    # �������еı�ͷ�����������ֶ�
    for i_col in range(cols_count):
        # �����ֶε�����
        field_name = cols[i_col]
        # �ֶζ���
        field_def = ogr.FieldDefn(field_name, ogr.OFTString)
        # �����ֶεĳ���
        field_def.SetWidth(100)
        # ���ֶζ�����ӵ�ͼ����
        out_layer.CreateField(field_def)
    # ��ȡ���ͼ�㶨��
    out_layer_def = out_layer.GetLayerDefn()
    # ��ȡ���ݵ�����
    rows_count = len(data)
    # �������е����ݲ�д����ֶ���
    for i_row in range(rows_count):
        # ��ȡ����
        lng = float(data[i_row][lng_col_num - 1])
        # ��ȡγ��
        lat = float(data[i_row][lat_col_num - 1])
        # ������Ҫ�ض���
        feature_point = ogr.Feature(out_layer_def)
        for i_col in range(cols_count):
            # ��ȡ�ֶ���
            field_name = cols[i_col]
            # ��ȡÿ���ֶζ�Ӧ��ֵ
            field_value = data[i_row][i_col]
            # ���ֶθ�ֵ
            feature_point.SetField(field_name, field_value)
        # ����Ҫ��Ϊ�����
        geom_point = ogr.Geometry(ogr.wkbPoint)
        # ��ӵ������ֵ
        geom_point.AddPoint(lng, lat)
        # ���õ�ļ�����Ϣ
        feature_point.SetGeometry(geom_point)
        # ����Ҫ�ص�
        out_layer.CreateFeature(feature_point)
    # ��������Դ
    out_ds.Destroy()
    # ��ʾ����ת���ɹ�
    print("Excel ת��ɹ���")


if __name__ == '__main__':
    # ��ȡ���̸�Ŀ¼��·��
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # ��ӡ���̸�Ŀ¼��·��
    print("root path:", root_path)
    # ���������ļ�·��
    data_path = os.path.abspath(root_path + r'\ShpData')
    # ��ӡ�����ļ�·��
    print("data path:", data_path)
    # �л�Ŀ¼
    os.chdir(data_path)
    # ����Ҫת����Excel�ļ���
    excel_name = "SpecialTownList.xlsx"
    # �������shp���ļ���
    vec_file = "SpecialTown.shp"
    # ����excelתshp�ļ�����
    excel_to_shp(data_path, excel_name, vec_file, 23, 24)
