## US News College Scraper

Really simple and modifiable scraper for US News' College Rankings.

The included `data.csv` should have all the data you need, but you can modify the `FIELDS` variable in `main.py` to get other desired fields or remove unwanted fields.

Default fields:
```python
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
```

Look at the items array in the data field of the search results ([https://www.usnews.com/best-colleges/api/search?_sort=schoolName&_sortDirection=asc&_page=1](https://www.usnews.com/best-colleges/api/search?_sort=schoolName&_sortDirection=asc&_page=1)) to look at the structure to find the fields.

If the `DETAILED` flag in `main.py` is set to true, the scraper will also scrape the page for each individual school for more data instead of just the aggregated search pages. This makes the scraping process about 10x slower, but adds the `DETAIL_FIELDS`.

The included `data-detailed.csv` was run with `DETAILED` on.

Detail fields:
```python
DETAIL_FIELDS = [
    'School Type',
    'Year Founded',
    'Religious Affiliation',
    'Academic Calendar',
    'Setting',
    '2018 Endowment',
    'School Website'
]
```
