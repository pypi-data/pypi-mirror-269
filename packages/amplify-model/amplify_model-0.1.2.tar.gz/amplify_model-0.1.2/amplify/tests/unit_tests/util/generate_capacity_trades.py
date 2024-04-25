from amplify.src.flex_calculation import *

def generate_short_capacity_charge_trade(flex: FlexibilityCalculation, mpos, startinterval_no):
    """

    """
    # place short capacity trades
    # size cap-mpos
    if startinterval_no == 0:
        start_energy_max = 0
        start_energy_min = 0
    else:
        start_energy_max = flex_before_trades.flex_with_mpo.allowed_max_energy_delta[startinterval_no-1]
        start_energy_min = flex_before_trades.flex_with_mpo.allowed_min_energy_delta[startinterval_no-1]
    # check energy 0 possible
    if start_energy_max < flex_before_trades.flex_with_mpo.allowed_min_energy_delta[startinterval_no] or \
        start_energy_min > flex_before_trades.flex_with_mpo.allowed_max_energy_delta[startinterval_no]:
        continue
    # check energy max
    available_energy_max = flex_before_trades.flex_with_mpo.allowed_max_energy_delta[startinterval_no] - start_energy_min
    available_power_max = available_energy_max / parameter_set['res'] * 3600
    # check energy min
    available_energy_min = flex_before_trades.flex_with_mpo.allowed_min_energy_delta[startinterval_no] - start_energy_max
    available_power_min = available_energy_min / parameter_set['res'] * 3600
    # check power max/min and size cap_mpo
    cap_mpo_max = max(0, min(available_power_max,
        flex_before_trades.flex_with_mpo.allowed_max_power[startinterval_no]))
    cap_mpo_min = min(0, max(available_power_min,
        flex_before_trades.flex_with_mpo.allowed_min_power[startinterval_no]))

def generate_short_capacity_discharge_trade(flex: FlexibilityCalculation, mpos, startinterval_no):
    """

    """
    for startinterval_no in range(len(flex_before_trades.flex_with_mpo.allowed_min_power)):
    # place short capacity trades
        # size cap-mpos
        if startinterval_no == 0:
            start_energy_max = 0
            start_energy_min = 0
        else:
            start_energy_max = flex_before_trades.flex_with_mpo.allowed_max_energy_delta[startinterval_no-1]
            start_energy_min = flex_before_trades.flex_with_mpo.allowed_min_energy_delta[startinterval_no-1]
        # check energy 0 possible
        if start_energy_max < flex_before_trades.flex_with_mpo.allowed_min_energy_delta[startinterval_no] or \
            start_energy_min > flex_before_trades.flex_with_mpo.allowed_max_energy_delta[startinterval_no]:
            continue
        # check energy max
        available_energy_max = flex_before_trades.flex_with_mpo.allowed_max_energy_delta[startinterval_no] - start_energy_min
        available_power_max = available_energy_max / parameter_set['res'] * 3600
        # check energy min
        available_energy_min = flex_before_trades.flex_with_mpo.allowed_min_energy_delta[startinterval_no] - start_energy_max
        available_power_min = available_energy_min / parameter_set['res'] * 3600
        # check power max/min and size cap_mpo
        cap_mpo_max = max(0, min(available_power_max,
            flex_before_trades.flex_with_mpo.allowed_max_power[startinterval_no]))
        cap_mpo_min = min(0, max(available_power_min,
            flex_before_trades.flex_with_mpo.allowed_min_power[startinterval_no]))