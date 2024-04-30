def ex1():
    try:
        f = open("foobar.txt")
        s = f.readline()
        i = int(s.strip())
    except OSError as e:
        print(f"OS error {e=}")
    except ValueError as e:
        print(f"Value error: {e=}")
    except Exception as e:
        print(f"Unexpected error: {e=}")
        raise

def ex2():
    try:
        raise NameError("Hey!")
    except NameError:
        print('Yeah!, NameError Hey! entered!')
        raise

def ex3(x, y):
    try:
        result = x / y
    except ZeroDivisionError:
        print("division by zero!")
    else:
        print("result is", result)
    finally:
        print("executing finally clause")

#ex1()
#ex2()
#ex3(2, 1)
#ex3(2, 0)
#ex3("2", "0")
