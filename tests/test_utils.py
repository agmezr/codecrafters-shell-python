from app import utils

def test_get_tokens():
    assert ["some", "test"] == utils.split_tokens("some test")
    assert ["'shell hello'"] == utils.split_tokens("'shell hello'")
    assert ["'world     test'"] == utils.split_tokens("'world     test'")
    assert ['hello', 'world'] == utils.split_tokens('hello    world')
    assert ['helloworld'] == utils.split_tokens("hello''world")
    assert ['helloworld'] == utils.split_tokens("hello''world")