from time import time
import concurrent.futures
from multiprocessing import cpu_count

def factorize(number):
    results = []
    for i in range(1,number + 1):
        if number % i == 0:
            results.append(i)
    return results

NUMBERS =[128, 255, 99999, 10651060]

if __name__ == '__main__':
    start = time()
    with concurrent.futures.ProcessPoolExecutor(cpu_count()) as executor:
        executor.map(factorize, NUMBERS)

    finish = time()
    print("Execution time:", finish - start)
