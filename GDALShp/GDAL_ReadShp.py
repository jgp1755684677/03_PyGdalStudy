# coding=gbk
import os

try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr


# ע��һ��shp�ļ�Ϊshp,layer,feature,field,attr,

def read_vec_file(vec_file):
    # ֧���ļ�����·��
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # ֧���ļ������ֶ�
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # ע����������
    ogr.RegisterAll()
    # ��ֻ���ķ�ʽ������Դ
    ds = ogr.Open(vec_file)
    # �ж��ļ��Ƿ����
    if ds is None:
        # ��ʾ���ļ��ɹ�
        print("���ļ���%s��ʧ�ܣ�" % vec_file)
        # �˳���ǰ����
        return
    # ��ʾ�ļ��򿪳ɹ�
    print("���ļ���%s���ɹ���" % vec_file)
    # ��ȡ����Դͼ�����
    layer_count = ds.GetLayerCount()
    # ��ӡ�ļ�ͼ�����
    print("�ļ���%s����ͼ�����Ϊ��%d" % (vec_file, layer_count))
    # ͨ��ͼ����Ż�ȡͼ��
    layer = ds.GetLayerByIndex(0)
    # �ж�ͼ���Ƿ��ȡ�ɹ�
    if layer is None:
        # ��ʾ��ȡͼ��ʧ��
        print("��ȡ��%d��ͼ��ʧ�ܣ�" % 0)
        # �˳���ǰ����
        return
    # ͼ���ʼ��
    layer.ResetReading()
    # ��ȡͼ�㶨����Ϣ
    layer_def = layer.GetLayerDefn()
    # ��ȡ�ֶθ���
    field_count = layer_def.GetFieldCount()
    # ��ӡ�ֶθ���
    print("�ڡ�%d����ͼ����ֶθ���Ϊ��%d" % (0, field_count))
    # ���������ֶ�
    for i_field in range(field_count):
        # ��ȡ��i�ֶζ���
        field_def = layer_def.GetFieldDefn(i_field)
        # ��ȡ���ֶε���Ϣ���ֶ���:�ֶ�����(�ֶγ���, �ֶξ���)
        print("%s:%s(%d.%d)" % (
        field_def.GetNameRef(), field_def.GetFieldTypeName(field_def.GetType()), field_def.GetWidth(),
        field_def.GetPrecision()))
    # ���ͼ����Ҫ�صĸ���
    feature_count = layer.GetFeatureCount()
    # ��ӡͼ��Ҫ�صĸ���
    print("�ڡ�%d����ͼ���Ҫ�ظ���Ϊ��%d" % (0, feature_count))
    # ��ȡͼ���еĵ�һ��Ҫ��
    feature = layer.GetNextFeature()
    while feature is not None:
        print("��ǰҪ�ص����Ϊ��%d \n����ֵΪ��" % feature.GetFID())
        # ������Ҫ�ص�������Ϣ
        for i_field in range(field_count):
            # �����ֶζ���
            field_def = layer_def.GetFieldDefn(i_field)
            # ������ʾ�ķ�ʽ�������ֶ�����+����ֵ
            line = "%s (%s) = " % (field_def.GetNameRef(), ogr.GetFieldTypeName(field_def.GetType()))
            # �ж�Ҫ�ص�ǰ�ֶ��Ƿ�ֵ
            if feature.IsFieldSet(i_field):
                # ��ֵ, ��ȡ���ֶε�����ֵ
                line = line + "%s" % (feature.GetFieldAsString(i_field))
            else:
                # δ��ֵ����ǰ�ֶε�ֵΪnull
                line = line + "(null)"
            # ��ӡ�����ֶκ�����ֵ
            print("line: " + line)
        # ��ȡ��һ��ͼ��Ҫ��
        feature = layer.GetNextFeature()
    # ��������Դ
    ds.Destroy()
    # ��ʾ���ݼ��ر�
    print("���ݼ��رգ�")


if __name__ == '__main__':
    # ��ȡ���̸�Ŀ¼·��
    root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # ��ӡ���̸�Ŀ¼·��
    print("root path:" + root_path)
    # ��������·��
    data_path = os.path.abspath(root_path + r'\ShpData')
    # ��ӡ����·��
    print("data path:" + data_path)
    # �л�������Ŀ¼
    os.chdir(data_path)
    # ���������ļ���
    vec_file = "gis_osm_transport_free_1.shp"
    # ���ö�ȡshp�ļ�����
    read_vec_file(vec_file)
