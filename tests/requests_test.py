import requests

# response = requests.get("http://www.jugantor.com/news-archive/today-print-edition/editorial/2016/1/2/699")
url = 'https://www.jugantor.com/news-archive/today-print-edition/editorial/2016/1/2/699'
max_redirects = 5

session = requests.Session()
response = session.get(url, allow_redirects=False)

redirect_count = 0
while response.status_code == 302 and redirect_count < max_redirects:
    print(f"Redirecting to: {response.headers['Location']}")
    response = session.get(response.headers['Location'], allow_redirects=False)
    redirect_count += 1

if redirect_count == max_redirects:
    print("Maximum redirects reached")
else:
    print(f"Final URL: {response.text}")