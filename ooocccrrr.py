# coding=utf-8
import os

os.system('python ./kkkk.py')  # 运行识别程序

ocr_result = "2_123_231"

result = str(ocr_result).split('_')
print(result[0])
print(int(result[1]))
x = int(result[1])
print x
print(result[2])
print(int(124.0))
print("---------")
tttt = 'data = ""'
aa = tttt.split('"')
print aa[0]
print aa[1]
print aa[2]
if len(aa[1]) == 0:
    print (222)
print("0---------------")
ocr_result = 'data = ""'
result = str(ocr_result).split('"')[1]

print(len(result))
if len(result) == 0:
    print("ERROR")
result = result.split("_")
print len("data = ''")

# print(result[0])
# print(result[1])
# print(result[2])
for i in range(28):
    print i

print("===================")
strr = "27_678876868874.51"
aa = strr.split('_')
print aa
