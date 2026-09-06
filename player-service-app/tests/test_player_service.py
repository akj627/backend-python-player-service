import sqlite3
import pytest
from player_service import PlayerService

@pytest.fixture
def service():
    """A PlayerService backed by a throwaway in-memory database."""
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE players (playerId TEXT, nameFirst TEXT, birthCountry TEXT);
        INSERT INTO players VALUES ('a1', 'Alice', 'USA');
        INSERT INTO players VALUES ('b2', 'Bob',   'Canada');
        INSERT INTO players VALUES ('c3', 'Carol', 'USA');
        """
    )
    conn.commit()
    return PlayerService(conn)


def test_search_by_player_returns_the_matching_row(service):
    assert service.search_by_player("a1")["nameFirst"] == "Alice"


def test_search_by_player_unknown_id_returns_empty(service):
    assert service.search_by_player("does-not-exist") == {}


def test_search_by_player_is_sql_injectable(service):
    """SHOWCASE: search_by_player builds SQL with str.format(), so a crafted
    id closes the quote and injects `OR '1'='1'`, defeating the filter.

    A safe (parameterised) implementation would treat the whole string as a
    literal id, find no such player, and return {}.
    """
    payload = "' OR '1'='1"

    result = service.search_by_player(payload)

    # Vulnerable behaviour: the WHERE clause matched every row, and the method
    # returns the last one instead of {}.
    assert result != {}, "expected {} for a bogus id - injection was blocked"
    assert result["playerId"] == "c3"


def test_search_by_country_is_sql_injectable(service):
    """SHOWCASE: same flaw in search_by_country - `' OR '1'='1` dumps the
    whole table regardless of the country filter."""
    everyone = service.search_by_country("' OR '1'='1")

    assert len(everyone) == 3  # all rows leaked past the birthCountry filter
