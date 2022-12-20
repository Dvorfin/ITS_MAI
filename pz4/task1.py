

def simple_generator():
    yield 1
    yield 2
    yield 32


def generator_of_even_numbers(max_num):
    for num in range(0, max_num, 2):
        yield num


if __name__ == '__main__':

    for val in generator_of_even_numbers(23):
        print(val)