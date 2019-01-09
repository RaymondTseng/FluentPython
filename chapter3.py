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