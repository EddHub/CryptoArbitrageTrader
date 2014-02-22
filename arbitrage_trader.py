# (c) by JohnDorien
# Contact: JohnDorien on Bitcointalk forums
# No warranty for anything!

# If you like this, please donate!

# BTC: 1JxT7dgLxbdHR9iBpu7v4z4ph3kjD5pjA9
# LTC: LQ32aPGFGwFb7MxvLTai2ePwRFRbnSKpWv


import btc_e_api, thread, time
from time import strftime
#import datetime from datetime
from vircurex import *
#from PyCryptsy import PyCryptsy
import crypto
from config import *
from coinse_api import *
import sys

########################################################

def getDepth_btce(pairpart1, pairpart2):
	depth_btce = btce.depth(pairpart1+'_'+pairpart2)
	return depth_btce

def getDepth_vircurex(pairpart1, pairpart2):
	depth_vircurex = Pair(pairpart1+"_"+pairpart2)
	return depth_vircurex

def getDepth_cryptsy(pairpart1, pairpart2):
	pairpart1 = pairpart1.upper()
	pairpart2 = pairpart2.upper()
	target1=cryptsy.GetBuyPrice(pairpart1, pairpart2)
	target2=cryptsy.GetSellPrice(pairpart1, pairpart2)
	depth_cryptsy = [target1, target2]
	return depth_cryptsy

def getDepth_cryptotrade(pairpart1, pairpart2):
	depth_cryptotrade = cryp.reqpublic('depth/'+pairpart1+'_'+pairpart2)
	return depth_cryptotrade

def getDepth_coinse(pairpart1, pairpart2):
	pairpart1 = pairpart1.upper()
	pairpart2 = pairpart2.upper()
	depth_coinse = unauthenticated_request('market/'+pairpart1+'_'+pairpart2+'/'+'depth')#,{'pair':pairpart1+'_'+pairpart2})
	return depth_coinse

#########################################################
def getS(exchange, pairpart1, pairpart2):
	if exchange == "btc-e":
		depth_btce = getDepth_btce(pairpart1, pairpart2)
		sprice = depth_btce['bids'][0][0]
	elif exchange == "vircu":
		depth_vircurex = getDepth_vircurex(pairpart1, pairpart2)
		sprice = depth_vircurex.highest_bid
	elif exchange == "cryptsy":
		#getDepth_cryptsy(pairpart1, pairpart2)
		pairpart1 = pairpart1.upper()
		pairpart2 = pairpart2.upper()
		sprice = cryptsy.GetSellPrice(pairpart2, pairpart1)
	elif exchange == "crypto":
		depth_cryptotrade = getDepth_cryptotrade(pairpart1, pairpart2)
		sprice = float(depth_cryptotrade['bids'][0][0])
		#print sprice
	elif exchange == "coins-e":
		depth_coinse = getDepth_coinse(pairpart1, pairpart2)
		sprice = depth_coinse['marketdepth']['bids'][1]['r']
	else:
		sprice = 0
	return sprice

def getB(exchange, pairpart1, pairpart2):
	if exchange == "btc-e":
		depth_btce = getDepth_btce(pairpart1, pairpart2)
		bprice = depth_btce['asks'][0][0]
	elif exchange == "vircu":
		depth_vircurex = getDepth_vircurex(pairpart1, pairpart2)
		bprice = depth_vircurex.lowest_ask
	elif exchange == "cryptsy":
		#getDepth_cryptsy(pairpart1, pairpart2)
		pairpart1 = pairpart1.upper()
		pairpart2 = pairpart2.upper()
		bprice = cryptsy.GetBuyPrice(pairpart1, pairpart2)
	elif exchange == "crypto":
		depth_cryptotrade = getDepth_cryptotrade(pairpart1, pairpart2)
		bprice = float(depth_cryptotrade['asks'][0][0])
		#print bprice
	elif exchange == "coins-e":
		depth_coinse = getDepth_coinse(pairpart1, pairpart2)
		bprice = depth_coinse['marketdepth']['asks'][0]['r']
	else:
		bprice = 0
	return bprice

#############################################################

def make_trade(exchange, type, amount, pairpart1, pairpart2, rate):   # Type = "buy" or "sell"
	if exchange == "btc-e":
		if type == "buy":
			print "sending buy request to btc-e"
			btce.trade('buy',amount, pairpart1+'_'+pairpart2, rate)
		else:
			print "sending sell request to btc-e"
			btce.trade('sell',amount, pairpart1+'_'+pairpart2, rate)
	elif exchange == "vircu":
		if type == "buy":
			vircurex.buy(pairpart1, amount, pairpart2, rate)
		else:
			vircurex.sell(pairpart1, amount, pairpart2, rate)
	elif exchange == "cryptsy":
		if type == "buy":
			cryptsy.CreateBuyOrder(pairpart1, pairpart2, amount, rate)
		else:
			cryptsy.CreateSellOrder(pairpart1, pairpart2, amount, rate)
	elif exchange == "crypto":
		if type == "buy":
			print "sending buy request to crypto-trade"
			cryp.req('trade',{"pair":pairpart1+"_"+pairpart2,"type":"Buy","amount":amount,"rate":rate})
		else:
			print "sending sell request to crypto-trade"
			cryp.req('trade',{"pair":pairpart1+"_"+pairpart2,"type":"Sell","amount":amount,"rate":rate})
	elif exchange == "coins-e":
		if type == "buy":
			authenticated_request('market/%s/' % (pairpart1+'_'+pairpart2),"neworder",{'order_type':'buy', 'rate':rate, 'quantity':amount,})
		else:
			authenticated_request('market/%s/' % (pairpart1+'_'+pairpart2),"neworder",{'order_type':'sell', 'rate':rate, 'quantity':amount,})
	else:
		return 0

#############################################################
def TestTrade(exchange,pairpart1,pairpart2):

        print "Test trading with " + pairpart1 +"/"+ pairpart2

        sys.stdout.write('\a')  #Beep
        sys.stdout.flush()      #Beep
        make_trade(exchange, "buy", amount1, pairpart1, pairpart2, 0.01)
        make_trade(exchange, "sell", amount1, pairpart1, pairpart2, 8888)

#############################################################
def Compare(pairpart1,pairpart2):

                print "Arbitrage checking for " + pairpart1 +"/"+pairpart2
 
                sprice = []     #Bid price, exchange buy price, for me sell price
                bprice = []     #Ask price, exchange sell price, for me buy price
                
		m=0
		while m<=(len(exc)-1):

                        BidPriceException = False
                        AskPriceException = False
                        sprice.append(-88888)
                        bprice.append(88888)
                               
                        try:
                                sprice[m] = float(getS(exc[m], pairpart1, pairpart2))

                        except  Exception:
                                BidPriceException = True
 
                        try:
                                bprice[m] = float(getB(exc[m], pairpart1, pairpart2))

                        except Exception:
                               AskPriceException = True
                                

                        if BidPriceException:
                                if AskPriceException:
                                        print "Exception on " + str(exc[m]) + " bid and ask price"

                                else: #AskPriceException = false
                                        print "Exception on " + str(exc[m]) + " bid price"

                        else: #BidPriceException = false
                                if AskPriceException:
                                        print "Exception on " + str(exc[m]) + " ask price"
                                        
                                else: #AskPriceException = false
                                        #print exc[m] + ": bid " + str(bprice[m]) + ", ask " + str(sprice[m])
                                        pass

                        m+=1

                #print "On " + str(exc) + ": bids " + str(sprice) + ", asks " + str(bprice)
                
                HiBid = max(sprice)             
                HiExc = sprice.index(HiBid)
                LoAsk = min(bprice)             
                LoExc = bprice.index(LoAsk)     

                print "Highest bid on " + exc[HiExc] + ": " + str(HiBid) + "; lowest ask on " + exc[LoExc] + ": " + str(LoAsk)
                
                if LoAsk < HiBid:
                        #print "Positive spread: Bid " + str(HiBid) + " (" + exc[HiExc] + ") - Ask " + str(LoAsk) + " (" + exc[LoExc] + ")"

                        HiBidAftFee = HiBid/FEE
                        LoAskAftFee = LoAsk*FEE
                        
                        if LoAskAftFee < HiBidAftFee:
                                yld = (HiBidAftFee - LoAskAftFee)/LoAskAftFee
                                #print "Potential arbitrage opportunity, yield after fees" + str(round(yld,2)) + "%"

                                if Diff < yld*100:
                                        print "* Arbitrage opportunity, yield after fees" + str(round(yld,2)) + "%"
                                        sys.stdout.write('\a')  #Beep
                                        sys.stdout.flush()      #Beep
                                        make_trade(exc[LoExc], "buy", amount1*yld, pairpart1, pairpart2, LoAsk)
                                        make_trade(exc[HiExc], "sell", amount1*yld, pairpart1, pairpart2, HiBid)
                                        print "* " + pairpart1 + " bought on " + exc[m] + ", sold on " + exc[k]
                                        
                                else:
                                        print "Positive spread below hurdle, yield after fees" + str(round(yld,2)) + "%"

                        else:
                                print "Positive spread less than fees"
                
                else:
                        print "Negative spread"

###############################################################

def main():
	"""main function, called at the start of the program"""
        
	def run1(sleeptime, lock):
                i=1
                pairpart1 = "ltc"
                pairpart2 = "btc"
                while True:
			lock.acquire()
			print "Starting round " + str(i)
			#TestTrade("Coins-e",pairpart1,pairpart2)
                        Compare(pairpart1,pairpart2)
                        i=i+1
			print "Round completed, sleeping for 20 seconds"
			print ""
			lock.release()
			time.sleep(sleeptime)
 
	lock = thread.allocate_lock()
	thread.start_new_thread(run1, (20, lock))
 
	while True:
		pass

if __name__ == "__main__":
	main()
