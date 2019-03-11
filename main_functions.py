import vehicle_functions as vf
import numpy as np
import find_gear as fg


def gear_curves(my_car):
    '''Full load curves of speed and torque'''
    full_load_speeds, full_load_torque = vf.get_load_speed_n_torque(my_car)

    '''Speed and acceleration ranges and poitns for each gear'''
    speed_per_gear, acc_per_gear = vf.get_speeds_n_accelerations_per_gear(my_car, full_load_speeds, full_load_torque)

    '''Extract speed acceleration Cubic Slpines'''
    cs_acc_per_gear = vf.get_cubic_splines_of_speed_acceleration_relationship(my_car, speed_per_gear, acc_per_gear)

    '''Start/stop speed for each gear'''
    Start, Stop = vf.get_start_stop(my_car, speed_per_gear, acc_per_gear, cs_acc_per_gear)

    sp_bins = np.arange(0, 60.1, 0.1)
    '''Get resistances'''
    car_res_curve, car_res_curve_force, Alimit = vf.get_resistances(my_car, sp_bins)

    Res = []

    for gear, acc in enumerate(cs_acc_per_gear):
        start = Start[gear] * 0.9
        stop = Stop[-1]
        curve = vf.calculate_curve_to_use(acc, Alimit, car_res_curve, start, stop, sp_bins)
        Res.append(curve)

    return Res, cs_acc_per_gear, (Start, Stop)


def gear_curves_n_gs(my_car, gs_style, degree):
    '''Full load curves of speed and torque'''
    full_load_speeds, full_load_torque = vf.get_load_speed_n_torque(my_car)

    '''Speed and acceleration ranges and poitns for each gear'''
    speed_per_gear, acc_per_gear = vf.get_speeds_n_accelerations_per_gear(my_car, full_load_speeds, full_load_torque)

    '''Extract speed acceleration Cubic Slpines'''
    cs_acc_per_gear = vf.get_cubic_splines_of_speed_acceleration_relationship(my_car, speed_per_gear, acc_per_gear)

    '''Start/stop speed for each gear'''
    Start, Stop = vf.get_start_stop(my_car, speed_per_gear, acc_per_gear, cs_acc_per_gear)

    sp_bins = np.arange(0, 60.1, 0.1)
    '''Get resistances'''
    car_res_curve, car_res_curve_force, Alimit = vf.get_resistances(my_car, sp_bins)

    Res = []

    for gear, acc in enumerate(cs_acc_per_gear):
        start = Start[gear] * 0.9
        stop = Stop[-1]
        curve = vf.calculate_curve_to_use(acc, Alimit, car_res_curve, start, stop, sp_bins)
        Res.append(curve)

    '''Get gs'''
    coefs_per_gear = vf.get_tan_coefs(speed_per_gear, acc_per_gear, degree)
    Tans = fg.find_list_of_tans_from_coefs(coefs_per_gear, Start, Stop)
    gs = fg.gear_points_for_AIMSUN_tan(Tans, gs_style, Start, Stop)

    return Res, cs_acc_per_gear, (Start, Stop), gs


def gear_curves_n_gs_from_poly(my_car, gs_style, degree):
    '''Full load curves of speed and torque'''
    full_load_speeds, full_load_torque = vf.get_load_speed_n_torque(my_car)

    '''Speed and acceleration ranges and poitns for each gear'''
    speed_per_gear, acc_per_gear = vf.get_speeds_n_accelerations_per_gear(my_car, full_load_speeds, full_load_torque)

    '''Extract speed acceleration Splines'''
    coefs_per_gear = vf.get_tan_coefs(speed_per_gear, acc_per_gear, degree)
    poly_spline = vf.get_spline_out_of_coefs(coefs_per_gear, speed_per_gear[0][0])

    '''Start/stop speed for each gear'''
    Start, Stop = vf.get_start_stop(my_car, speed_per_gear, acc_per_gear, poly_spline)

    sp_bins = np.arange(0, 60.1, 0.1)
    '''Get resistances'''
    car_res_curve, car_res_curve_force, Alimit = vf.get_resistances(my_car, sp_bins)

    Res = []

    for gear, acc in enumerate(poly_spline):
        start = Start[gear] * 0.9
        stop = Stop[-1]
        curve = vf.calculate_curve_to_use(acc, Alimit, car_res_curve, start, stop, sp_bins)
        Res.append(curve)

    '''Get gs'''

    Tans = fg.find_list_of_tans_from_coefs(coefs_per_gear, Start, Stop)
    gs = fg.gear_points_for_AIMSUN_tan(Tans, gs_style, Start, Stop)

    return Res, poly_spline, (Start, Stop), gs

def gear_4degree_curves_with_linear_gs(my_car, gs_style):
    '''Full load curves of speed and torque'''
    full_load_speeds, full_load_torque = vf.get_load_speed_n_torque(my_car)

    '''Speed and acceleration ranges and poitns for each gear'''
    speed_per_gear, acc_per_gear = vf.get_speeds_n_accelerations_per_gear(my_car, full_load_speeds, full_load_torque)

    '''Extract speed acceleration Splines'''
    coefs_per_gear = vf.get_tan_coefs(speed_per_gear, acc_per_gear, 4)
    poly_spline = vf.get_spline_out_of_coefs(coefs_per_gear, speed_per_gear[0][0])

    '''Start/stop speed for each gear'''
    Start, Stop = vf.get_start_stop(my_car, speed_per_gear, acc_per_gear, poly_spline)

    sp_bins = np.arange(0, 60.1, 0.1)
    '''Get resistances'''
    car_res_curve, car_res_curve_force, Alimit = vf.get_resistances(my_car, sp_bins)

    Res = []

    for gear, acc in enumerate(poly_spline):
        start = Start[gear] * 0.9
        stop = Stop[-1]
        curve = vf.calculate_curve_to_use(acc, Alimit, car_res_curve, start, stop, sp_bins)
        Res.append(curve)

    '''Get gs'''
    gs = fg.gear_linear(speed_per_gear,gs_style)

    return Res, poly_spline, (Start, Stop), gs