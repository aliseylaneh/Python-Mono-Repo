import multiprocessing
import os
from typing import Any, List


def info():
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def return_index(database: List[dict[str, Any]], row: dict[str, Any]) -> int:
    for index, record in enumerate(database):
        if record["ID"] == row["ID"]:
            return index
    raise ValueError("Record not found")


def deposit(database: List[dict[str, Any]], row: dict[str, Any], amount: int, lock: multiprocessing.Lock):
    with lock:
        index = return_index(database=database, row=row)
        if database[index]["VERSION"] != row["VERSION"]:
            row["VERSION"] = database[index]["VERSION"]
            print("Incompatible version detected !!")
            print("Retry SELECT ...")
            return
        database[index]["BALANCE"] += amount
        print("BELOW MODULE IS UPDATING:")
        info()
        print(f"{row['ID']} updated.")
        database[index]["VERSION"] += 1
        print(database[index])


def user_one(database, process_lock: multiprocessing.Lock):
    deposit(database=database, row={
        "ID": 5545,
        "BALANCE": 233143144,
        "VERSION": 1
    }, amount=20, lock=process_lock)


def user_two(database, process_lock: multiprocessing.Lock):
    deposit(database=database, row={
        "ID": 5545,
        "BALANCE": 233143144,
        "VERSION": 1
    }, amount=30, lock=process_lock)


if __name__ == '__main__':
    # TODO contains error
    manager = multiprocessing.Manager()
    DATABASE = manager.list([
        {"ID": 5545, "BALANCE": 10, "VERSION": 1}
    ])
    lock = multiprocessing.Lock()

    process_one = multiprocessing.Process(target=user_one, args=(DATABASE, lock))
    process_two = multiprocessing.Process(target=user_two, args=(DATABASE, lock))
    process_one.start()
    process_two.start()
    process_one.join()
    process_two.join()
