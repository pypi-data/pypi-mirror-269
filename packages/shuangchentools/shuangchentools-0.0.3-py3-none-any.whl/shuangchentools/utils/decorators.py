"""
@Author: shuangchen
@Time: 2024/3/25
@File: decorators.py
@Description: 常用装饰器
"""

import time
import functools
from typing import Callable, Any


def retry(retries: int = 3, delay: float = 1) -> Callable:
    """
    捕获到异常重试
    :param retries: 最大重试次数
    :param delay: 重试间隔时间
    """
    assert retries >= 1 and delay >= 0

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, retries + 1):

                try:
                    print(f'Running ({i}): {func.__name__}()')
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries:
                        print(f'Error: {repr(e)}.')
                        print(f'"{func.__name__}()" failed after {retries} retries.')
                        break
                    else:
                        print(f'Error: {repr(e)} -> Retrying...')
                        time.sleep(delay)

        return wrapper
    return decorator


def get_time(func: Callable) -> Callable:
    """
    记录函数执行时间
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time: float = time.perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = time.perf_counter()

        print(f'"{func.__name__}()" took {end_time - start_time:.3f} seconds to execute')
        return result
    return wrapper
