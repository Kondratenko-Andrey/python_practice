from typing import List, Optional
import functools, operator
from flask import Flask, request
from itertools import product

app = Flask(__name__)


@app.route('/search/', methods=['GET'])
def search():
    cell_tower_ids: List[int] = request.args.getlist("cell_tower_id", type=int)

    if not cell_tower_ids:
        return f"You must specify at least one cell_tower_id", 400

    phone_prefixes: List[str] = request.args.getlist("phone_prefix")

    protocols: List[str] = request.args.getlist("protocol")

    signal_level: Optional[float] = request.args.get(
        "signal_level", type=float, default=None)

    return (
        f"Search for {cell_tower_ids} cell towers. Search criteria: "
        f"phone_prefixes={phone_prefixes}, "
        f"protocols={protocols}, "
        f"signal_level={signal_level}"
    )


@app.route('/sum_prod_arr/', methods=['GET'])
def sum_prod_arr():
    num_arr: List[int] = request.args.getlist('n', type=int)
    return f"""Сумма указанных чисел: {sum(num_arr)} 
Произведение указанных чисел: {functools.reduce(operator.mul, num_arr, 1)}"""


@app.route('/double_arr/', methods=['GET'])
def double_arr():
    arr_1: List[int] = request.args.getlist('a1', type=int)
    arr_2: List[int] = request.args.getlist('a2', type=int)
    result = list(product(arr_1, arr_2))
    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
