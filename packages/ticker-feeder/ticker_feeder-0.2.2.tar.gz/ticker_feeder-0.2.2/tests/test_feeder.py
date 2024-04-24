from ticker_feeder.feeder import feed

def test_feed():
    assert feed('Hello') == None  # Assuming feed function does not return anything and just prints
