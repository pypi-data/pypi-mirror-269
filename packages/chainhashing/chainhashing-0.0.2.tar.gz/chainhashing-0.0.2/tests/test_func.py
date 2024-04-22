from chainhashing.example import Maxim

def test_maxim():
    maxim = Maxim()
    assert maxim.say_hello() == "Hello, my name is Maxim!"
