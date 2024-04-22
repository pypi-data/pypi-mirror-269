"""
Brief: encrpt DEMO
Author: liufanglong
Date: 2023-03-15
Filename: bdes_2023.py
"""
import requests

host = 'http://10.155.162.47:2146'

def encode(data):
    """encode"""
    url = host + '/bdes/encode'
    res = requests.post(url, data=data, headers={'Content-Type': 'application/octet-stream'})
    return res.content, res.headers['X-MIPS-BDES-META']

def decode(dataEncode, dataEncodeMeta):
    """decode"""
    url = host + '/bdes/decode'
    res = requests.post(url, data=dataEncode, headers={'Content-Type': 'application/octet-stream', \
                        'X-MIPS-BDES-META': dataEncodeMeta})
    return res.content

def main():
    """main"""
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