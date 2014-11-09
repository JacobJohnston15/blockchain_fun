import requests
import json
import datetime 
import sys


from constants import OFFENDING_ADDRESSES


start_date = datetime.datetime(year=2014, month=1, day=1)
end_date = datetime.datetime.now()
#start_date.strftime("%s") * 1000
check_date = start_date


f=open("final.txt","w") 
while check_date < end_date:
    print str(check_date) + "\n********************************\n\n\n" 
    
    stamp = int(check_date.strftime("%s")) * 1000 
    try:
        latest_blocks = requests.get('https://blockchain.info/blocks/%i?format=json' % stamp).content 
    except:
        print check_date
        sys.exit(0)
    blocks_json = json.loads(latest_blocks)

    transaction_count = 0
    matches = []
    for block in blocks_json['blocks']:
        try:
            block = requests.get('http://blockchain.info/rawblock/%s' % block['hash']).content
        except: 
            print check_date
            sys.exit(0)

        block_json = json.loads(block)

        block_date = datetime.datetime.fromtimestamp(block_json['time'])

        for tx_json in block_json['tx']:

            outputs = tx_json['out']
            transaction_count += 1

            x=(float(len(matches)) / float(transaction_count) * 100)
            y=(len(matches), transaction_count)



            for output in outputs:
                try:
                    if output['addr'] in OFFENDING_ADDRESSES:
                        print output['addr']# block_date
                        matches.append(output['addr'])
                        break
                except KeyError:
                    continue

    one_day = datetime.timedelta(days=1)
    check_date = check_date + one_day
    d=(check_date)
    """ Adds a new day and moves on """
    
    """f=open("final.txt","w")
    x=(float(len(matches)) / float(transaction_count) * 100)
    y=(len(matches), transaction_count)
    d=(check_date)
    """
    
    z = str(d)+'***'+str(x)+'***'+str(y)+'***\n'
    f.write(str(z))
    ''' f.write(str(d)+ '***') '''
    '''print "%d%%" % (float(len(matches)) / float(transaction_count) * 100)
    print "(%i/%i)" % (len(matches), transaction_count)
    '''
    '''f.write(str(y)+ '***\n')'''

f.close()

