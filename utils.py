# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import streamlit as st
from pathlib import Path
import time
import numpy as np
import pandas as pd
from unittest import case

from pandas import Series

from API import FWCAPI

s = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/classifications.csv' )
t = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/payrates.csv' )
q = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/penalties.csv' )
r = pd.read_csv( 'https://raw.githubusercontent.com/toddaus/API/master/wage-allowances.csv' )
u = pd.read_csv( "https://raw.githubusercontent.com/toddaus/API/master/award_structure.csv" )


st.write( "## Hospitality Wage Checker" )

age = st.selectbox(
    'Are you employed as Adult or as a Junior?',
    ('Adult', 'Junior') )

with st.expander( "See explanation" ):
    if age == 'Adult':
        st.write( "Adult employee means an employee who is 21 years of age or over" )
    elif age == 'Junior':
        st.write(
            "An employee who is less than 21 years of age and who is not undertaking a nationally recognised traineeship or apprenticeship" )
    else:
        st.write( "" )

option = st.selectbox(
    'What is your working arrangement?',
    ('Full Time', 'Part Time', 'Casual') )

with st.expander( "See explanation" ):
    if option == 'Part Time':
        st.write(
            "A part-time employee is an employee who is engaged to work at least 8 and fewer than 38 ordinary hours per week (or, if the employer operates a roster, an average of at least 8 and fewer than 38 hours per week over the roster cycle); and reasonably predictable hours of work." )
    elif option == 'Casual':
        st.write(
            "A person is a casual employee if there is no firm advance commitment to ongoing work with an agreed pattern of work" )
    elif option == 'Full Time':
        st.write(
            "An employee who is engaged to work an average of 38 ordinary hours per week is a full-time employee" )
    else:
        st.write( "" )

if option == 'Part Time':
    pt_hrs = st.number_input( "What hours are you employed for?", min_value=8.0, max_value=38.0, value=8.0,step = 0.5)

if age != 'Junior':

    if option == 'Full Time' and age == 'Adult':
        clause_description_id = 'Adult full-time and part-time employees'
        clause_description_id2 = 'Hospitality Employees'
    elif option == 'Part Time' and age == 'Adult':
        clause_description_id = 'Adult full-time and part-time employees'
        clause_description_id2 = 'Hospitality Employees'
    elif option == 'Casual' and age == 'Adult':
        clause_description_id = 'Adult casual employees'
        clause_description_id2 = 'Hospitality Employees'
    else:
        clause_description_id = ''

    job_filter = st.selectbox( "What is your role?", pd.unique( u['Profession'] ) )
    u2 = u[u['Profession'] == job_filter]

    job_filter2 = st.selectbox( "What is your grade?", pd.unique( u2['Grade'] ) )

    if job_filter == 'Introductory level':
        f = True
    else:
        f = False
    print( f )
    if job_filter2 != 'Null':
        u3 = u2[u2['Grade'] == job_filter2]
        indexx = u3.index[0]  # obtain the line number of the result
        u4 = u3.at[indexx, 'Level']
        u5 = u3.at[indexx, 'Level_no']
    elif f is True:
        u4 = 'Introductory level'
        u5 = 1.0
    else:
        u4 = 'Level 5'
        u5 = 6.0

    profess = job_filter
    grade = job_filter2
    classification = u4
    classification_level_no = u5
    classification_id = profess + ' ' + grade

    if job_filter2 != 'Null':
        output = u3['Award_Desc'].iloc[0]
    else:
        output = u2['Award_Desc'].iloc[0]
    with st.expander( "See explanation" ):
        st.write(output)

elif age == "Junior":

    classification_id = st.selectbox(
        'What level are you currently on?',
        ('Introductory', 'Level 2', 'Level 3', 'Level 4', 'Level 5') )

    clause_description_id = 'Junior office employees'
    clause_description_id2 = 'Junior office employees'

    classification = st.selectbox(
        'What is your current age?',
        ('15 years of age and under', '16 years of age', '17 years of age', '18 years of age', '19 years of age',
         '20 years of age') )

    if classification_id == "Introductory":
        classification_level_no = 1.0
    elif classification_id == "Level 2":
        classification_level_no = 2.0
    elif classification_id == "Level 3":
        classification_level_no = 3.0
    elif classification_id == "Level 4":
        classification_level_no = 4.0
    elif classification_id == "Level 5":
        classification_level_no = 5.0
    else:
        classification_level_no = 1.0


def data(clause_description=None):
    # this section is the default code"""
    id_or_code = 'MA000009'

    # filtering utilising the latest published year
    s2 = s[s['published_year'] == int( max( s['published_year'] ) )]
    # further filtering by the clause_description utilising the string containing the clause_description_id2
    s3 = s2[s2['clause_description'].str.contains( clause_description_id2 )]
    # further filtering by the parent_classification_name utilising the string containing the cparent_classification_name_id

    if age == 'Junior':  # only need to filter at this level for juniors
        s4 = s3[s3['parent_classification_name'].str.contains( classification_id, na=False )]
    else:
        s4 = s3

    # further filtering by the classification utilising the string containing the classification
    s5 = s4[s4['classification'].str.contains( classification )]
    # obtain the result and save it against class_fixed_id"""
    class_fixed_id = (s5['classification_fixed_id'].iloc[0])
    # filtering utilising the latest published year
    t2 = t[t['published_year'] == int( max( t['published_year'] ) )]
    # further filtering by the classification_fixed_id utilising the string containing the class_fixed_id
    t3 = t2[t2['classification_fixed_id'] == class_fixed_id]
    # obtain the result and save it against base_pay_rate_id_a
    base_pay_rate_id_a = t3['base_pay_rate_id'].iloc[0]
    # filtering utilising the latest published year"""
    q2 = q[q['published_year'] == int( max( q['published_year'] ) )]
    q3 = q2[q2['base_pay_rate_id'] == base_pay_rate_id_a]

    # storing in dictionary results clause, penalty and value"""
    class_dict2 = dict(
        zip( (q3['clause_description']) + (q3['penalty_description']).str.lower(), q3['penalty_calculated_value'] ) )

    #  check for full time/part time or casual for weekend/rostered day or weekend clause specific clause
    if 'Adult full-time and part-time employees' in clause_description_id and option != 'Casual':
        dictionary( class_dict2, "Adult full-time and part-time employees", 'full' )

    elif 'Adult casual employees' in clause_description_id and option == 'Casual':
        dictionary( class_dict2, "Adult casual employees", "casual" )

    elif 'Junior office employees' in clause_description_id and option != 'Casual':
        dictionary( class_dict2, "Junior full-time and part-time office employees", 'full' )

    elif 'Junior office employees' in clause_description_id and option == 'Casual':
        dictionary( class_dict2, "Junior casual office employees", 'casual' )


def dictionary(arg1, arg2, arg3):
    try:
        hr_Ord = arg1[arg2 + "—ordinary and penalty ratesordinary hours"]
    except:
        hr_Ord = 0

    try:
        hr_OT3 = arg1[arg2 + "—overtime ratesmonday to friday - after 2 hours"]
    except:
        hr_OT3 = 0

    try:
        hr_OT02 = arg1[arg2 + "—overtime ratesmonday to friday - first 2 hours"]
    except:
        hr_OT02 = 0

    try:
        hr_Sat = arg1[arg2 + "—ordinary and penalty ratessaturday"]
    except:
        hr_Sat = 0

    try:
        hr_Sun = arg1[arg2 + "—ordinary and penalty ratessunday"]
    except:
        hr_Sun = 0

    try:
        hr_PH = arg1[arg2 + "—ordinary and penalty ratespublic holiday"]
    except:
        hr_PH = 0

    if arg3 != 'casual':
        try:
            hr_WR = arg1[arg2 + "—overtime ratesweekends and rostered days off"]
        except:
            hr_WR = 0

        try:
            hr_OTPH = arg1[arg2 + "—overtime ratespublic holiday"]
        except:
            hr_OTPH = 0

    if arg3 == 'casual':
        try:
            hr_WC = arg1[arg2 + "—overtime ratesweekends"]
        except:
            hr_WC = 0
        hr_OTPH = 0
        hr_PH = 0

    r2 = r[r['published_year'] == int( max( q['published_year'] ) )]
    wage_dict = dict( zip( r2['allowance'].str.strip(), r2['allowance_amount'] ) )
    hr_even = round( wage_dict['Penalty—Monday to Friday—7.00 pm to midnight'] + hr_Ord, 2 )
    hr_night = round( wage_dict['Penalty—Monday to Friday—midnight to 7.00 am'] + hr_Ord, 2 )
    All_Split2 = round( wage_dict['Split shift allowance—2 hours and up to 3 hours'], 2 )
    All_Split3 = round( wage_dict['Split shift allowance—More than 3 hours'], 2 )

    st.write( 'Your Ordinary Hourly Rate is $', str( '{:.2f}'.format( hr_Ord, 2 ) ) )
    st.write( 'Your 7pm to midnight Hourly Rate is $', str( '{:.2f}'.format( hr_even ) ) )
    st.write( 'Your Midnight to 7am Hourly Rate is $', str( '{:.2f}'.format( hr_night ) ) )
    st.write( 'Your Saturday Hourly Rate is $', str( '{:.2f}'.format( hr_Sat ) ) )
    st.write( 'Your Sunday Hourly Rate is $', str( '{:.2f}'.format( hr_Sun ) ) )
    st.write( 'Your Public Holiday Hourly Rate is $', str( '{:.2f}'.format( hr_PH ) ) )
    st.write( 'Your Overtime First Two Hours Rate is $', str( '{:.2f}'.format( hr_OT02 ) ) )
    st.write( 'Your Overtime After First Two Hours Rate is $', str( '{:.2f}'.format( hr_OT3 ) ) )
    st.write( 'Your Public Holiday Overtime Hourly Rate is $', str( '{:.2f}'.format( hr_OTPH ) ) )
    st.write( 'Split shift allowance—2 hours and up to 3 hours is $', str( '{:.2f}'.format( All_Split2 ) ) )
    st.write( 'Split shift allowance—More than 3 hours $', str( '{:.2f}'.format( All_Split3 ) ) )