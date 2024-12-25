from src.system.message import Message

def test_set_in_quee():
    mock_message = Message()
    def test():
        return "Test"
    
    assert Message.add_process(test) == Proc