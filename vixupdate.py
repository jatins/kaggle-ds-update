import requests
import csv
import time
from datetime import datetime, timedelta

# Constants
BASE_URL = 'https://www.nseindia.com/api/historical/vixhistory'
START_YEAR = 2004
INTERVAL_DAYS = 90  # 3 months
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.nseindia.com/reports-indices-historical-vix',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'cookie': '_ga=GA1.1.12859391.1716649700; defaultLang=en; ak_bmsc=911F0617FEBC3C3918E87EE383A0FB6C~000000000000000000000000000000~YAAQqZUjFxbO4z2QAQAAYlPifRizZ/eDd1B6+tkCCamhqUd0L0nyUZW8kzpwU/vxqrNdQ/CDKcUC20kOir45eW96h5L7QZ8laeP7fXlns2d8y9Tdt8g3WogslOpims4H0zTbrNX+yJeR8lASwxqKV9JXe3rVklVLswLuo6Zoiass5JBMR5CmRpp9vu5x6d4jJCYBPtOlWoQ06MrPECqRA42aoL8wurQF8297+qxWX9YqdlXW7JVzKfodkWtfzs9CmEaWeTIOxWDp4vjL7oEK8/To+I0cfzWVaYnAS615h4oXs4nnR26vYH+AI+0FRZ+WUwu7KXQrnmmkq+ecaXGIo9cRCaI2He/AoADYVvcR5VeOCslcTuFigBh1BDtzRaZ1DEUshB6fZFRpNHJTmKX1ytyqtrvpST4bA1/xvDwj+5Jqegdc8J9rauZ1LR/LL8Xv/F6M7NSYZkcnwg0rIJiOwZ0=; AKA_A2=A; _abck=DB7CAB5F29F96A31A5332F28C7A48FA5~0~YAAQRpYRYFDur1eQAQAAwRghfgzPuKbFru4MrBxwujqMyCWVQIrQ7rzy7YrYBjPwkLYPsPShC6ydq7ujVknkWbg7RCojq9MebWIikXzT8ncyelvQj1MU4Le6uYmXe9vRx7z+PRr+UKlizjNIF5uTSUNpdy96cqLMm09Hj8aL53vwCMGTJDG9H9Tr85uw4DQLoLpY0UTOcYkh8qGepjPaI5T2aQ4TeBkKKWHD19NoChZnb7HtlUwL81INsHruWpplstiXLcMsb0sOFXAn50vLSKUSrLjml/elsHfiLiBFDjlqGA/fUTYHw4SGHBFfOn7Inp+hEtubli53PWAt6gHOytRSXEA0ki8Nq8N3BauvIhxZcj+z0+rqPdZRgkKIVM6j/xZiraVpd9P4Ztp2tRVHIl4Z72GBOwXNJ7U=~-1~-1~-1; nsit=jPD1yZEqvFUogtwKqmIlbz06; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcyMDEwMzA5NywiZXhwIjoxNzIwMTEwMjk3fQ.2XIWHH7S6cI9NTrPN03ZfwZb96_UJUGU8FJwpmIyyn4; bm_sz=383B71592CE48438E0C650400D4A7222~YAAQRpYRYEX1r1eQAQAAM1UifhiC5L+kDcdnEdGgZDbIQSfsVEfFocJdospR1rzIwBGMX6r1+2YFrfwK5xikAYK6ZlsEBwLBiw+DIxheW2XONqNrfHDO7P8yq2XX9t+3neLDK/eWjkhb7sIQOzy8lTvUh3YrFNbo/6+3wexTuA2W+THnBDAG0qy7pAeeMEwMAwi3bJvtVXFProZv8OQno5DnhI+Q1s1A9bwB/rNkt22ZQku7rkFBXN8N2Gu61F4F+c7WvqVxbJSc/9EKIfx7izIfBbs74mYowGdFgdteohwE9zbAv8kgV6GdHX3Nm1+TC1gI73S7HX7GarX4E2i2l/IVYrm4JMcPmoie+SZTnv/dRW4hlN1UZt74pu3uqZEdQ+3SS7+/JXCWqIDqO+MubfmU5obYxd98zfkGJ6c=~3682616~4404531; _ga_87M7PJ3R97=GS1.1.1720103017.9.1.1720103098.46.0.0; bm_sv=DFA765233CAC2C67AF609B17FF33DC72~YAAQRpYRYLL1r1eQAQAAomkifhi3VNgjvokK22+GaVjUGNOUWCycrZZhfO0VAvluMkrjRGeBPvPckvisjMDQMU9g9WfMk3wjYLUGozibNzLbQhIRROOGV9tQjeNOqyp2eIR+fFi3ZV4ETPohixpwIx1RNSxxoEgkklxSDdDYH2/kWSZOsRi32Al1mn+GiKcgk58ws5o4SFC4A68rsemeXw/nlG1E4Dq2POgLiWHqUukltf1s9u3iRbtykK2ptvq6UbcM~1; RT="z=1&dm=nseindia.com&si=7f1748a9-4921-4dfe-a597-8a491432cb82&ss=ly7cx9uf&sl=3&se=8c&tt=301&bcn=%2F%2F684d0d44.akstat.io%2F&ld=1rts&nu=kpaxjfo&cl=1wsc"'  # Replace with your actual cookie
}

def fetch_data(start_date, end_date, retries=3):
    url = f'{BASE_URL}?from={start_date}&to={end_date}'
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.json()['data']
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    print(f"Failed to fetch data for {start_date} to {end_date} after {retries} retries")
    return []

def generate_date_ranges(start_year, interval_days):
    current_date = datetime(start_year, 7, 2)
    end_date = datetime.today()

    while current_date < end_date:
        start_str = current_date.strftime('%d-%m-%Y')
        next_date = current_date + timedelta(days=interval_days)
        end_str = (next_date - timedelta(days=1)).strftime('%d-%m-%Y')
        yield start_str, end_str
        current_date = next_date

def get_and_save(filename):
    all_data = []
    for start_date, end_date in generate_date_ranges(START_YEAR, INTERVAL_DAYS):
        print(f"Fetching VIX data from {start_date} to {end_date}")
        data = fetch_data(start_date, end_date)
        if data:
            all_data.extend(data)
    
    if all_data:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=all_data[0].keys())
            writer.writeheader()
            writer.writerows(all_data)
        print(f"Data saved to {filename}")
    else:
        print("No data fetched.")

