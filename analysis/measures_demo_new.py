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

from dataset_definition import make_dataset_opioids, registrations

##########

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--start-date", type=str)
parser.add_argument("--intervals", type=int)

args = parser.parse_args()

start_date = args.start_date
intervals = args.intervals

##########

index_date = INTERVAL.start_date

dataset = make_dataset_opioids(index_date=index_date, end_date=index_date + months(1) - days(1))

##########

## Define demographic variables

age = patients.age_on(index_date)
dataset.age_group = case(
        when(age < 30).then("18-29"),
        when(age < 40).then("30-39"),
        when(age < 50).then("40-49"),
        when(age < 60).then("50-59"),
        when(age < 70).then("60-69"),
        when(age < 80).then("70-79"),
        when(age < 90).then("80-89"),
        when(age >= 90).then("90+"),
        default="missing",
)

dataset.sex = patients.sex 

imd = addresses.for_patient_on(index_date).imd_rounded
dataset.imd10 = case(
        when((imd >= 0) & (imd < int(32844 * 1 / 10))).then("1 (most deprived)"),
        when(imd < int(32844 * 2 / 10)).then("2"),
        when(imd < int(32844 * 3 / 10)).then("3"),
        when(imd < int(32844 * 4 / 10)).then("4"),
        when(imd < int(32844 * 5 / 10)).then("5"),
        when(imd < int(32844 * 6 / 10)).then("6"),
        when(imd < int(32844 * 7 / 10)).then("7"),
        when(imd < int(32844 * 8 / 10)).then("8"),
        when(imd < int(32844 * 9 / 10)).then("9"),
        when(imd >= int(32844 * 9 / 10)).then("10 (least deprived)"),
        default="unknown"
)

ethnicity6 = clinical_events.where(
        clinical_events.snomedct_code.is_in(codelists.ethnicity_codes_6)
    ).sort_by(
        clinical_events.date
    ).last_for_patient().snomedct_code.to_category(codelists.ethnicity_codes_6)

dataset.ethnicity6 = case(
    when(ethnicity6 == "1").then("White"),
    when(ethnicity6 == "2").then("Mixed"),
    when(ethnicity6 == "3").then("South Asian"),
    when(ethnicity6 == "4").then("Black"),
    when(ethnicity6 == "5").then("Other"),
    when(ethnicity6 == "6").then("Not stated"),
    default="Unknown"
)

dataset.region = practice_registrations.for_patient_on(index_date).practice_nuts1_region_name


#########################

measures = Measures()

measures.define_defaults(intervals=months(intervals).starting_on(start_date))

# Total denominator
denominator_naive = (
        (patients.age_on(index_date) >= 18) 
        & (patients.age_on(index_date) < 110)
        & ((patients.sex == "male") | (patients.sex == "female"))
        & (patients.date_of_death.is_after(index_date) | patients.date_of_death.is_null())
        & registrations(index_date, index_date).exists_for_patient()
        & dataset.opioid_naive
)

#########################

## Overall 
# By demographics - new prescribing
measures.define_measure(
    name="opioid_new_age", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"age_group": dataset.age_group}
    )

measures.define_measure(
    name="opioid_new_sex", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"sex": dataset.sex}
    )

measures.define_measure(
    name="opioid_new_region", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"region": dataset.region}
    )

measures.define_measure(
    name="opioid_new_imd", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"imd": dataset.imd10}
    )

measures.define_measure(
    name="opioid_new_eth6", 
    numerator=dataset.opioid_new,
    denominator=denominator_naive,
    group_by={"ethnicity6": dataset.ethnicity6}
    )

