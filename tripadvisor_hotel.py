# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 18:39:20 2017

@author: greg
"""

from lxml import html
import requests
from collections import OrderedDict
import pprint
import json
import argparse

def parse(url):
    print ("Fetching "+url)
    response = requests.get(url).text
    parser = html.fromstring(response)
    
    XPATH_RATING = '//div[@id="ratingFilter"]//ul//li'
    XPATH_NAME = '//h1[@property="name"]//text()'
    XPATH_HOTEL_RATING = '//span[@property="ratingValue"]//@content'
    XPATH_REVIEWS = '//a[@property="reviewCount"]/@content'
    XPATH_RANK = '//div[contains(@class,"popRanking")]//text()'
    XPATH_STREET_ADDRESS = "//div[@class='header_container']//span[@class='street-address']//text()"
    XPATH_LOCALITY  = '//div[@class="header_container"]//span[@property="addressLocality"]//text()'
    XPATH_ZIP = '//div[@class="header_container"]//span[@property="postalCode"]//text()'
    XPATH_COUNTRY = '//div[@class="header_container"]//span[@property="addressCountry"]//@content'
    XPATH_AMENITIES = '//div[@id="AMENITIES_TAB"]//div[contains(@class,"amenity_row")]' 
    XPATH_HIGHLIGHTS = '//div[@class="property_tags_wrap"]//li//text()'
    XPATH_OFFICIAL_DESCRIPTION = '//div[contains(@class,"additional_info")]//span[contains(@class,"tabs_descriptive_text")]//text()'
    XPATH_ADDITIONAL_INFO = '//div[@class="additional_info_amenities"]//div[@class="content"]//text()'
    
    ratings = parser.xpath(XPATH_RATING)
    raw_name = parser.xpath(XPATH_NAME)
    raw_rank = parser.xpath(XPATH_RANK)
    raw_street_address = parser.xpath(XPATH_STREET_ADDRESS)
    raw_locality = parser.xpath(XPATH_LOCALITY)
    raw_zipcode =  parser.xpath(XPATH_ZIP)
    raw_country = parser.xpath(XPATH_COUNTRY)
    raw_review_count = parser.xpath(XPATH_REVIEWS)
    raw_rating = parser.xpath(XPATH_HOTEL_RATING)
    amenities = parser.xpath(XPATH_AMENITIES)
    raw_highlights = parser.xpath(XPATH_HIGHLIGHTS)
    raw_official_description = parser.xpath(XPATH_OFFICIAL_DESCRIPTION)
    raw_additional_info = parser.xpath(XPATH_ADDITIONAL_INFO)

                    
    name = ''.join(raw_name).strip() if raw_name else None
    rank = ''.join(raw_rank).strip() if raw_rank else None
    street_address = ' '.join(raw_street_address).strip() if raw_street_address else None
    locality = ' '.join(raw_locality).strip() if raw_locality else None
    zipcode = ''.join(raw_zipcode).strip() if raw_zipcode else None
    country  = ' '.join(raw_country).strip() if raw_country else None
    review_count = ''.join(raw_review_count).strip() if raw_review_count else None
    hotel_rating = ''.join(raw_rating).strip() if raw_rating else None
    official_description = ' '.join(' '.join(raw_official_description).split()) if raw_official_description else None
    additional_info = ' '.join(''.join(raw_additional_info).split()) if raw_additional_info else None
    cleaned_highlights = filter(lambda x:x != '\n', raw_highlights)
    
    highlights = ','.join(cleaned_highlights).replace('\n','')
    # Ordereddict is for preserve the site order
    ratings_dict = OrderedDict()
    for rating in ratings:
        XPATH_RATING_KEY = './/div[@class="row_label"]//text()'
        XPATH_RATING_VALUE = './/span[@class="row_bar"]/following-sibling::span//text()'

        raw_rating_key = rating.xpath(XPATH_RATING_KEY)
        raw_rating_value = rating.xpath(XPATH_RATING_VALUE)

        cleaned_rating_key = ''.join(raw_rating_key).replace('\n','')
        cleaned_rating_value = ''.join(raw_rating_value).replace('\n','')
        ratings_dict.update({cleaned_rating_key:cleaned_rating_value})
    

    amenity_dict = OrderedDict()
    for amenity in amenities:
        XPATH_AMENITY_KEY = './/div[@class="amenity_hdr"]//text()'
        XPATH_AMENITY_VALUE = './/div[@class="amenity_lst"]//li/text()'

        raw_amenity_key = amenity.xpath(XPATH_AMENITY_KEY)
        raw_amenity_value = amenity.xpath(XPATH_AMENITY_VALUE)
        cleaned_aminity_value = filter(lambda x:x != ' ', raw_amenity_value)

        amenity_key = ''.join(raw_amenity_key).replace('\n','')
        amenity_value = ' ,'.join(cleaned_aminity_value).replace('\n','')
        amenity_dict.update({amenity_key:amenity_value})
    
    address = {        'street_address':street_address,
                    'locality':locality,
                    'zipcode':zipcode,
                    'country':country
    }

    data = {
                'address':address,
                'ratings':ratings_dict,
                'amenities':amenity_dict,
                'official_description':official_description,
                'additional_info':additional_info,
                'rating':hotel_rating,
                'review_count':review_count,
                'name':name,
                'rank':rank,
                'highlights':highlights
    }

    return data

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url',help='Tripadvisor hotel url')
    args = parser.parse_args()
    url = args.url
    scraped_data = parse(url)
    with open('tripadvisor_hotel_scraped_data.json','w') as f:
        json.dump(scraped_data,f,indent=4)
