import pandas as pd



class Capital:
    def __init__(self, data):
        #self.account_type = [i.get('accountType') for i in data]
        # self.currency = [i.get('currency') for i in data]
        # self.net_liquidation_value = [i.get('netLiquidationValue') for i in data]
        # self.unrealized_profit_loss = [i.get('unrealizedProfitLoss') for i in data]
        # self.unrealized_profit_loss_rate = [i.get('unrealizedProfitLossRate') for i in data]
        # self.unrealized_profit_loss_base = [i.get('unrealizedProfitLossBase') for i in data]
        # self.day_buying_power = [i.get('dayBuyingPower') for i in data]
        # self.overnight_buying_power = [i.get('overnightBuyingPower') for i in data]
        # self.settled_funds = [i.get('settledFunds') for i in data]
        # self.unsettle_funds = [i.get('unsettleFunds') for i in data]
        # self.crypto_buying_power = [i.get('cryptoBuyingPower') for i in data]
        # self.option_buying_power = [i.get('optionBuyingPower') for i in data]
        # self.total_cash_value = [i.get('totalCashValue') for i in data]
        # self.total_cost = [i.get('totalCost') for i in data]
        # self.remain_trade_times = [i.get('remainTradeTimes') for i in data]
        # self.total_market_value = [i.get('totalMarketValue') for i in data]
        # self.pending_funds = [i.get('pendingFunds') for i in data]
        # self.available_buying_power = [i.get('availableBuyingPower') for i in data]
        # self.unavailable_buying_power = [i.get('unAvailableBuyingPower') for i in data]
        # self.credit_diff_bp = [i.get('creditDiffBp') for i in data]
        # self.credit_bp = [i.get('creditBp') for i in data]
        # self.frozen_bp = [i.get('frozenBp') for i in data]
        # self.unrecovered_bp = [i.get('unRecoveredBp') for i in data]
        # self.crypto_bp = [i.get('cryptoBp') for i in data]
        # self.event_bp = [i.get('eventBp') for i in data]
        # self.dt_day_count_detail_vol_list = [i.get('dtDayCountDetailVoList') for i in data]
        # self.unlimited = [i.get('unlimited') for i in data]

        self.account_type = data.get('accountType')
        self.currency = data.get('currency')
        self.net_liquidation_value = data.get('netLiquidationValue')
        self.unrealized_profit_loss = data.get('unrealizedProfitLoss')
        self.unrealized_profit_loss_rate = data.get('unrealizedProfitLossRate')
        self.unrealized_profit_loss_base = data.get('unrealizedProfitLossBase')
        self.day_buying_power = data.get('dayBuyingPower')
        self.overnight_buying_power = data.get('overnightBuyingPower')
        self.settled_funds = data.get('settledFunds')
        self.unsettle_funds = data.get('unsettleFunds')
        self.crypto_buying_power = data.get('cryptoBuyingPower')
        self.option_buying_power = data.get('optionBuyingPower')
        self.total_cash_value = data.get('totalCashValue')
        self.total_cost = data.get('totalCost')
        self.remain_trade_times = data.get('remainTradeTimes')
        self.total_market_value = data.get('totalMarketValue')
        self.pending_funds = data.get('pendingFunds')
        self.available_buying_power = data.get('availableBuyingPower')
        self.unavailable_buying_power = data.get('unAvailableBuyingPower')
        self.credit_diff_bp = data.get('creditDiffBp')
        self.credit_bp = data.get('creditBp')
        self.frozen_bp = data.get('frozenBp')
        self.unrecovered_bp = data.get('unRecoveredBp')
        self.crypto_bp = data.get('cryptoBp')
        self.event_bp = data.get('eventBp')
        self.unlimited = data.get('unlimited')


        self.data_dict = {
                    'account_type': self.account_type,
                    'currency': self.currency,
                    'net_liquidation_value': self.net_liquidation_value,
                    'unrealized_profit_loss': self.unrealized_profit_loss,
                    'unrealized_profit_loss_rate': self.unrealized_profit_loss_rate,
                    'unrealized_profit_loss_base': self.unrealized_profit_loss_base,
                    'day_buying_power': self.day_buying_power,
                    'overnight_buying_power': self.overnight_buying_power,
                    'settled_funds': self.settled_funds,
                    'unsettle_funds': self.unsettle_funds,
                    'crypto_buying_power': self.crypto_buying_power,
                    'option_buying_power': self.option_buying_power,
                    'total_cash_value': self.total_cash_value,
                    'total_cost': self.total_cost,
                    'remain_trade_times': self.remain_trade_times,
                    'total_market_value': self.total_market_value,
                    'pending_funds': self.pending_funds,
                    'available_buying_power': self.available_buying_power,
                    'unavailable_buying_power': self.unavailable_buying_power,
                    'credit_diff_bp': self.credit_diff_bp,
                    'credit_bp': self.credit_bp,
                    'frozen_bp': self.frozen_bp,
                    'unrecovered_bp': self.unrecovered_bp,
                    'crypto_bp': self.crypto_bp,
                    'event_bp': self.event_bp,

                    'unlimited': self.unlimited
                }
        

        self.as_dataframe = pd.DataFrame(self.data_dict, index=[0])




class DT_DAY_DETAIL_LIST:
    def __init__(self, data):
        self.dt_day_count_detail_vol_list = data.get('dtDayCountDetailVoList')




class Positions:
    def __init__(self, data):

        self.id = [i.get('id') for i in data]
        self.tickerType = [i.get('tickerType') for i in data]
        self.optionStrategy = [i.get('optionStrategy') for i in data]
        self.items = [i.get('items') for i in data]
        self.items = [item for sublist in self.items for item in sublist]
        self.quantity = [i.get('quantity') for i in data]
        self.cost = [i.get('cost') for i in data]
        self.marketValue = [i.get('marketValue') for i in data]
        self.unrealizedProfitLoss = [i.get('unrealizedProfitLoss') for i in data]
        self.unrealizedProfitLossRate = [i.get('unrealizedProfitLossRate') for i in data]
        self.unrealizedProfitLossBase = [i.get('unrealizedProfitLossBase') for i in data]
        self.costPrice = [i.get('costPrice') for i in data]
        self.lastPrice = [i.get('lastPrice') for i in data]
        self.belongTradePrice = [i.get('belongTradePrice') for i in data]
        self.proportion = [i.get('proportion') for i in data]


        self.data_dict = { 
            'id': self.id,
            'ticker_type': self.tickerType,
            'option_strategy': self.optionStrategy,
            'items': self.items,
            'quantity': self.quantity,
            'cost': self.cost,
            'market_value': self.marketValue,
            'unrealized_pl': self.unrealizedProfitLoss,
            'unrealized_pl_rate': self.unrealizedProfitLossRate,
            'unrealized_pl_base': self.unrealizedProfitLossBase,
            'cost_price': self.costPrice,
            'last_price': self.lastPrice,
            'belong_trade_price': self.belongTradePrice,
            'proportion': self.proportion
        }

        self.as_dataframe = pd.DataFrame(self.data_dict)




class OpenPositions:
    def __init__(self, data):

        self.legId = [i.get('legId') for i in data]
        self.brokerId = [i.get('brokerId') for i in data]
        self.assetType = [i.get('assetType') for i in data]
        self.tickerType = [i.get('tickerType') for i in data]
        ticker = [i.get('ticker') for i in data]
        self.tickerId = [i.get('tickerId') for i in ticker]
        self.exchangeId = [i.get('exchangeId') for i in ticker]
        self.type = [i.get('type') for i in ticker]
        self.secType = [i.get('secType') for i in ticker]
        self.regionId = [i.get('regionId') for i in ticker]
        self.regionCode = [i.get('regionCode') for i in ticker]
        self.currencyId = [i.get('currencyId') for i in ticker]
        self.currencyCode = [i.get('currencyCode') for i in ticker]
        self.name = [i.get('name') for i in ticker]
        self.symbol = [i.get('symbol') for i in ticker]
        self.disSymbol = [i.get('disSymbol') for i in ticker]
        self.disExchangeCode = [i.get('disExchangeCode') for i in ticker]
        self.exchangeCode = [i.get('exchangeCode') for i in ticker]
        self.listStatus = [i.get('listStatus') for i in ticker]
        self.template = [i.get('template') for i in ticker]
        self.derivativeSupport = [i.get('derivativeSupport') for i in ticker]
        self.futuresSupport = [i.get('futuresSupport') for i in ticker]
        self.tinyName = [i.get('tinyName') for i in ticker]
        self.isPTP = [i.get('isPTP') for i in ticker]
        self.issuerRegionId = [i.get('issuerRegionId') for i in ticker]
        self.shariahFlag = [i.get('shariahFlag') for i in ticker]
        self.overnightTradeFlag = [i.get('overnightTradeFlag') for i in ticker]
        self.action = [i.get('action') for i in data]
        self.quantity = [i.get('quantity') for i in data]
        self.tickerId = [i.get('tickerId') for i in data]
        self.belongTickerId = [i.get('belongTickerId') for i in data]
        self.optionType = [i.get('optionType') for i in data]
        self.optionExpireDate = [i.get('optionExpireDate') for i in data]
        self.optionExercisePrice = [i.get('optionExercisePrice') for i in data]
        self.symbol = [i.get('symbol') for i in data]
        self.underlyingSymbol = [i.get('underlyingSymbol') for i in data]
        self.occExpireDate = [i.get('occExpireDate') for i in data]
        self.optionContractMultiplier = [i.get('optionContractMultiplier') for i in data]
        self.optionContractDeliverable = [i.get('optionContractDeliverable') for i in data]
        self.lastPrice = [i.get('lastPrice') for i in data]
        self.belongTradePrice = [i.get('belongTradePrice') for i in data]
        self.costPrice = [i.get('costPrice') for i in data]
        self.totalCost = [i.get('totalCost') for i in data]
        self.currency = [i.get('currency') for i in data]
        self.marketValue = [i.get('marketValue') for i in data]
        self.unrealizedProfitLoss = [i.get('unrealizedProfitLoss') for i in data]
        self.unrealizedProfitLossRate = [i.get('unrealizedProfitLossRate') for i in data]
        self.unrealizedProfitLossBase = [i.get('unrealizedProfitLossBase') for i in data]
        self.proportion = [i.get('proportion') for i in data]
        self.optionCycle = [i.get('optionCycle') for i in data]
        self.updatePositionTime = [i.get('updatePositionTime') for i in data]
        self.optionCanExercise = [i.get('optionCanExercise') for i in data]
        self.recentlyExpireFlag = [i.get('recentlyExpireFlag') for i in data]
        self.remainDay = [i.get('remainDay') for i in data]
        self.isLending = [i.get('isLending') for i in data]
        self.canFract = [i.get('canFract') for i in data]
        self.amOrPm = [i.get('amOrPm') for i in data]
        self.expirationType = [i.get('expirationType') for i in data]
        self.standardOption = [i.get('standardOption') for i in data]



        self.data_dict ={
            'option_id': self.tickerId,
            'ticker_id': self.belongTickerId,
            'leg_id': [i.get('legId') for i in data],
            'broker_id': [i.get('brokerId') for i in data],
            'asset_type': [i.get('assetType') for i in data],
            'ticker_type': [i.get('tickerType') for i in data],
            'ticker': [i.get('ticker') for i in data],
            'action': [i.get('action') for i in data],
            'quantity': [i.get('quantity') for i in data],
            'belong_ticker_id': [i.get('belongTickerId') for i in data],
            'option_type': [i.get('optionType') for i in data],
            'option_expire_date': [i.get('optionExpireDate') for i in data],
            'option_exercise_price': [i.get('optionExercisePrice') for i in data],
            'symbol': [i.get('symbol') for i in data],
            'underlying_symbol': [i.get('underlyingSymbol') for i in data],
            'occ_expire_date': [i.get('occExpireDate') for i in data],
            'option_contract_multiplier': [i.get('optionContractMultiplier') for i in data],
            'option_contract_deliverable': [i.get('optionContractDeliverable') for i in data],
            'last_price': [i.get('lastPrice') for i in data],
            'belong_trade_price': [i.get('belongTradePrice') for i in data],
            'cost_price': [i.get('costPrice') for i in data],
            'total_cost': [i.get('totalCost') for i in data],
            'currency': [i.get('currency') for i in data],
            'market_value': [i.get('marketValue') for i in data],
            'unrealized_profit_loss': [i.get('unrealizedProfitLoss') for i in data],
            'unrealized_profit_loss_rate': [i.get('unrealizedProfitLossRate') for i in data],
            'unrealized_profit_loss_base': [i.get('unrealizedProfitLossBase') for i in data],
            'proportion': [i.get('proportion') for i in data],
            'option_cycle': [i.get('optionCycle') for i in data],
            'update_position_time': [i.get('updatePositionTime') for i in data],
            'option_can_exercise': [i.get('optionCanExercise') for i in data],
            'recently_expire_flag': [i.get('recentlyExpireFlag') for i in data],
            'remain_day': [i.get('remainDay') for i in data],
            'is_lending': [i.get('isLending') for i in data],
            'can_fract': [i.get('canFract') for i in data],
            'am_or_pm': [i.get('amOrPm') for i in data],
            'expiration_type': [i.get('expirationType') for i in data],
            'standard_option': [i.get('standardOption') for i in data]
        }


        self.as_dataframe = pd.DataFrame(self.data_dict)