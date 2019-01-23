# 把函数视作对象
# 可通过别名使用函数，可把函数作为参数传递
def factorial(n):
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n-1)
fact = factorial

# 接受函数为参数，或者把函数作为结果返回的函数是高阶函数
# 如map，sorted等

# 可以用列表推导和生成器表达式代替map和filter
print(list(map(fact, range(6))))
print([fact(i) for i in range(6)])
print(list(map(factorial, filter(lambda n: n % 2, range(6)))))
print([fact(i) for i in range(6) if i % 2])

# all(iterable) 如果iterable的每个元素都是真值，返回True; all([])返回True
# any(iterable) 如果iterable中有一个元素是真值，返回True; any([])返回False

# lambda函数的定义体只能使用纯表达式，即不能复制，不能使用while和try等语句
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=lambda word: word[::-1]))

# 判断对象是否可调用，可以使用callable()

# 函数内省
# 函数对象还有很多属性，使用dir查看
print(dir(factorial))
# 大多属性为python对象共有

# 函数使用__dict__属性存储赋予它的用户属性，这种做法不太常见
def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Custom name'

# 列出常规对象没有而函数有的属性
class C: pass
obj = C()
def func(): pass
print(sorted(set(dir(func)) - set(dir(obj))))

# 从定位参数到仅限关键字参数
def tag(name, *content, cls=None, **attrs):
    """生成一个或多个HTML标签"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)

print(tag('br'))
print(tag('p', 'hello'))
print(tag('p', 'hello', 'world'))
print(tag('p', 'hello', id=33))
print(tag('p', 'hello', 'world', cls='sidebar'))
print(tag(content='testing', name='img'))
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
print(tag(**my_tag))

# 装饰器可以把一个普通函数与框架的请求处理机制结合起来，如果一个函数需要一个person参数
# 则可以从请求中获取那个名称对应的参数，那请求框架怎么知道函数需要哪个参数呢？
# 函数对象有__defaults__属性，是一个元组，里面保存定位参数和关键字参数的默认值
# 仅限关键字参数的默认值在__kwdefaults__属性中
# 参数的名称在__code__属性中

# 可以用inspect提取函数的签名，即获取函数参数的信息
from inspect import signature
sig = signature(tag)
print(sig)
print(str(sig))
for name, param in sig.parameters.items():
    print(param.kind, ':', name, param.default)

# inspect._empty表示没有默认值
# 可以使用bind方法把任意个参数绑定到签名中的形参上

bound_args = sig.bind(**my_tag)
for name, value in bound_args.arguments.items():
    print(name, '=', value)

# 如果删除my_tag中其中一个值，则bind()方法会报错，缺失了相关值

# 函数注解
def clip(text:str, max_len:'int > 0'=80) -> str:
    """
    在max_len前面或后面的第一个空格处截断文本
    :param text:
    :param max_len:
    :return:
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)
    return text[:end].rstrip()

# 注解不会做任何处理，只是存储在函数的__annotations__属性中（一个字典）
# 可以使用signature.return_annotation提取注解

# 支持函数式编程的包
# 普通计算阶乘
from functools import reduce
def fact(n):
    return reduce(lambda a, b: a*b, range(1, n+1))

# 使用operator计算
from operator import mul
def _fact(n):
    return reduce(mul, range(1, n+1))

# operator中有一类函数，能替代从序列中取出元素或读取对象属性的lambda表达式
# 如itemgetter和attrgetter
# itemgetter(1)的作用与lambda fields: fields[1]一样
# 多个参数传给itemgetter，它构建的函数会返回提取的值构成的元组
# itemgetter使用[]运算符，所以可以支持映射和任何实现__getitem__方法的类
# attrgetter类似，如attrgetter('name', 'coord.lat')提取相应字段的值

import operator
print([name for name in dir(operator) if not name.startswith('_')])

# i开头，后面是另一个运算符的那些名称，对应的是增量赋值运算符，如+=，&=等
# 如果第一个参数是可变的，那么这些运算符函数会就地修改它

# methodcaller创建的函数会在对象上调用参数指定的方法
from operator import methodcaller
s = 'The time has come'
upcase = methodcaller('upper')
print(upcase(s))

# 使用functools.partial冻结参数
# 这个函数用于基于一个函数创建一个新的可调用对象，把原函数的某些参数固定，使得参数更少
from functools import partial
triple = partial(mul, 3)
print(triple(7))
print(list(map(triple, range(1, 10))))