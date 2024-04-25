from datetime import datetime,timedelta
from colored import Style,Fore


from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.DatePicker import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *

class CalcNetFrom2Pt:
	def __init__(self,rate=False):
		print("END DATETIME")
		try:
			end=DateTimePkr()
		except Exception as e:
			print(e)
			return
		print("START DATETIME")
		try:
			start=DateTimePkr()
		except Exception as e:
			print(e)
			return
		print(f"{Fore.light_green}A break of {Fore.dark_goldenrod}60 Minutes is {Fore.light_yellow}Subtracted from {Fore.light_red}{Style.bold}{Style.underline}Total Duration{Style.reset}")
		breakt=timedelta(seconds=60*60)
		print(f'{Fore.spring_green_2a}{(end-start)-breakt}{Style.reset}')

		print(f"{Fore.light_red}{Style.bold}{Style.underline}Be Aware {Fore.light_yellow}Not Used in Rate Calculations!{Style.reset}\n{Fore.light_green}A break of {Fore.dark_goldenrod}30 Minutes is {Fore.light_yellow}Subtracted from {Fore.light_red}{Style.bold}{Style.underline}Total Duration{Style.reset}")
		breakt30=timedelta(seconds=60*30)
		print(f'{Fore.light_magenta}{(end-start)-breakt30}{Style.reset}')
		
		if not rate:
			return
			
		def mkFloat(text,data):
			try:
				if text == '':
					return data
				return float(eval(text))
			except Exception as e:
				print(e)
		while True:
		 rate=Prompt.__init2__(None,func=mkFloat,ptext='Rate of pay $/Hr',helpText="How Much do you make an hour?",data=1)
		 if rate in (None,):
		 	break
		 gross=round(((((end-start)-breakt).total_seconds()/60)/60)*rate,2)
		 print(gross)
		 tax=gross*0.178
		 print(gross-tax)
		 wwd=Prompt.__init2__(None,func=mkFloat,ptext='days in work week(to calculate union dues per day)',helpText="How Many days are in your work week?",data=4)
		 if wwd in (None,):
		 	break
		 union=10/wwd
		 net=gross-tax
		 net-=union
		 print('gross:',gross)
		 print('net income: ',net)
		 print('tax:',-tax)
		 print('union dues:',-union)
		 print('duration:',(end-start)-breakt)
		 break
		 
		 #how many days in work week
		 #divide 10 by work week days
		 #subtract from gross-tax
		print((end-start)-breakt)
		
if __name__=='__main__':
	state=True
	CalcNetFrom2Pt(rate=state)