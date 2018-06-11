import requests


class ApiManager:
    files = []  # cached list of files

    def __init__(self, host, apikey):
        self.headers = {"X-Api-Key": apikey}
        self.base_url = "http://{}/api".format(host.replace("http://", ""))

    def list_files(self):
        r = requests.get(self.base_url + "/files", headers=self.headers)
        try:
            self.files = r.json()["files"]
            self.files.sort(key=lambda f: f["date"], reverse=False)
            results = ["{}".format(f["display"]) for f in self.files]
            return "\n".join(results)
        except Exception as e:
            return "Error loading files: {}".format(e)

    def get_file(self, filename):
        if len(self.files) == 0:
            self.list_files()
        return "TODO"

    def get_status(self):
        r = requests.get(self.base_url + "/job", headers=self.headers)
        try:
            resp = r.json()
            curr_file = resp["job"]["file"]
            progress = resp["progress"]
            return "Printing {} is {} percent done. {} minutes left.".format(
                curr_file["display"],
                progress["completion"],
                round(float(progress["printTimeLeft"]) / 60, 2),
            )
        except Exception as e:
            return "Could not get current status: {}".format(e)
