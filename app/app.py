import os
from flask import Flask
import serialized_redisimport redis


REDIS_HOST = os.environ.get('REDIS_HOST')
redis_client = Redis(host=REDIS_HOST)

def Fib(n):
    if n in [0,1]:
        return n
    else:
        return Fib(n-1)+Fib(n-2)


@app.route("/<number>", methods=['GET'])
def get_fibonacci_api(number):
    number = int(number)
    stored_value = redis_client.get(number)
    if stored_value:
        logger.info("For %s stored value is used" % number)
        return jsonify({number: stored_value.decode()}), 200
    new_value = Fib(number)
    logger.info("For %s new value is calculated" % number)
    redis_client.set(number, new_value)
    return jsonify({number: new_value}), 200