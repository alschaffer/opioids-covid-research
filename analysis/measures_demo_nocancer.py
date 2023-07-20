###################################################
# This script creates monthly counts/rates of opioid
# prescribing for any opioid prescribing, new opioid prescribing,
# and high dose/long-acting prescribing by demographics categories
###################################################

from ehrql import Dataset, case, when, months, days, years, INTERVAL, Measures
from ehrql.tables.beta.tpp import (
    patients, 
    medications, 
    addresses,
    practice_registrations,
    clinical_events)

import codelists

from dataset_definition import make_dataset

index_date = INTERVAL.start_date

dataset = make_dataset(index_date=index_date)

measures = Measures()

# Total denominator
denominator = (
        (patients.age_on(index_date) >= 18) 
        & (patients.age_on(index_date) < 110)
        & ((patients.sex == "male") | (patients.sex == "female"))
        & (patients.date_of_death.is_after(index_date) | patients.date_of_death.is_null())
        & (practice_registrations.for_patient_on(index_date).exists_for_patient())
        & (~dataset.cancer)
    )

# Opioid naive denominator
denominator_naive = (
       denominator 
       & dataset.opioid_naive
    )

measures.define_defaults(intervals=months(54).starting_on("2018-01-01"))



# Without cancer

# By demographics - overall prescribing
measures.define_measure(
    name="opioid_any_age_nocancer", 
    numerator=dataset.opioid_any,
    denominator=denominator,
    group_by={"age_group": dataset.age_group}
    )

measures.define_measure(
    name="opioid_any_sex_nocancer", 
    numerator=dataset.opioid_any,
    denominator=denominator,
    group_by={"sex": dataset.sex}
    )

measures.define_measure(
    name="opioid_any_region_nocancer", 
    numerator=dataset.opioid_any,
    denominator=denominator,
    group_by={"region": dataset.region}
    )

measures.define_measure(
    name="opioid_any_imd_nocancer",  
    numerator=dataset.opioid_any,
    denominator=denominator,
    group_by={"imd": dataset.imd10}
    )

measures.define_measure(
    name="opioid_any_eth6_nocancer", 
    numerator=dataset.opioid_any,
    denominator=denominator, 
    group_by={"ethnicity6": dataset.ethnicity6}
    )

measures.define_measure(
    name="opioid_any_carehome_nocancer", 
    numerator=dataset.opioid_any,
    denominator=denominator,
    group_by={"carehome": dataset.carehome}
    )

# By demographics - new prescribing
measures.define_measure(
    name="opioid_new_age_nocancer", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"age_group": dataset.age_group}
    )

measures.define_measure(
    name="opioid_new_sex_nocancer", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"sex": dataset.sex}
    )

measures.define_measure(
    name="opioid_new_region_nocancer", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"region": dataset.region}
    )

measures.define_measure(
    name="opioid_new_imd_nocancer", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"imd": dataset.imd10}
    )

measures.define_measure(
    name="opioid_new_eth6_nocancer", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"ethnicity6": dataset.ethnicity6}
    )

measures.define_measure(
    name="opioid_new_carehome_nocancer", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"carehome": dataset.carehome}
    )
