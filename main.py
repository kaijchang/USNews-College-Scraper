import requests

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


def fetch_results_page(url, writer):
    print('Fetching ' + url + '...')
    resp = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'
    })
    json_data = json.loads(resp.text)
    for school in json_data['data']['items']:
        row = []
        for field in FIELDS:
            path = field.split('.')
            value = school
            for segment in path:
                if segment.isdigit():
                    value = value[int(segment)]
                else:
                    value = value[segment]
            row.append(value)
        writer.writerow(row)

    if json_data['meta']['rel_next_page_url']:
        fetch_results_page(json_data['meta']['rel_next_page_url'], writer)
    else:
        print('Done!')


with open('data.csv', 'w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(FIELDS)
    fetch_results_page('https://www.usnews.com/best-colleges/api/search?_sort=schoolName&_sortDirection=asc&_page=1',
                       data_writer)
