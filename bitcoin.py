import requests
import json
import datetime

from constants import OFFENDING_ADDRESSES

start_date = datetime.datetime(year=2013, month=1, day=1)
end_date = datetime.datetime.now()

#start_date.strftime("%s") * 1000
check_date = start_date

while check_date < end_date:
    print str(check_date) + "\n********************************\n\n\n"
    stamp = int(check_date.strftime("%s")) * 1000
    latest_blocks = requests.get('https://blockchain.info/blocks/%i?format=json' % stamp).content
    blocks_json = json.loads(latest_blocks)

    transaction_count = 0
    matches = []
    for block in blocks_json['blocks']:
        block = requests.get('http://blockchain.info/rawblock/%s' % block['hash']).content
        block_json = json.loads(block)

        block_date = datetime.datetime.fromtimestamp(block_json['time'])

        for tx_json in block_json['tx']:

            outputs = tx_json['out']
            transaction_count += 1

            for output in outputs:
                try:
                    if output['addr'] in OFFENDING_ADDRESSES:
                        print output['addr'], block_date
                        matches.append(output['addr'])
                        break
                except KeyError:
                    continue
    one_day = datetime.timedelta(days=1)
    check_date = check_date + one_day


    print "%d%%" % (float(len(matches)) / float(transaction_count) * 100)
    print "(%i/%i)" % (len(matches), transaction_count)

