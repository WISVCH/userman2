import requests
from django.conf import settings

LINK_PREFIX = "https://dienst2.ch.tudelft.nl/ldb/people/%d/"


def fetchDienst2(username):
    if not settings.DIENST2_APITOKEN:
        raise Exception("Dienst2 API token not set")

    headers = {"Authorization": "Token " + settings.DIENST2_APITOKEN}
    url = settings.DIENST2_BASEURL + "/ldb/api/v3/people/"
    r = requests.get(url, params={"ldap_username": username}, headers=headers, timeout=5)
    if r.status_code != 200:
        raise Exception(f"Status code {r.status_code}")
    return r


def fetchDienst2Status(username):
    if username in settings.DIENST2_WHITELIST:
        return {"status": "whitelisted", "message": "Whitelisted"}
    try:
        r = fetchDienst2(username)
    except Exception as e:
        return {"error": str(e)}

    json = r.json()
    n = len(json["results"])
    if n == 0:
        ret = {"status": "error", "message": "Username not found in Dienst2"}
    elif n > 1:
        ret = {"status": "error", "message": "Error: %d records matched" % n}
    else:
        person = json["results"][0]
        if person["membership_status"] >= 30:
            ret = {"status": "success", "message": "Active member"}
        else:
            ret = {"status": "warning", "message": "Not an active member"}
        if person["email_forward"]:
            ret["email_forward"] = person["email"]
        ret["id"] = person["id"]
        ret["href"] = LINK_PREFIX % person["id"]
    return ret


def usernameInDienst2(username):
    r = fetchDienst2(username)
    json = r.json()
    return len(json["results"]) > 0
