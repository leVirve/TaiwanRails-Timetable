import requests
import lxml.html

url = 'http://twtraffic.tra.gov.tw/twrail/SearchResult.aspx'


def list_it(notes, comment):
    r = [note.get('id') for note in notes]
    r.append(comment)
    return r


def get_results(url, params):
    results = list()
    response = requests.get(url, params=params)
    document = lxml.html.fromstring(response.text)
    for row in document.xpath("//tbody/tr[@class='Grid_Row']"):
        train_type = row.xpath("./td[1]//div/span")[0]
        train_code = row.xpath("./td[2]//a")[0]
        versa = row.xpath("./td[3]/font")[0]
        route = row.xpath("./td[4]/font")[0]
        launch_time = row.xpath("./td[5]/font")[0]
        arrive_time = row.xpath("./td[6]/font")[0]
        duration = row.xpath("./td[7]/font")[0]
        notes = row.xpath("./td[8]//div/img")
        comment = row.xpath("./td[8]//div/span[@id='Comment']")[0]
        price = row.xpath("./td[9]//span")[0]
        notes = list_it(notes, comment.text)

        results.append({
            'train_type': train_type.text,
            'train_code': train_code.text,
            'versa': versa.text,
            'route': route.text,
            'launch_time': launch_time.text,
            'arrive_time': arrive_time.text,
            'duration': duration.text,
            'price': price.text,
            'notes': notes
        })
    return results

if __name__ == '__main__':
    params = {
        'searchtype': 0,
        'searchdate': '2015/06/07',
        'fromstation': 1317,
        'tostation': 1025,
        'trainclass': 2,
        'fromtime': '0000',
        'totime': '2359',
    }
    results = get_results(url, params)

    for result in results:
        print(result)
