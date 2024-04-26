# data type: ?
# model type: ?
# notes: 以线上数据作为数据源
import numpy as np


def get_params(**kwargs):
    # game_time: value range `[1, 90]`
    # curr_time (float): value range `(0.0, 90.0)`
    # slices: a list of `[a, b]`, value range `[1, 90]`
    null_value = kwargs.get("null_value", 0)

    shift_size = kwargs.get("shift_size", 1)

    window_size = kwargs.get("window_size", 4)

    slices = [(i, i + window_size - 1) for i in range(1, 1 + 91 - window_size, shift_size)]

    context_length = kwargs.get("context_length", 16)

    point_start = kwargs.get("point_start", 0.5)
    point_stop = kwargs.get("point_stop", 20)
    point_step = kwargs.get("point_step", 0.5)

    points = np.arange(point_start, point_stop, point_step, dtype=np.float32)

    in_channel = kwargs.get("in_channel", False)

    # N: ['total', 'total_asian', ...]
    bet_n_ins = set(kwargs.get("bet_n_ins", ["total"]))

    # CP: {0: '全场', 1: '上半场', 2: '下半场'}
    bet_cp_ins = set(kwargs.get("bet_cp_ins", [0]))

    params = {
        "null_value": null_value,
        "shift_size": shift_size,
        "window_size": window_size,
        "slices": slices,  # 根据参数`window_size`和`shift_size`自动计算
        "context_length": context_length,
        "point_start": point_start,
        "point_stop": point_stop,
        "point_step": point_step,
        "points": points,  # 根据参数`point_*`自动计算
        "in_channel": in_channel,
        "bet_n_ins": bet_n_ins,
        "bet_cp_ins": bet_cp_ins,
    }
    kwargs.update(params)
    return kwargs


def bets2pairs(bets: list[dict], **kwargs):
    # P: 盘口; E: 方向; C: 赔率
    # N: ['total', 'total_asian', ...]
    # CP: {0: '全场', 1: '上半场', 2: '下半场'}
    bet_n_ins = kwargs["bet_n_ins"]
    bet_cp_ins = kwargs["bet_cp_ins"]

    over_data = {}
    under_data = {}
    for bet in bets:
        if bet["N"] not in bet_n_ins:
            continue

        if bet["CP"] not in bet_cp_ins:
            continue

        bet_p = bet["P"]
        bet_e = bet["E"]
        bet_c = bet["C"]

        if bet_e == "over":
            over_data[bet_p] = bet_c
        elif bet_e == "under":
            under_data[bet_p] = bet_c

    outs = [(p, over_data[p], under_data[p]) for p in (over_data.keys() & under_data.keys())]
    return outs


def pairs2array(pairs: list, **kwargs):
    points = kwargs["points"]

    array = np.zeros((len(points), 3), dtype=np.float32)
    for p, c_over, c_under in pairs:
        array[np.abs(points - p) < 0.01, :] = (p, c_over, c_under)

    if kwargs["in_channel"]:
        array = array[:, np.newaxis]
    else:
        array = array.reshape((-1, 1, 1))

    # (n,1,3) or (n*3,1,1)
    return array


def parse_section_odds(section: dict, **kwargs):
    # "1"-上场, "2"-中场, "3"-下场
    titan = section["mapping_match"]["titan"]
    match_state = titan["match_state"]
    real_start_time = titan["real_start_time"]

    crawler_time = section["event_titan"]["crawler_end_time"]

    curr_time = -1
    if match_state == "1":
        curr_time = (crawler_time - real_start_time) / 60
        curr_time = 44.9 if curr_time > 44.9 else curr_time
    elif match_state == "3":
        curr_time = 45 + (crawler_time - real_start_time) / 60
        curr_time = 89.9 if curr_time > 89.9 else curr_time

    curr_time = curr_time if curr_time > 0.1 else -1

    game_time = int(curr_time + 1.0)

    pairs = bets2pairs(section["bets"]["bets"], **kwargs)
    array = pairs2array(pairs, **kwargs)

    return game_time, array


def parse_event_data(data: list):
    keys = [
        "goalIn",  # 进球
        "ownGoal",  # 乌龙
        "penaltyKick",  # 点球
    ]

    mat = np.zeros((len(data), 2), dtype=np.int32)
    for nrow, event in enumerate(data):
        for key in keys:
            if key in event:
                kind = event["kind"].lower()
                etime = event["time"][:-1].split("+")[0]
                mat[nrow, 0 if kind == "home" else 1] = int(etime)  # [1, 90]
                break

    # matrix[n,2]
    return mat


def parse_sections(sections: list[dict], **kwargs):
    # game_time: value range `[1, 90]`
    # curr_time (float): value range `(0.0, 90.0)`
    # slices: a list of `[a, b]`, `max(b)` is 90 - 比赛时间
    game_time_list, odds_list = [], []
    for section in sections:
        game_time, array = parse_section_odds(section, **kwargs)
        if game_time < 1:
            continue
        game_time_list.append(game_time)
        odds_list.append(array)

    atime = np.asarray(game_time_list, dtype=np.int32)
    aodds = np.concatenate(odds_list, axis=1)

    last_section = sections[-1]
    mat = parse_event_data(last_section["event_titan"]["events"])

    return atime, aodds, mat


def get_sample(curr_time, atime, aodds, mat, **kwargs):
    # game_time: value range `[1, 90]`
    # curr_time (float): value range `(0.0, 90.0)`
    # slices: a list of `[a, b]`, `max(b)` is 90 - 比赛时间
    null_value = kwargs["null_value"]

    slices = kwargs["slices"]
    slices = [s for s in slices if s[1] < curr_time]

    context_length = kwargs["context_length"]
    assert len(slices) >= context_length

    slices = slices[-context_length:]

    h, _, c = aodds.shape

    out = np.full((h, context_length, c), null_value, dtype=np.float32)
    for i, (a, b) in enumerate(slices):
        indexing = (a <= atime) & (atime <= b)
        view = aodds[:, indexing]
        if view.size > 0:
            out[:, i] = np.nan_to_num(np.mean(view, axis=1, where=view > 0), nan=null_value)

    oth = np.asarray([((1 <= mat) & (mat <= b)).sum(axis=0).tolist() + [a, b] for a, b in slices], dtype=np.float32)
    oth = np.tile(oth, (h, 1, 1))

    out = np.concatenate((out, oth), axis=2)
    return out
