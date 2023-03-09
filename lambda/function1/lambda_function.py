from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import numpy as np
import boto3

BUCKET_NAME = os.getenv("BUCKET_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")
MONGODB_URL = os.getenv("MONGODB_URL")

s3 = boto3.resource('s3')

def extract_fake_news():

    types = ['fake','misleading-en']

    title_list,date_list = [],[]

    for type_ in types:

        link = f"https://dfrac.org/en/topic/{type_}/page/1/"
        req = requests.get(link)
        soup = BeautifulSoup(req.content, 'html.parser')
        total_pages = soup.find('span',class_= 'pages').get_text()[-3:]

        for page in range(1, int(total_pages)):
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


def lambda_handler(event, context):

    df, to_date, from_date = extract_fake_news().values()

    s3object = s3.Object(BUCKET_NAME,f"inbox/{from_date.replace('-','_')}_{to_date.replace('-','_')}_dfrac.json")


    s3object.put(
        Body=(bytes(json.dumps(df).encode('UTF-8')))
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Pipeline has been executed successfully')
    }