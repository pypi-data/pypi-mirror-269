"""imp_vol - """
import types

import numpy as np
from scipy.optimize import fsolve
from scipy.stats import norm

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__: list = ["call", "put", "implied_volatility", "OptionCall", "OptionPut"]


CONSTS = types.SimpleNamespace()
CONSTS.OptionCall = 1
CONSTS.OptionPut = 2

OptionCall = CONSTS.OptionCall
OptionPut = CONSTS.OptionPut


def call(S, K, r, T, sigma):
    if T == 0:
        raise ValueError("T is 0")
    d_1 = (1 / (sigma * (np.sqrt(T)))) * (np.log(S / K) + (r + sigma**2 / 2) * (T))
    d_2 = d_1 - sigma * np.sqrt(T)
    call = norm.cdf(d_1) * S - norm.cdf(d_2) * K * np.exp(-r * (T))
    return call


def put(S, K, r, T, sigma):
    if T == 0:
        raise ValueError("T is 0")
    d_1 = (1 / (sigma * (np.sqrt(T)))) * (np.log(S / K) + (r + sigma**2 / 2) * (T))
    d_2 = d_1 - sigma * np.sqrt(T)
    put = norm.cdf(-d_2) * K * np.exp(-r * (T)) - norm.cdf(-d_1) * S
    return put


def implied_volatility(S, K, r, T, price, initial_val, option_type: int):
    match option_type:
        case CONSTS.OptionCall:
            func = call
        case CONSTS.OptionPut:
            func = put
        case _:
            raise RuntimeError(f"{option_type=} is not allowed.")

    def isolate_sigma(sigma):
        return func(S, K, r, T, sigma) - price

    iv = fsolve(isolate_sigma, initial_val)[0]
    return iv
