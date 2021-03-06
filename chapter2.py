# 列表推导
symbols = '$%^&*'
codes = [ord(symbol) for symbol in symbols]
print(codes)


# 使用map&filter也可以做到列表推导的效果，但可读性会差很多，且速度不一定快
symbols = '$%^&*'
codes = [ord(symbol) for symbol in symbols if ord(symbol) > 127]
print(codes)
codes = list(filter(lambda c: c > 127, map(ord, symbols)))
print(codes)


# python2中，列表推导中for关键词之后的赋值操作可能会影响列表推导上下文的同名对量
# eg.
# x = '123'
# dummy = [x for x in 'ABC]
# x >>> 'C'

# python3则不会出现上述情况，表达式内部的变量只在局部起作用


# 列表推导笛卡尔积
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
# tshirts = [(color, size) for size in sizes for color in colors]  顺序看谁在前面
tshirts = [(color, size) for color in colors for size in sizes]
print(tshirts)


# 生成器表达式是更好的选择
# 生成器表达式背后遵守了迭代器的协议，可以逐个地产出元素，而不是先建立一个完整的列表，
# 然后再把这个列表传递到某个构造函数里。生成器表达式显然可以节省内存
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
    print(tshirt)

# 不使用中间变量交换两个变量的值
a = 1
b = 2
a, b = b, a
print(a, b)

# 运用*运算符可以把一个可迭代对象拆开作为函数的参数
print(divmod(20, 8))
t = (20, 8)
print(divmod(*t))

# 可以用*来处理剩下的元素
# 但在平行赋值中， *前缀只能用在一个变量名前面，但是这个变量名可以出现在赋值表达式的任意位置
a, b, *rest = range(5)
print(a, b, rest)
*rest, b, c, d = range(5)
print(rest, b, c, d)


# namedtuple是一个工厂函数，用来创建一个带字段名的元素和一个有名字的类
from collections import namedtuple
# 需要两个参数，一个是类名，另一个是类的各个字段的名字。后者可以是由数个字符串组成的可迭代对象，
# 或者是由空格分隔开的字段名组成的字符串
City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', '36.933', (35.689722, 139.691667))
print(tokyo.name, tokyo.coordinates)

# 除了从普通元祖那里继承来的属性之外，namedtuple还有一些自己专有的属性
# 这个类所有字段名称的元组
print(City._fields)
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
# 接受一个可迭代对象生成一个这个类的实例，效果与City(*delhi_data)一样
delhi = City._make(delhi_data)
# 把namedtuple以collections.OrderedDict的形式返回
for key, value in delhi._asdict().items():
    print(key + ':', value)


# s[a:b:c]即在a和b之间以c为间隔取值，c的值可以为负，意味着反向取值
s = 'bicycle'
print(s[::3])
print(s[::-1])
print(s[::-2])

# 省略 ...
# 如果x是四维数组，那么x[i, ...]就是x[i, :, :, :]的缩写

# 给切片赋值
l = list(range(10))
l[2: 5] = [20, 30]
print(l)
del l[5: 7]
print(l)
l[3::2] = [11, 22]
print(l)
# 即使只有一个值，右边也必须是可迭代对象
l[2::5] = [100]


# 若序列a里的元素是对其他可变对象的引用的话，所得结果不是你所想的
# 如my_list = [[]] * 3 来初始化一个由列表组成的列表，但所得到的列表里包含的三个元素是三个引用
# 且这个三个引用指向的都是同一个列表
# 正确方法如下
board = [['_'] * 3 for i in range(3)]
# 错误方法 [['_'] * 3] * 3


# 对于可变序列，*=不改变序列id，不可变序列则反之
l = [1, 2, 3]
print(id(l))
l *= 2
print(id(l))
t = (1, 2, 3)
print(id(t))
t *= 2
print(id(t))

# t = (1, 2, [30, 40])
# t[2] += [50, 60]
# 上述代码会抛异常，因为tuple不支持对它的元素赋值
# 但最后t变为了(1, 2, [30, 40, 50, 60])
# 改成t[2].extend([50, 60])则不会抛出异常


# list.sort就地排序，不返回元素
# sorted新建一个列表返回

# bisect模块提供了二分查找算法
# bisect.bisect为bisect_right函数的别名，对于值相同的元素，插入到值相同元素的后面
# bisect_left则相反
# 根据一个分数，找到它所对应的成绩
import bisect
def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect.bisect(breakpoints, score)
    return grades[i]
print([grade(score) for score in [33, 99, 77, 70, 89, 90, 100]])

# bisect.insort插入新元素
import random
SIZE = 7
random.seed(1729)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE * 2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)

# 不要过度使用list，针对特定情况选择
# 如存放1000万个浮点数，数组array会高效的多
# 如需要频繁对序列做先进先出的操作，deque的速度应该会更快
# from array import array
# from random import random
# floats = array('d', (random() for i in range(10**7)))
# print(floats[-1])
# fp = open('floats.bin', 'wb')
# floats.tofile(fp)
# fp.close()
# floats2 = array('d')
# fp = open('floats.bin', 'rb')
# floats2.fromfile(fp, 10**7)
# fp.close()
# print(floats2[-1])
# print(floats == floats2)

# memoryview是一个内置类，它能让用户在不复制内容的情况下操作同一个数组中的不同切片
import array
numbers = array.array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)
print(len(memv))
print(memv[0])
memv_oct = memv.cast('B')
print(memv_oct.tolist())
memv_oct[5] = 4
print(numbers)

# 双向队列deque
from collections import deque
dq = deque(range(10), maxlen=10)
print(dq)
dq.rotate(3)
print(dq)
dq.rotate(-4)
print(dq)
dq.appendleft(-1)
print(dq)
dq.extend([11, 22, 33])
print(dq)
dq.extendleft([10, 20, 30, 40])
print(dq)