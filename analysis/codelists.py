######################################

# Some covariates used in the study are created from codelists of clinical conditions or 
# numerical values available on a patient's records.
# This script fetches all of the codelists identified in codelists.txt from OpenCodelists.

######################################


# --- IMPORT STATEMENTS ---

## Import code building blocks from cohort extractor package
from databuilder.ehrql import codelist_from_csv

 
# --- CODELISTS ---

## Care home - use primis based on Schultze et al report (10.12688/wellcomeopenres.16737.1)
carehome_primis_codes = codelist_from_csv(
  "codelists/primis-covid19-vacc-uptake-longres.csv", 
  column = "code",
)

## Cancer 

###  Cancer - excluding lung/haem
oth_ca_codes = codelist_from_csv(
  "codelists/opensafely-cancer-excluding-lung-and-haematological-snomed.csv",
  column = "id"
)

### Cancer - lung
lung_ca_codes = codelist_from_csv(
  "codelists/opensafely-lung-cancer-snomed.csv",
  column = "id"
)

### Cancer - haematological
haem_ca_codes = codelist_from_csv(
  "codelists/opensafely-haematological-cancer-snomed.csv",
  column = "id"
)

### All cancer combined
cancer_codes = (
  oth_ca_codes +
  lung_ca_codes +
  haem_ca_codes
)

## Medication DM&D
### High dose, long-acting opioids 
hi_opioid_codes = codelist_from_csv(
  "codelists/opensafely-high-dose-long-acting-opioids-openprescribing-dmd.csv",
  column = "code",
)

### Non high dose, long-acting opioids 
non_hi_opioid_codes = codelist_from_csv(
  "codelists/opensafely-non-high-dose-long-acting-opioids-openprescribing-dmd.csv",
  column = "code",
)

### Any long-acting opioid
long_opioid_codes = (
  hi_opioid_codes +
  non_hi_opioid_codes
)

### Buccal opioids
buc_opioid_codes = codelist_from_csv(
  "codelists/opensafely-opioid-containing-medicines-buccal-nasal-and-oromucosal-excluding-drugs-for-substance-misuse-dmd.csv",
  column = "code",
)

### Inhaled opioids
inh_opioid_codes = codelist_from_csv(
  "codelists/opensafely-opioid-containing-medicines-inhalation-excluding-drugs-for-substance-misuse-dmd.csv",
  column = "code",
)

### Oral opioids
oral_opioid_codes = codelist_from_csv(
  "codelists/opensafely-opioid-containing-medicines-oral-excluding-drugs-for-substance-misuse-dmd.csv",
  column = "code",
)

### Parenteral opioids
par_opioid_codes = codelist_from_csv(
  "codelists/opensafely-opioid-containing-medicines-parenteral-excluding-drugs-for-substance-misuse-dmd.csv",
  column = "code",
)

### Rectal opioids
rec_opioid_codes = codelist_from_csv(
  "codelists/opensafely-opioid-containing-medicines-rectal-excluding-drugs-for-substance-misuse-dmd.csv",
  column = "code",
)

### Transdermal opioids
trans_opioid_codes = codelist_from_csv(
  "codelists/opensafely-opioid-containing-medicines-transdermal-excluding-drugs-for-substance-misuse-dmd.csv",
  column = "code",
)

### Other opioid
oth_opioid_codes = (
  buc_opioid_codes +
  inh_opioid_codes +
  rec_opioid_codes
)

### Any opioid
opioid_codes = (
  buc_opioid_codes +
  inh_opioid_codes +
  oral_opioid_codes +
  par_opioid_codes +
  rec_opioid_codes +
  trans_opioid_codes
)

# ## Diamorphine
# diamorph_opioid_codes = codelist_from_csv(
#   "codelists/anschaf-diamorphine-392faaa0-dmd.csv",
#   column = "dmd_id",
# )

## Ethnicity
ethnicity_codes_16 = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column="snomedcode",
    category_column="Grouping_16",
)

## Ethnicity
ethnicity_codes_6 = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    column="snomedcode",
    category_column="Grouping_6",
)

oxy_par_codes = codelist_from_csv(
  "codelists/opensafely-oxycodone-subcutaneous-dmd.csv",
  column = "code",
)

morph_par_codes = codelist_from_csv(
  "codelists/opensafely-morphine-subcutaneous-dmd.csv",
  column = "code",
)
