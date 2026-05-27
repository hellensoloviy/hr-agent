# tests/test_handlers.py
from agent.handlers import list_open_positions, get_candidate

def test_list_positions_returns_all():
    result = list_open_positions()
    assert result["count"] == 3

def test_get_candidate_by_name():
    result = get_candidate("Alice Chen")
    assert result["found"] == True
    assert result["candidate"]["id"] == "C001"

def test_get_candidate_not_found():
    result = get_candidate("Nobody Here")
    assert result["found"] == False