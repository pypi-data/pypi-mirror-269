import json
import os.path
from collections import defaultdict
from socket import AF_INET, AF_INET6, inet_ntop

from foyou_cli.geoip import geoip_pb2


def geoip(geoip_file, format='json', output=None):
    """解析 geoip dat 并导出

    :param geoip_file: 最新下载地址: https://github.com/v2fly/geoip/releases/latest
    :param format: 输出格式，默认为 json，可选 txt
    :param output: 输出目录，默认为 `geoip_file` 修改后缀为 json 的文件
    :return:
    """
    # noinspection PyUnresolvedReferences
    msg = geoip_pb2.GeoIPList()
    with open(geoip_file, 'rb') as f:
        msg.ParseFromString(f.read())

    data = defaultdict(list)
    for e in msg.entry:
        c = e.country_code
        for i in e.cidr:
            ipaddr = inet_ntop(AF_INET if len(i.ip) == 4 else AF_INET6, i.ip)
            data[c].append(f'{ipaddr}/{i.prefix}')

    if output is None:
        output = os.path.splitext(os.path.basename(geoip_file))[0]
        output = f'{output}.{format}'
    with open(output, 'w') as f:
        if format == 'txt':
            a = True
            for k, v in data.items():
                if a:
                    a = False
                else:
                    f.write('\n\n')
                f.write(f'# {k}\n')
                b = True
                for i in v:
                    if b:
                        b = False
                    else:
                        f.write('\n')
                    f.write(f'{i}')
        else:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    return 'Done!'


def main():
    geoip('C:/Users/foyou/Desktop/cn.dat', 'txt')


if __name__ == '__main__':
    main()
