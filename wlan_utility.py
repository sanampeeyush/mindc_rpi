from logge import generate_log as logger
import subprocess
import requests
import json

logger("app file started")

ssid_file = r"/etc/wpa_supplicant/wpa_supplicant.conf"

content = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=IN

network={
        ssid="NordAirT"
        psk="12345678ps"
        key_mgmt=WPA-PSK
        priority=2
}
network={
        ssid="{ssid}"
        psk="{pwd}"
        key_mgmt=WPA-PSK
        priority=1
}
"""


def fetch():
    try:
        mac = subprocess.run(
            "/home/pi/showmac.sh", shell=True, text=True, stdout=subprocess.PIPE
        ).stdout.strip("\n")

        url = "http://159.89.173.79:8000/creds/{mac}"
        resp = requests.get(url.replace("{mac}", mac))
        result = {}
        if resp.status_code == 200:
            result = json.loads(resp.text)

        if "ssid" in result and "pwd" in result:
            ssid = result.get("ssid")
            pwd = result.get("pwd")

            with open(ssid_file, "w") as f:
                f.write(content.replace("{ssid}", ssid).replace("{pwd}", pwd))
            logger(f"INFO::ssid={ssid} pwd={pwd}")
    except Exception as err:
        logger("ERROR::" + str(err))


def update(ssid, pwd):
    try:
        with open(ssid_file, "w") as f:
            f.write(content.replace("{ssid}", ssid).replace("{pwd}", pwd))
        logger(f"INFO::ssid={ssid} pwd={pwd}")
        return True
    except Exception as err:
        logger("ERROR::" + str(err))
        return False


# if __name__ == "__main__":
#     fetch()
