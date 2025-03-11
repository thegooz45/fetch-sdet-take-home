import subprocess
import json
import pytest

## a series of tests! the goals are to test happy path, as well as some negative tests!
# starting first with happy path!

def run_geoloc_util(*args):
    # note, i'd rather put the key in a constant, but i believe python doesn't do this?
    # ideally this sensitive data would be in a config file, or environment variable
    """run the geoloc script, and return the output """
    command = ["python", "geolog_util.py", "--apikey", "f897a99d971b5eef57be6fafa0d83239"] + list(args)
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout, result.stderr

def test_valid_city_state():
    stdout, stderr = run_geoloc_util("--locations", "Las Vegas, NV")
    assert "Las Vegas" in stdout
    assert "latitude" in stdout
    assert "longitude" in stdout
    assert stderr == ""

def test_valid_zip():
    stdout, stderr = run_geoloc_util("--locations", "10001")
    assert "New York" in stdout
    assert "latitude" in stdout
    assert "longitude" in stdout
    assert stderr == ""

def test_multiple_locations():
    stdout, stderr = run_geoloc_util("--locations", "10001", "Las Vegas, NV")
    assert "New York" in stdout
    assert "Las Vegas" in stdout
    assert "latitude" in stdout
    assert "longitude" in stdout
    assert stderr == ""

# negative tests!

def test_invalid_location():
    stdout, stderr = run_geoloc_util("--locations", "BajaBlast, Mountain Dew")
    assert "Invalid location" in stderr
    assert stdout == ""

def test_unsupported_states():
    stdout, stderr = run_geoloc_util("--locations", "Honolulu, HI")
    assert "hawaii and alaska are not supported!" in stderr
    assert stdout == ""

def test_missing_api_key():
    command = run_geoloc_util("--locations", "Las Vegas, NV")
    result = subprocess.run(command, capture_output=True, text=True)
    assert "error: the following arguments are required: --apikey" in result.stderr