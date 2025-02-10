import requests
from bs4 import BeautifulSoup

import json
import csv

FIELDS = [
    'institution.displayName',
    'institution.schoolType',
    'institution.aliasNames',
    'institution.state',
    'institution.city',
    'institution.zip',
    'institution.region',
    'institution.isPublic',
    'institution.institutionalControl',
    'institution.primaryPhotoCardThumb',
    'ranking.displayRank',
    'ranking.sortRank',
    'ranking.isTied',
    'searchData.actAvg.rawValue',
    'searchData.percentReceivingAid.rawValue',
    'searchData.acceptanceRate.rawValue',
    'searchData.tuition.rawValue',
    'searchData.hsGpaAvg.rawValue',
    'searchData.engineeringRepScore.rawValue',
    'searchData.parentRank.rawValue',
    'searchData.enrollment.rawValue',
    'searchData.businessRepScore.rawValue',
    'searchData.satAvg.rawValue',
    'searchData.costAfterAid.rawValue',
    'searchData.testAvgs.displayValue.0.value',
    'searchData.testAvgs.displayValue.1.value'
]

DETAILED = False
DETAIL_FIELDS = [
    'School Type',
    'Year Founded',
    'Religious Affiliation',
    'Academic Calendar',
    'Setting',
    '2018 Endowment',
    'School Website'
]

HEADERS = {
    'Accept-Language': 'en-US,en',
    'Priority': 'u=0, i',
    'Sec-CH-UA': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}


def traverse(root, path):
    value = root
    for segment in path.split('.'):
        if segment.isdigit():
            value = value[int(segment)] if len(value) > int(segment) else None
        else:
            value = value.get(segment, None)
    return value


def fetch_results_page(url, writer):
    print('Fetching ' + url + '...')
    resp = requests.get(url, headers=HEADERS)
    json_data = json.loads(resp.text)
    for school in json_data['data']['items']:
        row = []
        for field in FIELDS:
            row.append(traverse(school, field))

        if DETAILED:
            resp = requests.get('https://www.usnews.com/best-colleges/' + traverse(school, 'institution.urlName') + '-'
                                + traverse(school, 'institution.primaryKey'), headers=HEADERS)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for field in DETAIL_FIELDS:
                field_element = soup.find(text=field)
                if field_element is None:
                    row.append(None)
                    continue
                parent = field_element.parent.parent
                if field == 'School Website':
                    row.append(parent.a['href'] if parent.a else None)
                else:
                    row.append(parent.find_all('p')[-1].text)

        writer.writerow(row)

    if json_data['meta']['rel_next_page_url']:
        fetch_results_page(json_data['meta']['rel_next_page_url'], writer)
    else:
        print('Done!')


with open('data-detailed.csv' if DETAILED else 'data.csv', 'w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(FIELDS + (DETAIL_FIELDS if DETAILED else []))
    fetch_results_page('https://www.usnews.com/best-colleges/api/search?_sort=schoolName&_sortDirection=asc&_page=1',
                       data_writer)
