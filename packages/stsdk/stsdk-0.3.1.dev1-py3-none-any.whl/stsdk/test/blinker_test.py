import threading

from stsdk.test.constants import started


@started.connect
def say_hello(sender):
    def hhh():
        thread_name = threading.current_thread().name
        print("Current thread name:", thread_name, "sender:", sender)
        # started.send("我草")

    threading.Thread(target=hhh).start()


fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)
    started.send(x)
