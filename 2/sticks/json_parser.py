import json

first = input('path to the first file')
second = input('path to the second file')


def parser(file1, file2):
    with open(file1, encoding='utf-8') as a, open(file2, encoding='utf-8') as b:
        wine_data = a.read()[1:-1]
        wine_data2 = b.read()[1:-1]

    wine_data += ', ' + wine_data2[:-1]
    wine_data = wine_data[1:].split('}, {')
    wine_data = set(wine_data)

    wine_sorted = [[], []]

    for wine in wine_data:
        values = {}
        entry = wine.split(', "')

        for pair in entry:
            pair = pair.split(': ', 1)
            pair[0] = pair[0].replace('"', '')
            if '"' in pair[1]:
                pair[1] = pair[1][1:-1]
            if '\\' in pair[1]:
                pair[1] = pair[1].encode().decode('unicode_escape')

            if pair[1] == 'null':
                pair[1] = None
                values[pair[0]] = pair[1]
            elif pair[0] == 'price':
                pair[1] = int(pair[1])
                values[pair[0]] = pair[1]
            else:
                values[pair[0]] = pair[1]

        if values['price'] is None:
            wine_sorted[1].append(values)
        else:
            wine_sorted[0].append(values)

    wine_sorted = sorted(wine_sorted[0], key=lambda x: x['price'], reverse=True) + sorted(wine_sorted[1],
                                                                                          key=lambda x: x['points'])

    return wine_sorted


def writing_data(wines):
    with open('winedata_full.json', 'w', encoding='utf-8') as c:
        wines = str(json_dumper(wines)).encode().decode('unicode_escape') \
            .replace("'", '"').replace('#', "'").replace('None', 'null').replace('\\\\"', '\\"')
        c.write(wines)


def writing_statistics(wine_stats, sorts_stats):
    with open('stats.json', 'w', encoding='utf-8') as f:
        whole_statistics = {'statistics': {'wine': sorts_stats}}
        for elem in wine_stats:
            whole_statistics[elem] = wine_stats[elem]

        whole_statistics = str(whole_statistics).encode().decode('unicode_escape') \
            .replace("'", '"').replace('#', "'").replace('None', 'null').replace('\\\\"', '\\"')

        f.write(str(whole_statistics))


def sorts_statistics(wines):
    sorts = ['Gewürztraminer', 'Riesling', 'Merlot', 'Madera', 'Tempranillo', 'Red Blend']
    sorts_stats = {x: [] for x in sorts}
    prices = {}
    regions = {}
    countries = {}
    scores = {}

    for elem in wines:
        if elem['variety'] in sorts:
            sorts_stats[elem['variety']].append(elem)

    for elem in sorts_stats:
        prices[elem] = [stat['price'] for stat in sorts_stats[elem] if stat['price'] is not None]
        regions[elem] = [stat['region_1'] for stat in sorts_stats[elem] if stat['region_1'] is not None] + \
                        [stat['region_2'] for stat in sorts_stats[elem] if stat['region_2'] is not None]
        countries[elem] = [stat['country'] for stat in sorts_stats[elem] if stat['country'] is not None]
        scores[elem] = [int(stat['points']) for stat in sorts_stats[elem] if stat['points'] is not None]

    answer = prices_calculator(prices)

    for elem in counter(regions):
        answer[elem[0]]['most_common_region'] = elem[1]

    for elem in counter(countries):
        answer[elem[0]]['most_common_country'] = elem[1]

    for elem in scores:
        if len(scores[elem]) > 0:
            answer[elem]['average_score'] = round(sum(scores[elem]) / len(scores[elem]), 2)
        else:
            answer[elem]['average_score'] = None

    answer = {json.encoder.encode_basestring_ascii(k)[1:-1]: v for k, v in answer.items()}

    return answer


def wine_statistics(wines):
    most_expensive_wine = []
    cheapest_wine = []
    highest_score = []
    lowest_score = []
    countries_prices = {}
    countries_scores = {}
    commentators = {}

    highest_price = wines[0]['price']
    lowest_price = min([x['price'] for x in wines if x['price'] is not None])

    points = sorted({int(x['points']) for x in wines})
    highest_points = points[-1]
    lowest_points = points[0]

    for wine in wines:
        if wine['price'] is not None:
            if wine['price'] >= highest_price:
                most_expensive_wine.append(wine)
            elif wine['price'] <= lowest_price:
                cheapest_wine.append(wine)
            try:
                countries_prices[wine['country']].append(wine['price'])
            except KeyError:
                countries_prices[wine['country']] = [wine['price']]
        if wine['points'] is not None:
            if int(wine['points']) >= highest_points:
                highest_score.append(wine)
            elif int(wine['points']) <= lowest_points:
                lowest_score.append(wine)
            try:
                countries_scores[wine['country']].append(int(wine['points']))
            except KeyError:
                countries_scores[wine['country']] = [int(wine['points'])]
        try:
            commentators[wine['taster_name']] += 1
        except KeyError:
            commentators[wine['taster_name']] = 1

    for country in countries_prices:
        countries_prices[country] = round(sum(countries_prices[country]) / len(countries_prices[country]), 2)
    for country in countries_scores:
        countries_scores[country] = round(sum(countries_scores[country]) / len(countries_scores[country]), 2)

    sorted_countries_prices = sorted(countries_prices.items(), key=lambda x: x[1])
    sorted_countries_points = sorted(countries_scores.items(), key=lambda x: x[1])

    most_expensive_country = sorted_countries_prices[-1]
    cheapest_country = sorted_countries_prices[0]
    most_rated_country = sorted_countries_points[-1]
    underrated_country = sorted_countries_points[0]

    if len(most_expensive_wine) == 1:
        most_expensive_wine = most_expensive_wine[0]

    del commentators[None]

    ans = {'most_expensive_wine': most_expensive_wine, 'cheapest_wine': cheapest_wine,
           'highest_score': highest_score, 'lowest_score': lowest_score,
           'most_expensive_country': most_expensive_country[0], 'cheapest_coutry': cheapest_country[0],
           'most_rated_country': most_rated_country[0], 'underrated_country': underrated_country[0],
           'most_active_commentator': sorted(commentators.items(), key=lambda x: x[1])[-1][0]}

    return ans


def prices_calculator(prices):
    answer = {}
    for elem in prices:
        if len(prices[elem]) > 0:
            average_price = round(sum(prices[elem]) / len(prices[elem]), 2)
        else:
            average_price = None
            max_price = None
            min_price = None
            answer[elem] = {'average_price': average_price, 'max_price': max_price, 'min_price': min_price}
            continue

        max_price = max(prices[elem])
        min_price = min(prices[elem])

        answer[elem] = {'average_price': average_price, 'max_price': max_price, 'min_price': min_price}
    return answer


def counter(counts):
    answer = []
    for elem in counts:
        memo1 = counts[elem].copy()
        memo2 = (None, 0)
        for reg in set(memo1):
            if memo1.count(reg) > memo2[1]:
                memo2 = (reg, memo1.count(reg))
                counts[elem] = memo2

    for elem in counts:
        try:
            answer.append((elem, counts[elem][0]))
        except IndexError:
            answer.append((elem, None))

    return answer


def json_dumper(list_of_dicts):
    for dictionary in list_of_dicts:
        for key in dictionary:
            if dictionary[key] == str(dictionary[key]):
                dictionary[key] = json.encoder.encode_basestring_ascii(dictionary[key])[1:-1]
                dictionary[key] = dictionary[key].replace("'", '#').replace('"', '\\"')

    return list_of_dicts


if __name__ == '__main__':
    wine_parsed = parser(first, second)
    statistics1 = wine_statistics(wine_parsed)
    statistics2 = sorts_statistics(wine_parsed)
    writing_data(wine_parsed)
    writing_statistics(statistics1, statistics2)
