import alpaca_trade_api as tradeapi
import config, time
from chalice import Chalice

app = Chalice(app_name='alpaca01')

#api_version v2 refers to the version that we'll use
#very important for the documentation
api = tradeapi.REST(config.key, config.sec, config.url, api_version='v2')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/alpaca01', methods=['POST'])
def alpaca01(): 
    request = app.current_request
    webhook_message = request.json_body
    
    if webhook_message['side'] == "buy":
                    data = api.submit_order(symbol=webhook_message['ticker'],
                            qty="1",
                            side=webhook_message['side'],
                            type="market",
                            time_in_force="gtc")

    else: 
        position = api.get_position(webhook_message['ticker'])
        data = api.submit_order(symbol=webhook_message['ticker'],
                qty=position.qty,
                side=webhook_message['side'],
                type="market",
                time_in_force="gtc")

    return {
        'webhook_message': webhook_message
    }