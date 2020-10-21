def fitness_token_replay(log, model):
    traces = []
    ens = []
    for trace in log:
        t = []
        for event in log[trace]:
            t.append(event['concept:name'])
        if t not in traces:
            traces.append(t)
            ens.append(1)
        else:
            ens[traces.index(t)] += 1
    nm = 0.0
    nc = 0.0
    nr = 0.0
    np = 0.0
    for i in range(len(traces)):
        trace = traces[i]
        n = ens[i]
        model.reset()
        m = 0
        r = 0
        c = 0
        p = 1
        for event in trace:
            missing = model.enable(model.transition_name_to_id(event))
            m += missing
            produced, consumed = model.fire_transition(model.transition_name_to_id(event))
            p += produced
            c += consumed
        remaining = model.get_remaining_tokens()
        r += remaining
        last_tokens = model.get_last_token()
        if last_tokens == 0:
            m += 1
        elif last_tokens > 1:
            r += last_tokens - 1
        c += 1
        nm += n*m
        nc += n*c
        nr += n*r
        np += n*p
    f = (1 - (nm/nc))/2 + (1 - (nr/np))/2
    return f
