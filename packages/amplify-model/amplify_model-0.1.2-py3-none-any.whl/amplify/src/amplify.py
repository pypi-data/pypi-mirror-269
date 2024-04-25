from .flex_calculation import *
from .data_classes import *


class AmplifyWrapper:

    def __init__(self, *, 
        max_p_bat: int,
        min_p_bat: int,
        capacity_energy: int,
        efficiency_charge: float,
        efficiency_discharge: float,
        soh: float = 1,
        problem_detection_horizon: int = 4 * 60 * 60,
        file_path_time_measures = None
    ):
        self.flex_calculator = FlexCalculator(
            max_p_bat=max_p_bat,
            min_p_bat=min_p_bat,
            capacity_energy=capacity_energy,
            efficiency_charge=efficiency_charge,
            efficiency_discharge=efficiency_discharge,
            soh=soh,
            problem_detection_horizon=problem_detection_horizon
        )
        if file_path_time_measures is not None:
            self.measure_time = True
            self.file_path_time_measures = file_path_time_measures
            print(self.file_path_time_measures)
        else:
            self.measure_time = False

    def get_pure_flexibility(self, *, 
        forecast: List[int],
        p_max_ps: List[int],
        mpos: List[int],
        cap_mpos: List[int] = None,
        curr_soc: float,
        final_min_soc: float = 0.0,
        final_max_soc: float = 1.0,
        avg_p_bat_of_curr_interval: int,
        passed_time_of_curr_interval: int,
        res: int = 15 * 60,
        t_start: int
    ):
        if self.measure_time:
            t_start = time.time()

        pure_flex: FlexibilityCalculation = \
        self.flex_calculator.calculate_total_flex(
            forecast=forecast,
            p_max_ps=p_max_ps,
            mpos=mpos,
            cap_mpos=cap_mpos,
            curr_soc=curr_soc,
            final_max_soc=final_max_soc,
            final_min_soc=final_min_soc,
            avg_p_bat_of_curr_interval=avg_p_bat_of_curr_interval,
            passed_time_of_curr_interval=passed_time_of_curr_interval,
            res=res,
            t_start=t_start,
        )
        
        if self.measure_time and pure_flex.problems == []:
            duration = round(time.time() - t_start, 6)
            with open(f'{self.file_path_time_measures}', mode='a') as f:
                f.write(f'{duration}, ')
            return pure_flex, duration
        else:
            return pure_flex, None

    def get_market_flexibility(self, *, 
        forecast: List[int],
        p_max_ps: List[int],
        mpos: List[int],
        cap_mpos: List[int] = None,
        curr_soc: float,
        final_min_soc: float = 0.0,
        final_max_soc: float = 1.0,
        avg_p_bat_of_curr_interval: int,
        passed_time_of_curr_interval: int,
        res: int = 15 * 60,
        t_start: int
    ):
        if self.measure_time:
            t_start = time.time()

        flex: FlexibilityCalculation = \
        self.flex_calculator.calculate_total_flex(
            forecast=forecast,
            p_max_ps=p_max_ps,
            mpos=mpos,
            cap_mpos=cap_mpos,
            curr_soc=curr_soc,
            final_max_soc=final_max_soc,
            final_min_soc=final_min_soc,
            avg_p_bat_of_curr_interval=avg_p_bat_of_curr_interval,
            passed_time_of_curr_interval=passed_time_of_curr_interval,
            res=res,
            t_start=t_start,
        )
        # print(flex)
        # print(mpos)
        market_flex: MarketFlexibilityCalculation = \
            self.change_flex_to_market_flex(flex=flex, mpos=mpos)
            
        if self.measure_time and market_flex.problems == []:
            duration = round(time.time() - t_start, 6)
            with open(f'{self.file_path_time_measures}', mode='a') as f:
                f.write(f'{duration}, ')
            return market_flex, duration
        else:
            return market_flex, None
    
    def change_flex_to_market_flex(self, flex, mpos):
        cumulated_mpos = 0
        allowed_max_power = []
        allowed_min_power = []
        allowed_max_energy_delta = []
        allowed_min_energy_delta = []

        for interval_no in range(len(flex.flex_with_mpo.allowed_max_power)):
            allowed_max_power.append(
                flex.flex_with_mpo.allowed_max_power[interval_no] -
                mpos[interval_no]
            )
            allowed_min_power.append(
                flex.flex_with_mpo.allowed_min_power[interval_no] -
                mpos[interval_no]
            )
            cumulated_mpos = cumulated_mpos + mpos[interval_no]

            if flex.flex_with_mpo.allowed_max_energy_delta[interval_no] is not None:
                allowed_max_energy_delta.append(
                    flex.flex_with_mpo.allowed_max_energy_delta[interval_no] -
                    cumulated_mpos * flex.res/3600
                )
            else:
                allowed_max_energy_delta.append(None)
            if flex.flex_with_mpo.allowed_min_energy_delta[interval_no] is not None:
                allowed_min_energy_delta.append(
                    flex.flex_with_mpo.allowed_min_energy_delta[interval_no] -
                    cumulated_mpos * flex.res/3600
                )
            else:
                allowed_min_energy_delta.append(None)

        flex_with_mpo = MarketFlexibility(
            allowed_max_energy_delta=allowed_max_energy_delta,
            allowed_min_energy_delta=allowed_min_energy_delta,
            allowed_max_power=allowed_max_power,
            allowed_min_power=allowed_min_power,
        )
        market_flex = MarketFlexibilityCalculation(
            t_create=int(time.time()),
            t_start=flex.t_start,
            res=flex.res,
            flex_with_mpo=flex_with_mpo,
            flex_without_mpo=flex.flex_without_mpo,
            problems=flex.problems
        )
        return market_flex

    def calculate_total_flex(self, *, 
        forecast: List[int],
        p_max_ps: List[int],
        mpos: List[int],
        cap_mpos: List[int] = None,
        curr_soc: float,
        final_min_soc: float = 0.0,
        final_max_soc: float = 1.0,
        avg_p_bat_of_curr_interval: int,
        passed_time_of_curr_interval: int,
        res: int = 15 * 60,
        t_start: int
    ):
        flex: FlexibilityCalculation = \
        self.flex_calculator.calculate_total_flex(
            forecast=forecast,
            p_max_ps=p_max_ps,
            mpos=mpos,
            cap_mpos=cap_mpos,
            curr_soc=curr_soc,
            final_max_soc=final_max_soc,
            final_min_soc=final_min_soc,
            avg_p_bat_of_curr_interval=avg_p_bat_of_curr_interval,
            passed_time_of_curr_interval=passed_time_of_curr_interval,
            res=res,
            t_start=t_start,
        )
        return flex

class Amplify(AmplifyWrapper):
    pass