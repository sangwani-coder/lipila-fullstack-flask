"""
    test_momo.py
    Lipila Fee Collection System
    Creator: Sangwani P. Zyambo

    unittests for the momo class.
"""

# test the Momo class
def test_momo_class_passing_numbers(momo):
    m1 = '0965604023'
    m2 = '0765604023'
    m3 = '0971892260'
    m4 = '0771892260'

    network = momo

    np1 = network.get_network(m1)
    assert np1 == 'mtn'
    np2 = network.get_network(m2)
    assert np2 == 'mtn'
    np3 = network.get_network(m3)
    assert np3 == 'airtel'
    np4 = network.get_network(m4)
    assert np4 == 'airtel'

def test_momo_class_failing_numbers(momo):
    m1 = '09656040230'
    m2 = '076560402'
    m3 = '0991892260'
    m4 = '0951892260'

    network = momo

    np1 = network.get_network(m1)
    assert np1 == 'Unknown'
    np2 = network.get_network(m2)
    assert np2 == 'Unknown'
    np3 = network.get_network(m3)
    assert np3 == 'Unknown'
    np4 = network.get_network(m4)
    assert np4 == 'Unknown'