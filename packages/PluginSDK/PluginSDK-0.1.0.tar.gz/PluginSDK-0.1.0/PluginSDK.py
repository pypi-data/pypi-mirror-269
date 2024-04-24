import requests
from urllib.parse import quote

class PluginSDK:
    def __init__(self, server_address):
        self.server_address = server_address
    
    def get(self, relative_url):
        url = self.server_address + relative_url
        response = requests.get(url)
        return response.text
    
    def get_plugin_ver(self):
        return self.get("/api/SDKVer")
    
    def get_playing(self):
        return self.get("/api/isPlaying").lower() == 'true'
    
    def get_play_audio(self):
        return self.get("/api/playAudio").lower() == 'true'
    
    def get_mm_ver(self):
        return self.get("/api/nowVer")
    
    def get_mm_running(self):
        return self.get("/api/runningDirectory")
    
    def get_play_audio_key(self):
        return self.get("/api/playAudioKey")
    
    def get_toggle_stream_key(self):
        return self.get("/api/toggleStreamKey")
    
    def get_vb_volume(self):
        volume = self.get("/api/VBvolume")
        try:
            return int(volume)
        except ValueError:
            return 0
    
    def get_volume(self):
        volume = self.get("/api/volume")
        try:
            return int(volume)
        except ValueError:
            return 0
    
    def get_tips_volume(self):
        volume = self.get("/api/tipsvolume")
        try:
            return int(volume)
        except ValueError:
            return 0
    
    def get_list_view_info(self, response_type):
        if response_type not in ["json", "xml", "text"]:
            raise ValueError("responseType must be one of 'json', 'xml', 'text'")
        return self.get(f"/api/listViewInfo?type={response_type}")
    
    def play_audio(self, audio_name):
        if not audio_name:
            raise ValueError("audioName cannot be empty")
        encoded_audio_name = quote(audio_name)
        return self.get(f"/api/playAudio?name={encoded_audio_name}")

