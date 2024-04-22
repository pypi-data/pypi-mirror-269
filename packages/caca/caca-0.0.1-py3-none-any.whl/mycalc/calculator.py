import numpy as np

def array_arithmetic(arr1, arr2, operator):
    if operator == '+':
        return arr1 + arr2
    elif operator == '-':
        return arr1 - arr2
    elif operator == '*':
        return arr1 * arr2
    elif operator == '/':
        return np.divide(arr1, arr2, out=np.zeros_like(arr1), where=arr2!=0)

def arange(start, stop=None, step=1):
    """
    주어진 시작(start), 끝(stop), 및 간격(step)에 따라 일정한 간격으로 숫자가 채워진 배열을 생성합니다.
    :param start: 시작 값
    :param stop: 끝 값 (생략 가능)
    :param step: 간격 (기본값: 1)
    :return: 생성된 배열
    """
    if stop is None:
        start, stop = 0, start
    length = max(int(np.ceil((stop - start) / step)), 0)
    return [start + step * i for i in range(length)]