import argparse
import logging

from binCollector.bin_collection import get_bin_collector_infos

# Logging config.
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: => %(message)s',
                    datefmt='%m-%d %H:%M')
logger = logging.getLogger('bin')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-date', dest='date', type=str, required=True, help='Date format must be yyyymmdd')
    parser.add_argument('-url', dest='url', type=str, default=None, help='URL server.')
    parser.add_argument('-v', dest='verbose', help='increase output verbosity')

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    res = get_bin_collector_infos(args.date, args.url)

    for n in range(len(res['summary'])):
        logger.info('Next bin to be collected: {summary} in {dtstart} '
                    '\n----UID: {uid}'.format(summary=res['summary'][n],
                                              dtstart=res["dtstart"][n],
                                              uid=res["uid"][n]))
