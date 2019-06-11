def find_xs_in_y(xs, y):
    return [x for x in xs
            if y['begin'] <= x['begin'] and
            x['end'] <= y['end']]


def find_x_including_y(xs, y):
    for x in xs:
        if x['begin'] <= y['begin'] and y['end'] <= x['end']:
            return x
    return None
