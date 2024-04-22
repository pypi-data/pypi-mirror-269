"""
Brief: encrpt DEMO
Author: lintianwei01
Date: 2021-06-29
Filename: bdes.py
"""
import requests

host = "http://10.153.133.21:8018"

def encode(data):
    "description"
    url = host + '/bdes/encode?binary=1'
    res = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})
    return res.content, res.headers['X-MIPS-BDES-META']


def decode(dataEncode, dataEncodeMeta):
    "description"
    url = host + '/bdes/decode?binary=1'
    res = requests.post(url, data=dataEncode, 
                        headers={'Content-Type': 'application/octet-stream', 'X-MIPS-BDES-META': dataEncodeMeta})
    return res.content


def main():
    "description"
    data = requests.get('http://cp01-rd-dongdong01.epc.baidu.com:8100/img/test.jpg').content
    print len(data)
    dataEncode, dataEncodeMeta = encode(data)
    print len(dataEncode)
    print (dataEncodeMeta)
    dataDecode = decode(dataEncode, dataEncodeMeta)
    print len(dataDecode)
    print 'data == dataDecode: ', data == dataDecode


if __name__ == '__main__':
    main()
