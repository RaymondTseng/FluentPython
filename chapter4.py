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

# 处理UnicodeEncodeError
city = 'São Paulo'
# 报错，cp437无法编码ã
# print(city.encode('cp437'))
# 跳过无法编码的字符
print(city.encode('cp437', errors='ignore'))
# 把无法编码的字符替换成?
print(city.encode('cp437', errors='replace'))
# 把无法编码的字符替换成XML实体
print(city.encode('cp437', errors='xmlcharrefreplace'))

# UnicodeDecodeError类似

# 如何找出字节序列的编码，不能，必须有人告诉你
# 但可以通过试探和分析找出编码
# 例如，如果b'\x00'字节经常出现，那么可能是16位或32位编码
# 可以使用chardet侦测文件编码

# b'\xff\xfe'位BOM(byte-order mark)，即字节序标记，指明编码时使用Intel CPU的小字节序
# 在小字节序中，各个码位的最低有效字节在前面，如字母'E'的码位为U+0045，十进制数为69
# 则在字偏移的第二位和第三位编码为69和0，在大字节序中，则为0和69
# 为了避免混淆，utf-16编码要在编码文本前加上不可见字符，即U+FFEF
# 因为按照设计，U+FFEF不存在，所以字节序列b'\xff\xfe'必定是不可见字符
# utf-16le显示指明使用小字节序，utf-16be使用大字节序
# 如果文件使用utf-16编码，而且没有BOM，那么假定它使用大字节序编码
# 但在Intel x86中有很多文件用的是不带BOM的小字节序编码

# utf-8不管设备使用哪一种字节序，生成的字节序列始终一直，不需要BOM
# 但某些windows应用，依然会在utf-8编码的文件前添加BOM
# Excel会根据有没有BOM确定文件是不是utf-8编码，否则使用windows代码页(codepage)编码
# utf-8的U+FFEF字节序列是'b\xef\xbb\xbf'
# 但python不会根据有无BOM确定文件是否为utf-8编码

# 如果打开文件时没有指定encoding参数，默认值由locale.getpreferredencoding()提供
# 如果设定了PYTHONENCODING环境变量，sys.stdout/stdin/stderr的编码使用设定的值，否则，继承所在的控制台
# 如果输入输出到重定向文件，使用locale.getpreferredencoding()
# sys.getfilesystemencoding()用于编码文件名，若文件名为字节序列，则不经改动传给OS API

s1 = 'café'
s2 = 'cafe\u0301'
print(s1, s2)
print(len(s1), len(s2))
print(s1 == s2)
# \u0301是combining acute accent，加在e后面得到é
# 可以使用unicodedate.normalize函数提供的Unicode规范化
from unicodedata import normalize
# NFC，使用最少码位构成等价的字符串
print(len(normalize('NFC', s1)), len(normalize('NFC', s2)))
# NFD，把组合字符分称基字符和单独的组合字符
print(len(normalize('NFD', s1)), len(normalize('NFD', s2)))

# 保存文本前，最好使用normalize清洗字符串

# NFKC, NFKD对“兼容字符”有影响
# Unicode为各个字符提供“规范化”的码位，但是为了兼容现有的标准，有些字符会出现多次
# 各个兼容字符会被替换成一个或多个“兼容分解”的字符，即便这样有些格式损失，但仍是首选表述


# 对于只包含latin1字符的字符串s，s.casefold()和s.lower()得到的结果往往一样
# 除了μ和德语Eszett
# 自python3.4起，s.casefold()和s.lower()得到不同结果的有116个码位
# Unicode6.3命名了110122个字符，只占了了0.11%

# 极端规范化，去掉变音符号
import unicodedata
import string
def shave_marks(txt):
    norm_txt = unicodedata.normalize('NFD', txt)
    # 过滤所有组合记号
    shaved = ''.join(c for c in norm_txt if unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)

def shave_marks_latin(txt):
    norm_txt = unicodedata.normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue
        keepers.append(c)
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)

# 不同的区域采用排序规则有所不同，葡萄牙语等很多语言按照拉丁字母表排序
# 但重音符号和下加符对排序几乎没什么影响，如cajá视作caja
# 在Python中，非ASCII文本的标准排序方式是使用locale.strxfrm函数
# 这个函数会把字符串转换成适合所在区域进行比较的形式

# import locale
# locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
# fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
# sorted_fruits = sorted(fruits, key=locale.strxfrm)
# print(sorted_fruits)
# 上面这段代码在GNU/Linux中可以但在Windows中会报错
# 原因可能是windows未实现所设区域，也可能是区域名称拼写错误
# locale.setlocale()不推荐在代码中使用，应该在进程启动时设置好
# 操作系统必须支持区域设置
# 必须知道如何拼写区域名称
# 操作系统的制作者必须正确实现了所设的区域

# 使用PyUCA进行Unicode排序
import pyuca
coll = pyuca.Collator()
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=coll.sort_key)
print(sorted_fruits)
# pyuca只支持python3
# 使用Collator构造方法可以定制排序方式，默认使用自带的allkeys.txt
# 即Unicode6.3.0的Default Unicode Collation Element Table

# Unicode标准提供了一个完整的数据库，不仅包括码位与字符名称之间的映射
# 还有各个字符的元数据，以及字符之间的关系
# 如字符是否可以打印，是否是字母，是否是数字
# unicodedata中有几个函数可以获取字符的元数据
# 如字符在标准官方名称是不是组合字符，以及符号对应人类的可读数字

# re模块对Unicode的支持并不充分，regex的目的是取代它

# 支持字符串和字符序列的双模式API
# 然后根据类型展现不同的行为，re和os中就有这样的函数

import re
# 字符串模式
re_numbers_str = re.compile(r'\d+')
re_words_str = re.compile(r'\w+')
# 字节序列模式
re_numbers_bytes = re.compile(rb'\d+')
re_words_bytes = re.compile(rb'\w+')

# 泰达米尔数字
text_str = ("Ramanujan saw \u0be7\u0bed\u0be8\u0bef"
            " as 1729 = 1³ + 12³ = 9³ + 10³.")
text_bytes = text_str.encode('utf-8')
print('Text', repr(text_str), sep='\n  ')
print('Numbers')
# 可以匹配泰达米尔数字和ASCII数字
print('  str  :', re_numbers_str.findall(text_str))
# 只能匹配ASCII数字
print('  bytes  :', re_numbers_bytes.findall(text_bytes))
print('Words')
print('  str  :', re_words_str.findall(text_str))
print('  bytes  :', re_words_bytes.findall(text_bytes))

# 对于os也有类似的函数
# os.listdir('.')返回字符串
# os.listdir(b'.')返回字节序列

# python3.1中引入surrogateescape把每个无法解码的字节替换成
# Unicode中U+DC00到U+DCFF之间的码位，这些码位没有被分配字符


