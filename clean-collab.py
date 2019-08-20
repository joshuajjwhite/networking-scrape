#!/usr/bin/env python3
import pandas as pd
import numpy as np
import json
from functools import partial

collab = pd.read_csv("collabspace.csv")

def print_all(pd_printable):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(pd_printable)

def get_series_not_null(df, column):
    return df.loc[df[column].notnull(), column]

def map_and_filter_json_series(series, map_crit=(lambda x: x), filter_crit=(lambda x: True)):
    return (
        series
        .apply(json.loads)
        .apply(partial(map, map_crit))
        .apply(partial(map, lambda string: string.strip()))
        .apply(partial(filter, filter_crit))
        .apply(list)
    )

def merge_to_unique_list(lst1, lst2):
    merged = ([] if lst1 is np.nan else lst1) + ([] if lst2 is np.nan else lst2)
    return list(dict.fromkeys(merged))

'''
Pull website out of general_contact
    - emails in this column are reflected in e-mail column so we can ditch them
'''
general_contact = get_series_not_null(collab, 'general_contact')
body_websites = map_and_filter_json_series(general_contact, 
    map_crit=lambda dic: dic['general_contact-href'], 
    filter_crit=lambda href: 'mailto:' not in href
)

'''
Pull websites from header_contact and combine them with general_contact websites
'''
header_contact = get_series_not_null(collab, 'header_contact')
object_to_header_map = lambda dic: dic['header_contact-href']
header_websites = map_and_filter_json_series(header_contact, 
    map_crit=lambda dic: dic['header_contact-href'].replace('http://http', 'http'), 
    filter_crit=lambda href: 'mailto:' not in href and 'members_search' not in href 
)

collab['website'] = body_websites
print_all(collab[['website']][collab['first_name'] == 'Hilda'])
collab['website'] = collab['website'].combine(header_websites, merge_to_unique_list)
print_all(collab[['website']][collab['first_name'] == 'Hilda'])

'''
Put contact column into webstite column
'''
contact_column_as_lists = (
    get_series_not_null(collab, 'contact')
    .apply(lambda website: [website])
)
collab['website'] = collab['website'].combine(contact_column_as_lists, merge_to_unique_list)

'''
Pull social accounts from member card
'''
member_card_socials = get_series_not_null(collab, 'social')
card_socials = map_and_filter_json_series(member_card_socials, map_crit=lambda dic: dic['social-href'])

social_and_filter_crit = {
    'facebook': lambda href: 'facebook' in href or 'fb' in href, 
    'instagram': lambda href: 'instagram' in href,
    'twitter': lambda href: 'twitter' in href or '@' in href,
}

for social, crit in social_and_filter_crit.items():
    collab[social] = (
        card_socials
        .apply(partial(filter, crit))
        .apply(list)
    )

print(collab[['twitter', 'facebook']][collab['first_name'] == 'Hilda'])

'''
Pull socials from header_social and merge unqiues to member card socials
'''
header_socials =  get_series_not_null(collab, 'header_social')
header_socials = map_and_filter_json_series(header_socials, map_crit=lambda dic: dic['header_social-href'].replace('http://', ''))

for social, crit in social_and_filter_crit.items():
    filtered_social = (
        header_socials
        .apply(partial(filter, crit))
        .apply(list)
    )

    collab[social] = collab[social].combine(filtered_social, merge_to_unique_list)

print(collab[['twitter','facebook']][collab['first_name'] == 'Hilda'])

list_columns_to_format = [
    'facebook',
    'instagram',
    'twitter',
    'website',
]

for series in list_columns_to_format:
    collab[series] = (
        collab[series]
        .apply(lambda lst: '\n'.join(lst))
    )

clean_columns = [
    'first_name',
    'last_name',
    'e-mail',
    'facebook',
    'instagram',
    'twitter',
    'website',
    'page-href',
]

#Manual correction. Missed during origional scraping
collab.loc[collab['facebook'] == 'https://www.facebook.com/RedMelog/', 'first_name'] = 'Melog'

# print_all(collab[['facebook', 'twitter', 'instagram']])
collab[clean_columns].to_csv('collab_clean.csv', index=False)