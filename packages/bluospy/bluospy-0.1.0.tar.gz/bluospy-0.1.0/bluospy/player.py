import requests
import urllib.parse

from bluospy.utils import (
    playlist_xml_to_dict,
    status_xml_to_dict,
    error_dict,
    volume_xml_to_dict,
)


class Player:

    def __init__(self, url, port=11000):
        self.url = url
        self.port = port
        self.base_url = f"http://{url}:{port}"

    @property
    def status(self):
        res = requests.get(self.base_url + "/Status")
        if res.status_code == 200:
            return status_xml_to_dict(res.text)
        else:
            return error_dict(res.status_code, res.text)

    # Volume control

    def get_volume(self):
        res = requests.get(self.base_url + "/Volume")
        if res.status_code == 200:
            vdict = volume_xml_to_dict(res.text)
            return vdict
        else:
            return error_dict(res.status_code, res.text)

    def set_volume(
        self, level=None, abs_db=None, db=None, tell_slaves=True, mute=False
    ):
        # Check that exactly one of the options is provided
        nargs = sum(opt is not None for opt in [level, abs_db, db])
        if nargs > 1:
            raise ValueError("At most one of level, abs_db or db should be provided")

        options = f"tell_slaves={int(tell_slaves)}&mute={int(mute)}"
        api_call = f"/Volume?{options}"
        if level is not None:
            api_call += f"&level={level}"
        if abs_db is not None:
            api_call += f"&abs_db={abs_db}"
        if db is not None:
            api_call += f"&db={db}"

        res = requests.get(self.base_url + api_call)

        if res.status_code == 200:
            vdict = volume_xml_to_dict(res.text)
            return vdict
        else:
            return error_dict(res.status_code, res.text)

    @property
    def volume(self):
        vdict = self.get_volume()
        if "level" in vdict:
            return vdict["level"]
        else:
            return vdict

    @volume.setter
    def volume(self, level):
        self.set_volume(level=level)

    def volume_up(self):
        return self.set_volume(db=2)

    def volume_down(self):
        return self.set_volume(db=-2)

    @property
    def mute(self):
        vdict = self.get_volume()
        if "mute" in vdict:
            return bool(vdict["mute"])
        else:
            return vdict

    @mute.setter
    def mute(self, muted):
        self.set_volume(mute=muted)

    # Playback control

    def play(self, seek=None, stream=None):

        stream_arg = ""
        if stream is not None:
            stream_arg = "url=" + urllib.parse.quote(stream)
        seek_arg = ""
        if seek is not None:
            seek_arg = f"seek={seek}"

        args = "?" + "&".join([arg for arg in [stream_arg, seek_arg] if arg != ""])
        res = requests.get(self.base_url + "/Play" + args)
        if res.status_code == 200:
            return status_xml_to_dict(res.text)
        else:
            return error_dict(res.status_code, res.text)

    def pause(self, toggle=False):
        res = requests.get(self.base_url + "/Pause?" + f"toggle={int(toggle)}")
        if res.status_code == 200:
            return status_xml_to_dict(res.text)
        else:
            return error_dict(res.status_code, res.text)

    def stop(self):
        res = requests.get(self.base_url + "/Stop")
        if res.status_code == 200:
            return status_xml_to_dict(res.text)
        else:
            return error_dict(res.status_code, res.text)

    def skip(self):
        res = requests.get(self.base_url + "/Skip")
        if res.status_code == 200:
            return status_xml_to_dict(res.text)
        else:
            return error_dict(res.status_code, res.text)

    def back(self):
        res = requests.get(self.base_url + "/Back")
        if res.status_code == 200:
            return status_xml_to_dict(res.text)
        else:
            return error_dict(res.status_code, res.text)

    @property
    def shuffle(self):
        return bool(self.status["shuffle"])

    @shuffle.setter
    def shuffle(self, shuffled):
        res = requests.get(self.base_url + "/Shuffle?" + f"state={int(shuffled)}")
        if res.status_code != 200:
            raise RuntimeError(f"HTTP{res.status_code}: {res.text}")

    @property
    def repeat(self):
        return bool(self.status["repeat"])

    @repeat.setter
    def repeat(self, rstate):
        res = requests.get(self.base_url + "/Repeat?" + f"state={int(rstate)}")
        if res.status_code != 200:
            raise RuntimeError(f"HTTP{res.status_code}: {res.text}")
