import requests
import datetime
import shutil
import locale
locale.setlocale(locale.LC_ALL, 'zh_TW.utf8')

from multiprocessing import Pool

import tqdm


def gen_datetime_objs(start_t_str, num_days):
    dts = []

    start_dt = datetime.datetime.strptime(start_t_str, '%Y-%m-%d_%H-%M')

    dts = [start_dt - datetime.timedelta(days=x) for x in range(num_days)]

    return dts


def gen_urls(dts):
    urls = []
    for dt in dts:
        yyyy = dt.strftime("%Y")
        mm = dt.strftime("%m")
        dd = dt.strftime("%d")
        hour = dt.strftime("%H")
        # min = dt.strftime("%M")

        # print(f'{yyyy}-{mm}-{dd}_{hour}-{min}')

        CWBWRF_MultiModels_forcasts = ['f00_12s', 'f12_24s', 'f24_36s', 'f36_48s', 'f48_60s', 'f60_72s']

        # https://watch.ncdr.nat.gov.tw/00_Wxmap/5F4_CWBWRF_MultiModels/202406/2024061300/G01_2024061300_f00_12s.gif
        node_set = [f'https://watch.ncdr.nat.gov.tw/00_Wxmap/5F4_CWBWRF_MultiModels/{yyyy}{mm}/{yyyy}{mm}{dd}{hour}/G01_{yyyy}{mm}{dd}{hour}_{node}.gif' for node in CWBWRF_MultiModels_forcasts]

        urls.extend(node_set)

    return urls


def download_data(url):

    try:
        print(url)
        r = requests.get(url, stream=False, timeout=3)
        gifname = url.split('/')[-1]
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

    else:
        with open(f'./imgs/{gifname}', 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)


def main():
    
    start_t_str = '2024-06-09_12-00'
    num_days = 5
    dts = gen_datetime_objs(start_t_str, num_days)

    urls = gen_urls(dts)


    # for url, dt in zip(tqdm.tqdm(urls)):
        
        # response = requests.get(url, stream=True)
        # gifname = url.split('/')[-1]

        # print(url)
        # with open(f'./imgs/{gifname}', 'wb') as out_file:
        #     shutil.copyfileobj(response.raw, out_file)

        # del response

    # p = Pool(10)
    # p.map(download_data, urls)

    with Pool(10) as p:
        res = p.map_async(download_data, urls)
        # print(res)
        p.close()
        p.join()


if __name__ == '__main__':
    main()