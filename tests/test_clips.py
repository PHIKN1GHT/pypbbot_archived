from pypbbot.utils import Clips

def test_clips_add():
    a = Clips.from_str('wad')
    b = Clips.from_str('cd')
    assert str(a + b) == 'wadcd'
    assert str(123 + b) == '123cd'
    assert str(b + 0.0) == 'cd0.0'
    print(Clips()+a)
    
