import threading
import time


def main():
    raise Exception("terrible")


t = threading.Thread(target=main)
t.start()
t.join()
print(t.is_alive())
