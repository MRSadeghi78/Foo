import requests


def ip_to_location(ip_address):
    """
    :param ip_address:
    :return:
    """
    try:
        response = requests.get("http://ip-api.com/json/" + ip_address)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None


def get_client_ip(request) -> str:
    x_real_ip = request.headers.get("X-Real-IP")
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_real_ip:
        return x_real_ip
    elif x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.client.host
