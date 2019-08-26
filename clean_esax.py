#!/usr/bin/env python3
import pandas as pd
import numpy as np
import json
from functools import partial

esax = pd.read_csv("esax.csv")

socials_to_clean = [
    'facebook',
    'twitter',
    'youtube',
    'website',
    'pinterest',
    'google_plus',
    'instagram',
    'linkedin'
]

for social_type in socials_to_clean:

    json_array_to_field_map = partial(map, lambda dic: dic[social_type + '_json' + '-href'])
    
    social_href_joined_list = (esax[social_type + '_json']
        .apply(json.loads)
        .apply(json_array_to_field_map)
        .apply(lambda lst: '\n'.join(lst))
    )

    esax[social_type] = social_href_joined_list

#Special case where member page href was company website
cimc_crit = esax['organisation'] == 'CIMC'
esax.loc[cimc_crit, 'website'] = esax.loc[cimc_crit, 'organisation_page-href']

clean_columns = [
    'organisation',
    'sponsor_level',
    'website',
    'facebook',
    'linkedin',
    'instagram',
    'twitter',
    'youtube',
    'pinterest',
    'google_plus',
]

esax[clean_columns].to_csv('esax_clean.csv', index=False)
