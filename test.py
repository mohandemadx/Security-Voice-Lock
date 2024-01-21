import threading
import time

def my_function():
    print("Thread started")
    time.sleep(5)  # Simulate a long-running task
    print("Thread finished")

if __name__ == '__main__':
    # Code to run before the thread
    print("Before thread")

    # Start the thread
    thread = threading.Thread(target=my_function)
    thread.start()

    # Wait for the thread to finish
    thread.join()

    # Code to run after the thread
    print("After thread")
