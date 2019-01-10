from collections import abc
# 用instance而不是type判定某个数据是不是广义上的映射类型
my_dict = {}
print(isinstance(my_dict, abc.Mapping))

# 如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的
# 原子不可变数据类型（str, bytes和数值类型）都是可散列类型，frozenset也是可散列的
# 如果一个自定义对象实现了__eq__方法，并且在方法中用到了这个对象的内部状态的话
# 那么只有当所有这些内部状态都是不可变的情况下，这个对象才是可散列的

# 字典构造方法
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('two', 2), ('one', 1), ('three', 3)])
e = dict({'three': 3, 'one': 1, 'two': 2})

# 字典推导
DIAL_CODES = [(86, 'China'), (91, 'India'), (1, 'United States')]
country_code = {country: code for code, country in DIAL_CODES}
print(country_code)
country_code = {code: country.upper() for code, country in DIAL_CODES if code < 66}
print(country_code)

# 用setdefault处理找不到的键
my_dict = {'one': [1], 'two': [2], 'three': [3]}
key = 'four'
value = 4
# 不好的实现
# occurences = my_dict.get(key, [])
# occurences.append(value)
# my_dict[key] = occurences
# print(my_dict)
# 好的实现
my_dict.setdefault(key, []).append(value)
print(my_dict)

# 某个键不在映射里，但仍希望通过这个这个键读取到默认值
# 两种方法 --> 1. defaultdict 2.自定义dict，实现__missing__方法
import collections
index = collections.defaultdict(list)
index[key].append(value)
print(index)
# defaultdict中的default_factory只会在__getitem__中调用
# 如d为defaultdict，d[k]会调用default_factory，d.get(k)会返回None

# __missing__方法同样只会被__getitem__调用
class StrKeyDict0(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    # 没有使用k in dict这种方法，因为会导致__contains__被递归调用
    # python3中dict.keys()返回的是一个视图，在视图中查找元素速度很快
    # python2中则返回的是一个列表，速度较慢
    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()

# collections.OrderedDict
# 有序字典，添加键的时候会保持顺序，因此键的迭代次序是一致的
# popitem方法默认删除并返回的是字典里的最后一个元素
# popitem(last=False)调用，它删除并返回第一个被添加进去的元素

# collections.ChainMap
# 可以容纳数个不同的映射对象（多个字典），然后在进行键查找操作的时候
# 这些对象会被当做一个整体逐个查找，直到键被找到为止
from collections import ChainMap
import builtins
pylookup = ChainMap(locals(), globals(), vars(builtins))
print(pylookup)

# collections.Counter
# 为键准备一个整数计数器，每次更新一个键的时候都会增加这个计数器
from collections import Counter
ct = collections.Counter('abracasfasfaz')
print(ct)
ct.update('aaaaaaaaaaazz')
print(ct)
print(ct.most_common(2))

# collections.UserDict
# 把标准的dict用纯python又实现了一遍，用来让用户继承写子类
class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    # data是一个dict的实例，是UserDict中最终存储数据的地方
    def __contains__(self, item):
        return str(key) in self.data

    def __setitem__(self, key, value):
        self.data[key] = value

# 不可变映射类型
# 比如不能让用户错误地修改某个映射
# MappingProxyType，如果给这个类一个映射，它会返回一个只读的映射视图
# 如果对原映射作出了改动，我们通过这个视图可以观察到，但无法通过这个视图对原映射作出修改
from types import MappingProxyType
d = {1: 'A'}
d_proxy = MappingProxyType(d)
print(d_proxy)
print(d_proxy[1])
# 这句报错
# d_proxy[2] = 'x'
d[2] = 'B'
print(d_proxy[2])

# 集合
# a | b 返回合集
# a & b 返回交集
# a - b 返回差集
# 使用这些中缀云算法让代码更易读，节约时间
# 若a和b中任意一个对象已是集合，则a.intersection(b)求交集
# 比 a & b求交集更高效

# {1, 2, 3}这种字面量句法相比于构造方法set([1, 2, 3])更高效
# 因为python必须从set这个名字来查询构造方法，然后新建一个列表，把列表传入构造函数中
# 但前者会使用BUILD_SET的字节码来创建集合

# 同样有集合推导的概念

