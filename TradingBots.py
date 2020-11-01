
class Trader:
    
    
    
    
    def __init__(self,money, time_horizon, upper_sell_bound, lower_sell_bound, buy_loss_limit, upper_short_bound, lower_short_bound, short_loss_limit ):
        
        """Method for initializing a Trader object

        Args: 
            money (float)
            stock_num (int)
            

        Attributes:
            
            money (float): amount of cash held
            stock_num (int): number of stocks held
            time (int): timestep / number of action points in session past
            profit_made (float): accumulated profit of trading object for session
            
            error_num (int): number of errors made by agent
            buy_num (int): cumulative number of stocks bought in session
            sell_num (int): cumulative number of stocks bought in session
            stock_tracker (list): 
                    list of lists, where each element is a list containing 
                    the stocks purchased price and time session purchase
            short_open_num (int): cumulative number of shorts bought in session
            short_num (int): number of shorts currently held
            short_tracker (list): list of lists contatining information of currently held shorts.
                                        price at opening of short and time stamp of opening
            
            short_sell_num (int): Number of shorts closed.
        """
        
        
        self.money = money
        self.stock_num = 0
        self.time = 0
        self.profit_made = 0
        
        self.error_num = 0
        self.buy_num = 0
        self.sell_num = 0
        self.stock_tracker = []
        self.short_open_num = 0
        self.short_num = 0
        self.short_tracker = []
        self.short_sell_num_forced=0
        self.short_sell_num = 0

        self.time_horizon = time_horizon
        self.upper_sell_bound = upper_sell_bound
        self.lower_sell_bound = lower_sell_bound
        self.buy_loss_limit = buy_loss_limit
        self.upper_short_bound = upper_short_bound
        self.lower_short_bound = lower_short_bound
        self.short_loss_limit = short_loss_limit
        
    def buy(self, price):
        
        """ If the agent has enough cash it will purchases stock at the current price.
        Appends the time and the price paid for the stock to the stock_tracker list.
        
         Args:
             price (float): The current price of the stock
             
        Return:
            None
             
        
        """
        if self.money > price:
            self.money -= price
            self.stock_num +=1
            self.stock_tracker.append([price, self.time])
            self.buy_num +=1
        else: self.error_num+=1
            
    def sell(self, price, stock_num_held = 0):
        """ If the agent has enough cash it will purchases stock at the current price.
        Appends the time and the price paid for the stock to the stock_tracker list.
        
         Args:
             price (float): The current price of the stock
             
        Return:
            None
             
        
        """
        
        
        
        if self.stock_num>0:
            
            self.stock_num -=1
            self.money += price*0.997
            first_stock_held = self.stock_tracker.pop(stock_num_held)
            profit_amount = price*0.997 - first_stock_held[0]*((self.time - first_stock_held[1])*(0.0002/252)+1)
            self.sell_num +=1
            self.profit_made+= profit_amount
        else:
            self.error_num+=1
            
    
        
        
        
    def short_open(self,price):
        '''
        
        '''
        if self.money > price/2:
            self.money -= price/2
            self.short_num +=1
            self.short_tracker.append([price, self.time])
            self.short_open_num +=1
        else: self.error_num+=1
    
    def short_close(self,price, short_num_held = 0):
        if self.short_num>0:
            
            self.short_num -=1
            
            first_stock_held = self.short_tracker.pop(short_num_held)
            
            profit_amount = first_stock_held[0] -price #*((self.time - first_stock_held[1])*(0.0002/252)+1)
            
            #0.11% is a reasonable yearly interest rate of 3% divided by 252
            self.money += 1.5*first_stock_held[0]  - price*1.005  -first_stock_held[0]*((self.time - first_stock_held[1])*(0.03/252))
            
            self.short_sell_num +=1
            self.profit_made+= profit_amount
            #self.money += profit_amount + first_stock_held[0]/2
        else:
            self.error_num+=1
 

           
    def help_sell(self, todays_price):
        '''
        Sells stocks which have increased in value by over one percent,
        or if it has lost more than 0.2 percent to avoid losses.
    
        parameters
        -------------
        stock_tracker
            list of stocks and the time they were purchaced
            (the date purchaced becomes important with longer timeframe
            in order to account for inflation)
    
        todays_price
            The current market price of the stock
        
        self
            The the current self object in order to perform sell operations.
        
        returns
        --------------
        None
        '''

        #Solves the problem of changing position due to pop() method
        decreaser = 0
        for i ,stock_data in enumerate(self.stock_tracker):
            i-=decreaser
            
            #if the stock price today is higher than 1.5 percent than it was paid for
            if stock_data[0]*self.upper_sell_bound < todays_price:
                self.sell(price = todays_price, stock_num_held = i)
                decreaser+=1
            
            #If the stock price less than 0.5% the price it was paid for sell it to prevent loss
            elif stock_data[0]*self.buy_loss_limit > todays_price:
                self.sell(price = todays_price, stock_num_held = i)
                decreaser+=1
            
            #if the price has flatlining we will take lower profit gain
            elif (stock_data[1] +self.time_horizon*(2/5) < self.time) and (stock_data[0]*self.lower_sell_bound  < todays_price):
                self.sell(price = todays_price, stock_num_held = i)
                decreaser+=1
            
            # If the stock is 
            elif stock_data[1] +self.time_horizon < self.time:
                self.sell(price = todays_price, stock_num_held = i)
                decreaser+=1
    

            
    def help_close_short(self, todays_price):
        '''
        Sells stocks which have increased in value by over one percent,
        or if it has lost more than 0.2 percent to avoid losses.
    
        parameters
        -------------
        self.short_tracker
            list of stocks and the time they were purchaced
            (the date purchaced becomes important with longer timeframe
            in order to account for inflation)
    
        todays_price
            The current market price of the stock
        
        self
            The the current self object in order to perform sell operations.
        
        returns
        --------------
        None
        '''
    
        #Solves the problem of changing position due to pop() method
        decreaser = 0
        for i ,short_data in enumerate(self.short_tracker):
            i-=decreaser
        
            #If the short has reached a level where it is profitable to make the trade, it will do so
            if short_data[0]*self.upper_short_bound < todays_price:
                self.short_close(price = todays_price, short_num_held = i)
                decreaser+=1
        
            #the price seems to be going in the opposite way to prediction so sell to limit loss
            elif short_data[0]*self.short_loss_limit > todays_price:
                self.short_close(price = todays_price, short_num_held = i)
                decreaser+=1
        
            #if the price has flatlining we will take lower profit gain
            elif short_data[1] +self.time_horizon*(2/5) < self.time and (short_data[0]*self.lower_short_bound < todays_price):
                self.short_close(price = todays_price, short_num_held = i)
                decreaser+=1
        
            #the price has flatlined so not worth holding
            elif short_data[1] +self.time_horizon < self.time:
                self.short_close(price = todays_price, short_num_held = i)
                decreaser+=1


class Trader_2p_threshold(Trader):
    
    def __init__(self,money,time_horizon ):

        
        upper_sell_bound = 1.02
        lower_sell_bound = 1.01
        buy_loss_limit = 0.985
        upper_short_bound = 0.97
        lower_short_bound = 0.99
        short_loss_limit = 0.015
       
        Trader.__init__(self,money,time_horizon, upper_sell_bound, lower_sell_bound, buy_loss_limit, upper_short_bound, lower_short_bound, short_loss_limit  )
  
class Trader_3p_threshold(Trader):
    
    def __init__(self,money,time_horizon ):

        
        upper_sell_bound = 1.03
        lower_sell_bound = 1.015
        buy_loss_limit = 0.98
        upper_short_bound = 0.96
        lower_short_bound = 0.975
        short_loss_limit = 0.02
       
        Trader.__init__(self,money,time_horizon, upper_sell_bound, lower_sell_bound, buy_loss_limit, upper_short_bound, lower_short_bound, short_loss_limit  )
  

class Trader_1p5_threshold(Trader):
    
    def __init__(self,money,time_horizon ):

        
        upper_sell_bound = 1.015
        lower_sell_bound = 1.01
        buy_loss_limit = 0.989
        upper_short_bound = 0.975
        lower_short_bound = 0.99
        short_loss_limit = 0.01
       
        Trader.__init__(self,money,time_horizon, upper_sell_bound, lower_sell_bound, buy_loss_limit, upper_short_bound, lower_short_bound, short_loss_limit  )

class Trader_1p_threshold(Trader):
    
    def __init__(self,money,time_horizon ):

        
        upper_sell_bound = 1.01
        lower_sell_bound = 1.005
        buy_loss_limit = 0.99
        upper_short_bound = 0.98
        lower_short_bound = 0.99
        short_loss_limit = 0.008
       
        Trader.__init__(self,money,time_horizon, upper_sell_bound, lower_sell_bound, buy_loss_limit, upper_short_bound, lower_short_bound, short_loss_limit  )
  




