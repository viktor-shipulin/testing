import pytest
from game import (
    RIDDLES,
    parse_number,
    check_entry,
    check_riddle,
    count_correct,
    passed_riddles,
    is_win_final,
)

def test_parse_number_valid():
    assert parse_number("1") == 1
    assert parse_number("5") == 5
    assert parse_number("9") == 9


def test_check_entry_pass():
    assert check_entry(1) == True
    assert check_entry(6) == True


def test_check_entry_lose():
    assert check_entry(7) == False
    assert check_entry(9) == False


def test_check_riddle_correct():
    assert check_riddle("снег", "снег") == True


def test_check_riddle_ignores_case_and_spaces():
    assert check_riddle("СНЕГ", "снег") == True
    assert check_riddle("  снег  ", "снег") == True


def test_count_correct_all_right():
    answers = [correct for question, correct in RIDDLES]
    assert count_correct(answers, RIDDLES) == 6


def test_passed_riddles_enough():
    assert passed_riddles(4) == True
    assert passed_riddles(6) == True


def test_is_win_final_win():
    assert is_win_final(1) == True
    assert is_win_final(7) == True


def test_is_win_final_lose():
    assert is_win_final(8) == False
    assert is_win_final(9) == False

def test_parse_number_letters():
    with pytest.raises(ValueError):
        parse_number("abc")


def test_parse_number_empty():
    with pytest.raises(ValueError):
        parse_number("")


def test_parse_number_too_big():
    with pytest.raises(ValueError):
        parse_number("10")


def test_parse_number_zero():
    with pytest.raises(ValueError):
        parse_number("0")

def test_check_riddle_wrong_answer():
    assert check_riddle("дождь", "снег") == False


def test_count_correct_some_wrong():
    answers = ["снег", "да", "мокрых", "сон", "неверно", "все"]
    assert count_correct(answers, RIDDLES) == 3


def test_passed_riddles_not_enough():
    assert passed_riddles(3) == False
    assert passed_riddles(0) == False