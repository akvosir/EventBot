import requests


def location_request(lat, long):
    url = 'http://127.0.0.1:8000/getByLocation/'
    r = requests.post(url=url,
                      data={
                          'lat': lat,
                          'long': long,
                      })

    return r.json()


def button_request(text):
    url = 'http://127.0.0.1:8000/getByCategory/'
    r = requests.post(url=url,
                      data={
                          'word': text,
                      })
    # print(r)
    return r.json()
