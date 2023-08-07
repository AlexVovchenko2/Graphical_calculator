from math import *


def operate(op: str, a: float, b: float = 0) -> float:
	operator = {
		"+": lambda x, y: x+y,
		"-": lambda x, y: x-y,
		"*": lambda x, y: x*y,
		"/": lambda x, y: x/y,
		"^": lambda x, y: x**y,
	}
	return operator[op](a, b)


def mathoper(op: str, arg: float) -> float:
	operator = {
		"ln": lambda x: log(x),
		"sin": lambda x: sin(x),
		"cos": lambda x: cos(x),
		"tg": lambda x: tan(x),
		"ctg": lambda x: cos(x)/sin(x),
		'': lambda x: x
	}
	return operator[op](arg)


def calculate(expr):
	s = expr
	if s[0] == '-':
		s = '0' + s
	s = s.replace(' ', '')   # редактирование строки перед записью в массив токенов (лишние плюсы, замена
	s = s.replace('++', '+')  # унарных минусов на отдельный символ)
	data = list(map(str, s))
	for i in range(1, len(data)):
		if data[i] == '-' and data[i - 1] not in "01234567890)":
			data[i] = '~'
	s = ''.join(data)

	alphabet = "abcdefghijklmnopqrstuvwxyz"
	operands = "+-*/^"
	dijits = "0123456789.~"
	data = []
	num = ''
	function = ''

	for i in s:

		if i in dijits:  # отдельный токен представляет собой либо число, либо знак, причем унарный минус идет вместе с
			num += i  # числом, что позволяет избежать проблем с бинарным и унарным минусом
		elif i in alphabet:
			function += i
		else:
			if len(function) >= 1:
				data.append(function)
			function = ''
			if len(num) != 0:
				data.append(num)
			num = ''
			if i in operands:
				data.append(i)
	if len(function) >= 1:
		data.append(function)
	if len(num) != 0:
		data.append(num)

	for i in range(len(data)):
		c = data[i].count("~")
		data[i] = '-'*(c % 2) + data[i].replace('~', '')

	numbers = []
	operations = []
	priority = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}  # установка приоритетов операций

	for i in range(len(data)):  # алгоритм сортировочной станции, реализованный с помощью двух массивов
		# print(i, ':')
		try:
			check = float(data[i])
		except (ValueError, TypeError):
			check = data[i]

		last = None if len(operations) == 0 else operations[-1]

		# print(numbers, operations, sep='\n')

		if type(check) == float:
			numbers.append(check)
		elif len(operations) == 0:
			operations.append(check)
		elif priority[check] > priority[last]:
			operations.append(check)
		else:
			if last is None:
				continue
			while priority[check] <= priority[last]:
				sign = operations.pop()
				v = numbers.pop()
				u = numbers.pop()
				numbers.append(operate(sign, u, v))
				if len(operations) == 0:
					break
			operations.append(check)

		# print('-----')
		# print(numbers, operations, sep='\n')
		# print('##############')

	while operations:
		sign = operations.pop()
		v = numbers.pop()
		u = numbers.pop()
		numbers.append(operate(sign, u, v))
	return numbers.pop()


# print(calculate("-3*2+15/2"))
# exit()


def brakets_scan(st: str) -> bool:  # проверка на правильность расставленных скобок
	err: bool = False
	pair = {'(': ')'}
	stack = []
	for c in st:
		if c in pair:
			stack.append(pair[c])
		elif c in pair.values():
			if len(stack) == 0 or c != stack.pop():
				err = True
				break
	return err


def solve(expr):
	if brakets_scan(expr):
		raise SyntaxError("invalid brackets")
	s = expr
	s = s.replace(' ', '')
	s = s.replace('++', '+')
	if s[0] == '-':
		s = '0' + s

	if '(' not in s:
		return calculate(expr)

	alphabet = "abcdefghijklmnopqrstuvwxyz"
	cnt_left, cnt_right = 0, 0
	func, function = '', ''
	brakets_expr = ''
	for i in s:                    # чтение строки и запись выражения в скобках в отдельную переменную, причем
		if i in alphabet and cnt_left == cnt_right == 0:  # названия функций тоже записываются. В итоге
			func += i                                 # выражение в скобках заменяется на результат в скобках (если
		elif len(func) != 0:   # перед скобками функция - значение функции) и так же продолжает рекурсивно работать,
			function = func  # пока в выражении не останется скобок, потом вызывается функция calculate, которая
			func = ''        # доделывает оставшееся

		if i == '(':
			cnt_left += 1
		if i == ')':
			cnt_right += 1
		if cnt_left != cnt_right:
			brakets_expr += i
		elif not(cnt_left == cnt_right == 0):
			# print(f"{function}{brakets_expr})")
			# print(mathoper(function, solve(brakets_expr[1:])))
			# print(s)
			s = s.replace(f"{function}{brakets_expr})", str(mathoper(function, solve(brakets_expr[1:]))), 1)
			# print(s)
			break
	return solve(s)


with open("input.txt") as file:
	expression = file.readline().replace('\n', '')
with open("output.txt", 'w') as file:
	file.write(f"{solve(expression)}")

