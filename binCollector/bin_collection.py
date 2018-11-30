import logging
import re

import requests

logger = logging.getLogger('bin')

# Regex patterns to extract data.
pattern_event = r'(?<= BEGIN:VEVENT ).*?(?= END:VEVENT)'
pattern_uid = r'UID:(.*) DTSTAMP'
pattern_dtstamp = r'DTSTAMP:(.*) DTSTART'
pattern_dtstart = r'DTSTART;VALUE=DATE:(.*) SUMMARY'
pattern_summary = r'SUMMARY:(.*)'


def get_bin_collector_infos(date: str = None, url: str = None):
    """
    Get bin collector informations.
    :param date: String date.
    :param url: URL.
    :return: Dict with all information needed.
    """
    bins = get_info_from_server(url)

    data_dict = dict()

    for bin in bins:
        uid = re.findall(pattern_uid, bin)[0]
        dtstamp = re.findall(pattern_dtstamp, bin)[0]
        dtstart = re.findall(pattern_dtstart, bin)[0]
        summary = re.findall(pattern_summary, bin)[0]

        if not dtstart in data_dict.keys():
            data_dict[dtstart] = {'uid': [],
                                  'dtstamp': [],
                                  'dtstart': [],
                                  'summary': []}

        if uid not in data_dict[dtstart]['uid']:
            data_dict[dtstart]['uid'].append(uid)
        if dtstamp not in data_dict[dtstart]['dtstamp']:
            data_dict[dtstart]['dtstamp'].append(dtstamp)
        if dtstamp not in data_dict[dtstart]['dtstart']:
            data_dict[dtstart]['dtstart'].append(dtstart)
        if summary not in data_dict[dtstart]['summary']:
            data_dict[dtstart]['summary'].append(summary)

    date_list_sorted = sorted(data_dict.keys())
    date_ = get_closest_date(date, date_list_sorted)

    res = data_dict[date_]
    logger.debug('Res: {res}'.format(res=res))
    return res


def get_info_from_server(url=None):
    """
    Get info from server.
    :param url: URL.
    :return: Requested data.
    """

    if url is None:
        url = r'https://s3-eu-west-1.amazonaws.com/fs-downloads/GM/binfeed.ical'
    logger.debug('Getting info from URL: {}'.format(url))
    r = requests.get(url)
    logger.debug('Response from server: {}'.format(r.status_code))
    string_ = repr(r.text.replace('\r\n', ' '))
    res = re.findall(pattern_event, string_)
    logger.debug('Raw text from server: {}\n\n'.format(res))
    return res


def get_closest_date(date: str, list_date: list):
    """
    Get the closest date to collect bins.
    :param date: String date.
    :param list_date: List of dates available.
    :return: String closest date.
    :raises ValueError
    """
    if len(date) != 8:
        raise ValueError('Date must be in this format: yyyymmdd')

    if not isinstance(date, int):
        date = int(date)

    if date > int(list_date[-1]):
        raise ValueError('Date must be lower than {}'.format(list_date[-1]))

    date_ = int((min(list_date, key=lambda x: abs(int(x) - date))))
    value = str(date_)

    if date_ == date:
        return value

    if date > date_:
        index = list_date.index(str(date_))
        value = str(list_date[index + 1])
        return value

    return value


if __name__ == '__main__':
    print(get_bin_collector_infos(date='20171228'))
