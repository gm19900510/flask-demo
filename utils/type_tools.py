import struct

type_dict = {
    '424D': 'bmp',
    'FFD8FF': 'jpg',
    '2E524D46': 'rm',
    '4D546864': 'mid',
    '89504E47': 'png',
    '47494638': 'gif',
    '49492A00': 'tif',
    '41433130': 'dwg',
    '38425053': 'psd',
    '2142444E': 'pst',
    'FF575043': 'wpd',
    'AC9EBD8F': 'qdf',
    'E3828596': 'pwl',
    '504B0304': 'zip',
    '52617221': 'rar',
    '57415645': 'wav',
    '41564920': 'avi',
    '2E7261FD': 'ram',
    '000001BA': 'mpg',
    '000001B3': 'mpg',
    '6D6F6F76': 'mov',
    '7B5C727466': 'rtf',
    '3C3F786D6C': 'xml',
    '68746D6C3E': 'html',
    'D0CF11E0': 'doc/xls',
    '255044462D312E': 'pdf',
    'CFAD12FEC5FD746F': 'dbx',
    '3026B2758E66CF11': 'asf',
    '5374616E64617264204A': 'mdb',
    '252150532D41646F6265': 'ps/eps',
    '44656C69766572792D646174653A': 'eml'
}
max_len = len(max(type_dict, key=len)) // 2


def get_filetype_by_file(filename):
    # 读取二进制文件开头一定的长度
    with open(filename, 'rb') as f:
        byte = f.read(max_len)
    # 解析为元组
    byte_list = struct.unpack('B' * max_len, byte)
    # 转为16进制
    code = ''.join([('%X' % each).zfill(2) for each in byte_list])
    # 根据标识符筛选判断文件格式
    result = list(filter(lambda x: code.startswith(x), type_dict))
    if result:
        return type_dict[result[0]]
    else:
        return 'unknown'


def get_filetype_by_stream(stream):
    byte = stream.read(max_len)
    # 解析为元组
    byte_list = struct.unpack('B' * max_len, byte)
    # 转为16进制
    code = ''.join([('%X' % each).zfill(2) for each in byte_list])
    # 根据标识符筛选判断文件格式
    result = list(filter(lambda x: code.startswith(x), type_dict))
    if result:
        return type_dict[result[0]]
    else:
        return 'unknown'
