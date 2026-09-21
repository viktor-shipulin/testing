import pytest
from get_result import get_result

@pytest.mark.parametrize("score, expected", [
    (-1,  "Некорректный балл"),   
    (30,  "Незачёт"),
    (60,  "Зачёт"),
    (80,  "Хорошо"),
    (95,  "Отлично"),
    (150, "Некорректный балл"),   
])
def test_score_classes(score, expected):
    assert get_result(score, 100) == expected

@pytest.mark.parametrize("attendance, expected", [
    (-1,  "Некорректная посещаемость"),  
    (30,  "Незачёт"),                    
    (65,  "Зачёт"),
    (75,  "Хорошо"),
    (90,  "Отлично"),
    (150, "Некорректная посещаемость"),  
])
def test_attendance_classes(attendance, expected):
    assert get_result(100, attendance) == expected

@pytest.mark.parametrize("score, expected", [
    (0,   "Незачёт"),
    (49,  "Незачёт"),
    (50,  "Зачёт"),
    (69,  "Зачёт"),
    (70,  "Хорошо"),
    (89,  "Хорошо"),
    (90,  "Отлично"),
    (100, "Отлично"),
])
def test_score_boundaries(score, expected):
    assert get_result(score, 100) == expected

@pytest.mark.parametrize("attendance, expected", [
    (0,   "Незачёт"),
    (59,  "Незачёт"),
    (60,  "Зачёт"),
    (69,  "Зачёт"),
    (70,  "Хорошо"),
    (79,  "Хорошо"),
    (80,  "Отлично"),
    (100, "Отлично"),
])
def test_attendance_boundaries(attendance, expected):
    assert get_result(100, attendance) == expected

@pytest.mark.parametrize("score", [-1, 101])
def test_score_invalid_boundaries(score):
    assert get_result(score, 100) == "Некорректный балл"


@pytest.mark.parametrize("attendance", [-1, 101])
def test_attendance_invalid_boundaries(attendance):
    assert get_result(100, attendance) == "Некорректная посещаемость"

@pytest.mark.parametrize("score", ["90", None, [90], 3.5j])
def test_score_type_error(score):
    with pytest.raises(TypeError):
        get_result(score, 80)


@pytest.mark.parametrize("attendance", ["80", None, [80], 3.5j])
def test_attendance_type_error(attendance):
    with pytest.raises(TypeError):
        get_result(90, attendance)

@pytest.mark.parametrize("score, attendance, expected", [
    (95, 75, "Хорошо"),  
    (95, 65, "Зачёт"),   
    (95, 50, "Незачёт"),
    (50, 60, "Зачёт"),   
])
def test_priority_combinations(score, attendance, expected):
    assert get_result(score, attendance) == expected
