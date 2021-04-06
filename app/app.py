import os
from flask import Flask
import redis
import logging
from flask import jsonify


REDIS_HOST = os.environ.get('REDIS_HOST')
redis_client = Redis(host=REDIS_HOST)
app = Flask(__name__)
redis_client = redis.Redis(host=REDIS_HOST)
port = int(os.environ.get("PORT", 5000))

def Fib(n):
    if n in [0,1]:
        return n
    else:
        return Fib(n-1)+Fib(n-2)


@app.route("/<int:number>", methods=['GET'])
def get_fibonacci_api(number):
    stored_value = redis_client.get(number)
    if stored_value:
        logging.info("For %s stored value is used" % number)
        return jsonify({number: stored_value.decode()}), 200
    new_value = Fib(number)
    logging.info("For %s new value is calculated" % number)
    redis_client.set(number, new_value)
    return jsonify({number: new_value}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=port)
