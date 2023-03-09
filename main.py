from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import numpy as np
# import boto3

# BUCKET_NAME = os.getenv("BUCKET_NAME")


# s3 = boto3.resource('s3')

def extract_fake_news():

    types = ['fake','misleading-en']

    title_list,date_list = [],[]

    for type_ in types:

        link = f"https://dfrac.org/en/topic/{type_}/page/1/"
        req = requests.get(link)
        soup = BeautifulSoup(req.content, 'html.parser')
        total_pages = soup.find('span',class_= 'pages').get_text()[-3:]

        for page in range(1, 5):
            pg = requests.get(f"https://dfrac.org/en/topic/{type_}/page/{page}/")
            cnt = pg.content
            soup = BeautifulSoup(cnt, 'html.parser')
            headlines = soup.find_all('div', class_= 'td-module-meta-info')
            for headline in headlines:
                try:
                    title = headline.find('h3').get_text()
                    title = title.strip()
                    title = title.replace("- Read Fact Check", "").replace(" Read- Fact Check", "").replace("Read, Fact-Check", "").replace("Fact Check: ", "").replace(" Read Fact Check", "").replace("Fact Check-", "").replace('FactCheck:', '').replace('Fact-Check: ', '')
                    title = title.strip()
                    title_list.append(title)
                except:
                    title_list.append(np.NaN)

                try:
                    date = headline.find('time').get_text()  
                    datetime_obj = datetime.datetime.strptime(date, "%B %d, %Y")
                    date = datetime_obj.strftime("%Y-%m-%d")
                    date_list.append(date)
                except:
                    date_list.append(np.NaN)

    data = {
        'Title' : title_list,
        'Date' : date_list,
        'Target' : ["false"] * len(date_list)
    }

    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    df = df.sort_values(by='Date', ascending=False)

    from_date = df['Date'].iloc[0]
    to_date = df['Date'].iloc[-1]

    return {
            "data" : df,
            "to_date" : to_date,
            "from_date" : from_date
        }


def lambda_handler():

    df, to_date, from_date = extract_fake_news().values()


    # df.to_json(f"{from_date.replace('-','_')}_{to_date.replace('-','_')}_dfrac.json") 

    date_from_db = '2023-02-28'

    filtered_df = df[df['Date'] > date_from_db]
    print(filtered_df.shape)

    return {
        'statusCode': 200,
        'body': json.dumps('Pipeline has been executed successfully')
    }

x = lambda_handler()