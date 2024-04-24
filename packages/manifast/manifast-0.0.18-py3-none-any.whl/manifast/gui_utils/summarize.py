#!/usr/bin/env python3
# coding=utf-8
'''
brief        :  
Author       : knightdby knightdby@163.com
Date         : 2024-04-24 13:08:21
FilePath     : /manifast/manifast/gui_utils/summarize.py
Description  : 
LastEditTime : 2024-04-24 16:22:56
LastEditors  : knightdby
Copyright (c) 2024 by Inc, All Rights Reserved.
'''
import itertools
from tabulate import tabulate

def precision_summarize(precisions_dict,headers=["category", "AP"]):

    """
    Summarize the precision results in a table.

    Args:
        precisions_dict (dict): a dictionary containing the precision results.

    Returns:
        str: the table as a string.
    """
    sorted_dict = {k: precisions_dict[k] for k in sorted(precisions_dict)}
    results_per_category=sorted_dict.items()
    N_COLS = min(6, len(results_per_category) * 2)
    results_flatten = list(
        itertools.chain(*results_per_category))
    results_2d = itertools.zip_longest(
        *[results_flatten[i::N_COLS] for i in range(N_COLS)])
    table = tabulate(
        results_2d,
        tablefmt="pipe",
        floatfmt=".3f",
        headers=headers * (N_COLS // 2),
        numalign="left",
    )
    return table

def precision_summarize_small(small_dict):
    """
    Create a small table using the keys of small_dict as headers. This is only
    suitable for small dictionaries.

    Args:
        small_dict (dict): a result dictionary of only a few items.

    Returns:
        str: the table as a string.
    """
    sorted_dict = {k: small_dict[k] for k in sorted(small_dict)}
    keys, values = tuple(zip(*sorted_dict.items()))
    table = tabulate(
        [values],
        headers=keys,
        tablefmt="pipe",
        floatfmt=".3f",
        stralign="center",
        numalign="center",
    )
    return table


def experiment_summarize(experiment_dict_):
    """
    Create a summary of an experiment.

    Args:
        experiment_dict_ (dict): a dictionary containing the results of an
            experiment.
             dictionary has the following format:
            {'name': {'score': xxx, 'precision_div': {}, 'precision_sum': {}}}

    Returns:
        str: the summary as a string.
    """
    experiment_dict = {key: value for key, value in sorted(
    experiment_dict_.items(), key=lambda item: float(item[1]['score']), reverse=True)}

    summarize_text=''
    # summarize_text+="-----------------summary-----------------\n"
    score_sum=[['exp_name','score']]
    for key, sub_dict in experiment_dict.items():
        score_sum.append([key,sub_dict['score']]) 
    score_info=tabulate(score_sum,
                       tablefmt= "heavy_outline",
                        headers="firstrow",
                             showindex="always",
                        numalign="center",
                             )+'\n\n'
    print(score_info)
    summarize_text+=score_info
    # summarize_text+="\n-----------------dividual-----------------\n"
    for key, sub_dict in experiment_dict.items():
        summarize_text+=f"name:  {key}\n"
        summarize_text+=f"score: {sub_dict['score']}\n"
        summarize_text+='++++'*20+'\n'
        
        for key_i, value_i in sub_dict.items():
            if '_sum' in key_i:
                key_i=key_i.replace('_sum','')
                # summarize_text+=f"{key_i}:\n"
                table = precision_summarize_small(value_i)+'\n'
                summarize_text+=table
        for key_i, value_i in sub_dict.items():
            if '_div' in key_i:
                key_i=key_i.replace('_div','')
                # summarize_text+=f"{key_i}:\n"
                table = precision_summarize(value_i)+'\n'
                summarize_text+=table
        for key_i, value_i in sub_dict.items():
            if '_sum' not in key_i and '_div' not in key_i and 'score' not in key_i:
                # summarize_text+=f"{key_i}:\n"
                summarize_text+=f"{sub_dict}:\n"
        summarize_text+='++++'*20+'\n\n\n'
    return summarize_text
