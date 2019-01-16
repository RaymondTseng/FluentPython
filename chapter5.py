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