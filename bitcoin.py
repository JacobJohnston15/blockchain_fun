import requests
import json
import datetime 
import sys
#Importation

from constants import OFFENDING_ADDRESSES
#Importing the gambling addresses from the text file that holds all of them 


start_date = datetime.datetime(year=2015, month=01, day=01)
end_date = datetime.datetime.now()
check_date = start_date
#Initializing the start and end date for the data collection process  
#The end date gets the current time using datetime (predefined and imported)


f=open("final.txt","w") 
#Opens the text file where the data will be put after being collected
while check_date < end_date:
    print str(check_date) + "\n****\n\n\n" 
    #This line prints the date that the data is being collected for 
    #It also prints asterisks so that new dates can be seen on the terminal 
    
    stamp = int(check_date.strftime("%s")) * 1000 
    try:
        latest_blocks = requests.get('https://blockchain.info/blocks/%i?format=json' % stamp).content 
        #This is a try/except to ping the API (Checking to make sure that the internet is working)
    except:
        print check_date
        sys.exit(0)
        #If the program can not pull data from the API, the program will print the date that it is on 
        #and will exit
    blocks_json = json.loads(latest_blocks)
    #Declares the variable blocks_json to be the json data of the latest blocks that the program pulls 
    #from the API 

    transaction_count = 0
    #Sets the current transaction count to 0
    matches = []
    #Creates an empty list (array) called matches
    for block in blocks_json['blocks']:
    #Uses the 'blocks' variable from the blockchain API, which grabs all of the blocks from the date that 
    #the program is running for
        try:
            block = requests.get('http://blockchain.info/rawblock/%s' % block['hash']).content
            #Try/Except to ping the API again
        except: 
            print check_date
            sys.exit(0)
            #If there is no response, the program will print the date that it is on and will exit 

        block_json = json.loads(block)
        #Reinitializes block_json to the block variable in the json data that the program has collected

        block_date = datetime.datetime.fromtimestamp(block_json['time'])
        #Defines the variable block_date to be the 'time' variable that the program collects from the API 

        for tx_json in block_json['tx']:
        #Uses the 'tx' variable in the API to get transactions from the blocks

            outputs = tx_json['out']
            #Defines the variable outputs to be the 'out' variable in the API, meaning that outputs is all 
            #of the outputs of the transaction that the program is currently on
            transaction_count += 1
            #Add one to the transaction count

            x=(float(len(matches)) / float(transaction_count) * 100)
            #Defines x to equal the matching outputs divided by the total transaction count, multiplied by 100
            y=(len(matches), transaction_count)
            #Defines y to equal the matches and the transaction count, seperated by a comma


            for output in outputs:
            #Loop to check and see if the output of a transaction matches a gambling address
                try:
                    if output['addr'] in OFFENDING_ADDRESSES:
                    #If the output address is in the gambling addresses in the text file
                        print output['addr']# block_date
                        #Prints the matching address to the screen
                        #This can be commented out for optimization purposes
                        matches.append(output['addr'])
                        #Append the output address to the list 
                        break
                except KeyError:
                    continue
                    #If nothing matches, the program continues and moves on to the next day

    one_day = datetime.timedelta(days=1)
    #Declares the one_day variable to equal one day 
    check_date = check_date + one_day
    #Adds one day to the current date that the program is on 
    d=(check_date)
    #Declares d to equal the check_date variable (the current date)
    
    z = str(d)+' - '+str(x)+' - '+str(y)+' - \n'
    #Declares z to equal d,x, and y so that all of the variables can be written to the file at once
    f.write(str(z))
    #Writes z to the text file

f.close()
#Closes the text file

