# 字符的标识，即码位
# 字符的具体表述取决于所用的编码

# 把码位转换成字节序列的过程叫编码
# 把字节序列转换成码位的过程是解码

# 4个Unicode字符
s = 'cafe'
print(len(s))
# 使用utf-8把str对象编码成bytes对象
b = s.encode('utf-8')
# bytes对象以b开头
print(b)
b = b.decode('utf-8')
print(b)

# python3的str类型基本相当于python2的unicode类型
# python2.6的bytes类型，就是str类型
# 但python3的bytes类型却不是把str类型换个名称那么简单

# bytes或bytearray对象的各个元素是介于0~255（含）之间的整数
cafe = bytes('café', encoding='utf-8')
print(cafe)
# cafe[0]返回一个元素
print(cafe[0])
# cafe[:1]返回bytes对象
print(cafe[:1])
# bytearray对象没有字面量句法
cafe_arr = bytearray(cafe)
print(cafe_arr)
print(cafe_arr[-1:])

# 特别的，对于str类型来说，s[i]返回一个元素，而s[i:i+1]返回一个相同类型的序列

# 各字节的值可能会使用下列三种不同的方式显示
# 可打印的ASCII范围内的字节
# 制表符、换行符、回车符和对应的字节，使用转移序列\t,\n,\r和\\
# 其他字节的值，使用十六进制转义序列。eg. \x00是空字节

# 可以使用字符串方法处理二进制序列，如endswith, replace, strip等，除了有几个方法不行
# re模块中的正则表达式函数也能处理二进制序列
# 二进制序列有个方法是str没有的，fromhex，作用是解析十六进制数字对
print(bytes.fromhex('31 4B CE A9'))

# 使用缓冲类对象(bytes, bytearray, memoryview, array.array)构建二进制序列
import array
numbers = array.array('h', [-2, -1, 0, 1, 2])
octets = bytes(numbers)
print(octets)

# 使用缓冲类对象创建bytes或bytearray，始终复制源对象中的字节序列
# 与之相反，memoryview对象允许在二进制数据结构之间共享内存

# struct模块能把打包的字节序列转换成不同类型字段组成的元组，或者反向操作
