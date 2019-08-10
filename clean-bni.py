#!/usr/bin/env python3
import pandas as pd

bni = pd.read_csv("bnieast.csv")

remove_phone = [' ', r'\.', '-', 
    'Phone', 'Mobile', 'Fax', 
    'Freephone', 'Direct']

new_columns = [
    'organization',
    'first name',
    'last name',
    'phone',
    'mobile',
    'fax',
    'facebook-href',
    'linkedin-href',
    'instagram-href',
    'twitter-href',
    'business name',
    'type of business',
    'location',
    'direct',
    'free phone',
    'youtube-href',
    'pinterest-href',
    'website',
    'member-href',
]

phone_columns = [
    'phone',
    'mobile',
    'fax',
    'direct',
    'free phone'
]

new_names = {
    "facebook-href": 'facebook',
    "linkedin-href": 'linkedin',
    "instagram-href": 'instagram',
    "twitter-href": 'twitter',
    "youtube-href": 'youtube',
    "pinterest-href": 'pinterest',
}

clean_bni = (
    bni[new_columns]
    .sort_values(['organization', 'last name'])
    .rename(new_names, axis=1)
)

clean_bni[phone_columns] = (
    clean_bni[phone_columns]
    .astype(str)
    .replace(to_replace=remove_phone, value='', regex=True)
)

print(clean_bni[phone_columns].head())
print(clean_bni)

clean_bni = clean_bni.replace(to_replace='nan', value='')

clean_bni.to_csv("bni-clean.csv", na_rep="", index=False)
