import pytest
from app import app
from player_service import PlayerService
import sqlite3

@pytest.fixture
def service():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE players (playerId TEXT, nameFirst TEXT, birthCountry TEXT);
        INSERT INTO players VALUES ('a1', 'Alice', 'USA');
        INSERT INTO players VALUES ('b2', 'Bob', 'Canada');
    """)
    conn.commit()
    return PlayerService(conn)

def test_get_all_players_list(service):
    lst = service.get_all_players()
    assert len(lst) == 2
    assert lst[0]["nameFirst"] == "Alice"
    assert lst[1]["nameFirst"] == "Bob"

def test_search_by_player_found(service):
    assert service.search_by_player("a1")["nameFirst"] == "Alice"

def test_search_by_player_not_found(service):
    assert service.search_by_player("zzz") == {}
