from my_depression_library.analyze import analyze_depression_test

def test_analyze_depression_test():
    # Test cases
    assert analyze_depression_test([1, 2, 3, 4, 5]) == "Mild depression"
    assert analyze_depression_test([5, 5, 5, 5, 5]) == "Moderate depression"
    assert analyze_depression_test([10, 10, 10, 10, 10]) == "Severe depression"
