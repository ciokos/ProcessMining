import csv
import xml.etree.ElementTree as Et
from datetime import datetime

from PetriNet import PetriNet


def alpha(log):
    dg = dependency_graph(log)
    tw = []
    ti = []
    to = []
    for key1 in dg.keys():
        tw.append(key1)
        ti.append(key1)
        for key2 in dg[key1].keys():
            tw.append(key2)
    for key1 in dg.keys():
        for key2 in dg[key1].keys():
            if key2 in ti:
                ti.remove(key2)
    tw = list(set(tw))
    for transition in tw:
        if transition not in dg.keys():
            to.append(transition)

    successions = []
    causalities = []
    parallels = []
    choices = []

    for key1 in dg.keys():
        for key2 in dg[key1].keys():
            successions.append([key1, key2])
    for succession in successions:
        if [succession[1], succession[0]] not in successions:
            causalities.append(succession)
        else:
            parallels.append(succession)
    for transition1 in tw:
        for transition2 in tw:
            if [transition1, transition2] not in successions and [transition2, transition1] not in successions:
                choices.append([transition1, transition2])
    x = []
    for causality in causalities:
        a = causality[0]
        b = causality[1]
        for AB in x:
            copied = analyze_ab(a, b, AB, choices, causalities)
            if copied is not None and copied not in x:
                x.append(copied)
        x.append([[a], [b]])
    y = remove_subsets(x)


    petri_net = PetriNet()
    for i in range(len(tw)):
        petri_net.add_transition(tw[i], -i)
    petri_net.add_place(1)
    petri_net.add_marking(1)
    petri_net.add_place(2)
    for transition in ti:
        petri_net.add_edge(1, petri_net.transition_name_to_id(transition))
    for transition in to:
        petri_net.add_edge(petri_net.transition_name_to_id(transition), 2)
    place_counter = 3
    for AB in y:
        petri_net.add_place(place_counter)
        A = AB[0]
        B = AB[1]
        for a in A:
            petri_net.add_edge(petri_net.transition_name_to_id(a), place_counter)
        for b in B:
            petri_net.add_edge(place_counter, petri_net.transition_name_to_id(b))
        place_counter += 1
    return petri_net


def remove_subsets(x):
    y = list(x)
    for AB1 in x:
        for AB2 in x:
            if AB1 == AB2:
                continue
            if is_subset(AB1[0], AB2[0]) and is_subset(AB1[1], AB2[1]):
                if AB1 in y:
                    y.remove(AB1)
    return y


def is_subset(list1, list2):
    for elem in list1:
        if elem not in list2:
            return False
    return True


def analyze_ab(a, b, AB, choices, causalities):
    for A in AB[0]:
        if [a, A] not in choices:
            return
    for B in AB[1]:
        if [b, B] not in choices or [a, B] not in causalities:
            return
    tmp = list(AB)
    if a not in AB[0]:
        AB[0].append(a)
    if b not in AB[1]:
        AB[1].append(b)
    return tmp


def log_as_dictionary(f):
    rows = f.splitlines()
    rows = list(filter(None, rows))
    reader = csv.reader(rows, delimiter=';')
    parsed_csv = list(reader)
    cases = list(set([item[1] for item in parsed_csv]))
    log = {}
    for case in cases:
        events = []
        for row in parsed_csv:
            if row[1] == case:
                events.append(row)
        log[case] = events
    return log


# def dependency_graph(log):
#     dg = {}
#     for case in sorted(log.keys()):
#         for i in range(len(log[case])-1):
#             task1 = log[case][i][0]
#             task2 = log[case][i+1][0]
#             dg[task1][task2] += 1
#     return dg

def dependency_graph(log):
    dg = {}
    for case in sorted(log.keys()):
        for i in range(len(log[case])-1):
            task1 = log[case][i]['concept:name']
            task2 = log[case][i+1]['concept:name']
            if task1 not in dg:
                dg[task1] = {}
            if task2 not in dg[task1]:
                dg[task1][task2] = 0
            dg[task1][task2] += 1
    return dg


def read_from_file(filename):
    prefix = '{http://www.xes-standard.org/}'
    root = Et.parse(filename).getroot()
    log = {}
    for trace in root.findall(prefix+'trace'):
        case_id = ''
        events = []
        for attr in trace.findall(prefix+'string'):
            attr_key = attr.attrib['key']
            if attr_key == 'concept:name':
                case_id = attr.attrib['value']
                break

        for event in trace.findall(prefix+'event'):
            attributes = {}
            for attribute in event.findall('*'):
                key = attribute.attrib['key']
                value = attribute.attrib['value']
                to_type = attribute.tag.replace(prefix, "")
                if to_type == 'int':
                    value = int(value)
                elif to_type == 'date':
                    value = value.split('+')[0]
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                attributes[key] = value
            events.append(attributes)
        log[case_id] = events
    return log
