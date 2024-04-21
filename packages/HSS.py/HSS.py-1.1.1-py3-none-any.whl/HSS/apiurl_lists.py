# APIのURLを定義するモジュール

BASEURL = "https://hss-dev.aknet.tech/v1"
HSS_AP_KEY = [
    "school",
    "users",
    "permission",
    "application"
]

def make_url(mode, id=None):
    """
    Generate an API request URL.

    Parameters:
        mode: Specify the type of request.
        id: Optionally specify the ID to include in the request.

    Return value:
        str: generated URL
    """
    if mode == 0 and id != None:
        id = str(id)
        return BASEURL + "/"+HSS_AP_KEY[mode]+"/"+id
    elif mode ==0 and id is None:
        return BASEURL + "/"+HSS_AP_KEY[mode]+"/"
    elif mode == 1 and id != None:
        id = str(id)
        return BASEURL + "/" + HSS_AP_KEY[mode] + "/" + id
    elif mode ==  2:
        return BASEURL + "/" + HSS_AP_KEY[mode]
    elif mode ==  3:
        return BASEURL + "/" + HSS_AP_KEY[mode] + "/" + id
    else:
        return None