from bluospy.player import Player

import pytest
from unittest.mock import MagicMock, call
import urllib.parse


@pytest.fixture
def player():
    return Player("192.168.1.1")


# Mocking the REST API calls
@pytest.fixture
def mock_requests(mocker):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    return mock_get


def test_init(player):
    assert player.url == "192.168.1.1"
    assert player.port == 11000
    assert player.base_url == "http://192.168.1.1:11000"


def test_status(player, mock_requests, mocker):
    mocker.patch(
        "bluospy.player.status_xml_to_dict", return_value={"status": "playing"}
    )
    assert player.status == {"status": "playing"}
    mock_requests.assert_called_once_with("http://192.168.1.1:11000/Status")


def test_get_volume(player, mock_requests, mocker):
    mocker.patch("bluospy.player.volume_xml_to_dict", return_value={"level": 10})
    assert player.get_volume() == {"level": 10}
    mock_requests.assert_called_once_with("http://192.168.1.1:11000/Volume")


def test_set_volume(player, mock_requests, mocker):
    mocker.patch("bluospy.player.volume_xml_to_dict", return_value={"level": 20})
    assert player.set_volume(level=20) == {"level": 20}
    mock_requests.assert_called_once_with(
        "http://192.168.1.1:11000/Volume?tell_slaves=1&mute=0&level=20"
    )


def test_volume_up_down(player, mock_requests, mocker):
    mocker.patch("bluospy.player.volume_xml_to_dict", return_value={"level": 22})
    assert player.volume_up() == {"level": 22}
    mock_requests.assert_called_with(
        "http://192.168.1.1:11000/Volume?tell_slaves=1&mute=0&db=2"
    )

    mocker.resetall()
    mocker.patch("bluospy.player.volume_xml_to_dict", return_value={"level": 18})
    assert player.volume_down() == {"level": 18}
    mock_requests.assert_called_with(
        "http://192.168.1.1:11000/Volume?tell_slaves=1&mute=0&db=-2"
    )


def test_play(player, mock_requests, mocker):
    mocker.patch(
        "bluospy.player.status_xml_to_dict", return_value={"status": "playing"}
    )
    assert player.play(stream="http://example.com/song.mp3") == {"status": "playing"}
    stream_arg = urllib.parse.quote("http://example.com/song.mp3")
    mock_requests.assert_called_once_with(
        f"http://192.168.1.1:11000/Play?url={stream_arg}"
    )


def test_pause_toggle(player, mock_requests, mocker):
    mocker.patch("bluospy.player.status_xml_to_dict", return_value={"status": "paused"})
    assert player.pause(toggle=True) == {"status": "paused"}
    mock_requests.assert_called_once_with("http://192.168.1.1:11000/Pause?toggle=1")


def test_stop(player, mock_requests, mocker):
    mocker.patch(
        "bluospy.player.status_xml_to_dict", return_value={"status": "stopped"}
    )
    assert player.stop() == {"status": "stopped"}
    mock_requests.assert_called_once_with("http://192.168.1.1:11000/Stop")


def test_shuffle_repeat(player, mock_requests, mocker):
    # Shuffle
    mocker.patch("bluospy.player.status_xml_to_dict", return_value={"shuffle": True})
    player.shuffle = True
    assert player.shuffle == True
    mock_requests.assert_has_calls(
        [
            call("http://192.168.1.1:11000/Shuffle?state=1"),
            call("http://192.168.1.1:11000/Status"),
        ]
    )

    # Repeat
    mocker.resetall()
    mocker.patch("bluospy.player.status_xml_to_dict", return_value={"repeat": True})
    player.repeat = True
    assert player.repeat == True
    mock_requests.assert_has_calls(
        [
            call("http://192.168.1.1:11000/Repeat?state=1"),
            call("http://192.168.1.1:11000/Status"),
        ]
    )
