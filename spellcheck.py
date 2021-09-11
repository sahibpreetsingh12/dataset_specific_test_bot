# Levenshtein distance https://www.youtube.com/watch?v=MiqoA-yF-0M

# or  https://medium.com/@ethannam/understanding-the-levenshtein-distance-equation-for-beginners-c4285a5604f0

# source http://norvig.com/spell-correct.html

# instead of big.txt we will will have a text file that contains all our glosaary

import re


from collections import Counter


master_dic_dataset_name = {
        'agricultural data' : 'agcensus_crop',
        'agricluture' : 'agcensus_crop', 
        'agri data' : 'agcensus_crop',
        'agricuture data':'agcensus_crop',
        'agriculture':'agcensus_crop',
        'agriculture census': 'agcensus_crop',
        'agcensus':'agcensus_crop',
        'rainfall':'rainfall',
        'rain data':'rainfall',
        'rainfall data':'rainfall',
        'agricultural census':'agcensus_crop',
        'rain figures':'rainfall',
        'sales of fertiliser':'fertiliser_sales',
        'sales of fertilisers':'fertiliser_sales',
        'fertiliser sales':'fertiliser_sales',
        'fertilizer sales data':'fertiliser_sales',
        'fertilizers sales data':'fertiliser_sales',
         'sales regarding fertlisers':'fertiliser_sales',
         'rbi_deposit':'rbi_deposit',
         'deposits of rbi':'rbi_deposit',
         'rbi-deposit':'rbi_deposit',
         'rbi deposit': 'rbi_deposit',
         'deposits by rbi':'rbi_deposit',
         'investments of rbi':'rbi_deposit',
         'investments by rbi':'rbi_deposit',
         'mnrega employment':'nrga_emp',
         'credit by bank':'rbi_credit',
         'Soil':'soil'
         ,'soil':'soil',
         'pmfby':'pmfby',
         'PM Kisan':'pm_kisan',
         'Pradhan Mantri Krishi Sinchai Yojana (PMKSY)':'pmksy',
         'pradhan mantri krishi sinchai yojana':'pmksy',
         'Agriculture Wages': 'rural_wages', 'Consumer Price Index and Inflation (CPI)': 'cpi', 
         'Credit by Bank': 'rbi_credit', 'Debt and Investment (NSSO)': 'debt_invest', 
         'Deposits with Bank': 'rbi_deposit', 'Employment (NSSO)': 'plfs', 
         'Household Consumption on Education (NSSO)': 'social_education', 
         'MGNREGA - Agriculture Investments': 'nrega', 'MGNREGA - Employment': 'nrga_emp', 
         'Unincorporated Non-Agriculture Enterprises Excluding Construction (NSSO)': 'non_agri', 'Financial Inclusion Survey (NABARD)': 'fis', 'Input survey (Non - Crop)': 'input_noncrop', 'NRLM - Self Help Groups (SHGs)': 'nrlm', 'Situation Assessment of Agricultural household (NSSO)': 'sas', 'Agricultural Census 2010-11 (Crop)': 'census', 'Agricultural Census 2010-11 (Non-Crop)': 'apy', 'Agricultural Census 2015-16 (Crop)': 'agcensus_c', 'Agricultural Census 2015-16 (Non-Crop)': 'agcensus_nc', 'Agricultural Marketing (Agmarknet)': 'coc', 'Area Production Statistics (NHB)': 'nhb', 'Area Production Yield (APY)': 'agcensus_crop', 'Cost of Cultivation (CoC)': 'agcensus_noncrop', 
         'Fertiliser Sales': 'fertiliser_sales',
          'Food and Fertiliser Subsidy': 'subsidy', 
          'Input Survey (Crop Composite)': 'input_composite',
           'Input Survey (Crop)': 'input_crop', 'National Food Security Mission (NFSM) Spending': 'nfsm', 
           'Procurement of Foodgrains': 'procurement', 'Public Distribution System (PDS)': 'pds', 'Soil Health Card - Funding status': 'shc_fund',
            'Soil Health Card - Nutrient Status': 'shc_nutrient', 'Stock of Foodgrains': 'stock', 'Depth to Water Level': 'depth', 'Groundwater - Stages of Extraction': 'depth', 
            'Rainfall': 'rainfall', 'Soil': 'soil', 'Temperature': 'temperature', 'Crop Insurance - Pradhan Mantri Fasal Bima Yojana (PMFBY)': 'pmfby', 'Minimum Support Price (MSP)': 'msp', 'PM Kisan': 'pm_kisan', 
            'Pradhan Mantri Krishi Sinchai Yojana (PMKSY)': 'pmksy', 'Mission Antodaya': 'antyodaya',
             'Socio-economic Caste Census (SECC)': 'secc', 'Census Household Amenities': 'census_household',
              'Census PCA Demography': 'agmarknet','CPI': 'cpi', 
    'apy': 'agcensus_crop', 
    'Temperature': 'temperature', 
    'Consumre Price Index and Inflation': 'cpi', 
    'SHC Financial Status': 'shc_fund', 
    'SHC - Nutrition Level': 'shc_nutrient', 
    'NSSO Employmenet': 'plfs', 
    'Stages of Groundwater': 'groundwater', 
    'MGNREGA dataset of Agriculture Investmnets': 'nrega', 
    'PMFBY': 'pmfby', 
    'Household Consumption on Eduaction': 'social_education', 
    'Houshold Consumption on Education': 'social_education', 
    'Soil Quality Card funding': 'shc_fund', 
    'Credit by Bank': 'rbi_credit', 
    'Household Consumption on Edu': 'social_education', 
    'groundwater - extraction stages': 'groundwater', 
    'PMKSY': 'pmksy', 
    'Employmetn data by MGNREGA': 'nrga_emp', 
    'Employment data by MNGREGA': 'nrga_emp', 
    'Household Consomption on Education': 'social_education', 
    'SHC - Nutrent Status': 'shc_nutrient', 
    'Nutrient Status': 'shc_nutrient', 
    'Nutrient Status of your SHC': 'shc_nutrient', 
    'PMK': 'pm_kisan', 
    'rainfall': 'rainfall', 
    'agriculture pay': 'rural_wages', 
    'PM Kisan': 'pm_kisan', 
    'Debt and Investment': 'debt_invest', 
    'groundwater extraction phases': 'groundwater', 
    'groundwater stages': 'groundwater', 
    'SHC - Funding Status': 'shc_fund', 
    'Soil Health Index - Nutrient Levels': 'shc_nutrient', 
    'MGNREGA Employment': 'nrga_emp', 
    'Deposits with Bank': 'rbi_deposit', 
    'Agriculture wages': 'rural_wages', 
    'Credit bie Bank': 'rbi_credit', 
    'Depth to Water Level': 'depth', 
    'Debet and Investment dataset': 'debt_invest', 
    'Agriculture Wages': 'rural_wages', 
    'groundwater': 'depth', 
    'deptto-water-level': 'depth', 
    'Household Consumption on Edu by NSSO': 'social_education', 
    'Depth to Groundwater': 'depth', 
    'groundwater Extraction stages': 'groundwater', 
    'Employmnet (NSSO)': 'plfs', 
    'soil': 'soil', 
    'Agri Investment by MGNREGA': 'nrega', 
    'Deposist with Bank': 'rbi_deposit', 
    'SHC - Fund Status': 'shc_fund', 
    'Debt and Investnent data by NSSO': 'debt_invest', 
    'agricultur wages': 'rural_wages', 
    'groundwater - Extraction cycles': 'groundwater', 
    'Soil Quality Card': 'shc_fund', 
    'agricultural pay': 'rural_wages',
    'funding status SHC': 'shc_fund', 
    'groundwater extraction stags': 'groundwater', 
    'Soils': 'soil', 
    'NSSO dataset of Employment': 'plfs', 
    'Soil Health Certificate - Nutrient content': 'shc_nutrient', 
    'Good Soil Index - Nutrient Composition': 'shc_nutrient', 
    'Kisan PM': 'pm_kisan', 
    'Deposits wit Bank': 'rbi_deposit', 
    'agriculture wages': 'rural_wages', 
    'detailed source names': 'plfs', 
    'NSSO dataset regarding Debt and Investment': 'debt_invest', 
    'Agriculture Investments by MGNREGA': 'nrega', 
    'Stock of Foodgrains': 'stock', 
    'SHC - Nutrient Status': 'shc_nutrient', 
    'food and fertilizer': 'subsidy', 
    'consumer price index': 'cpi', 
    'Agri Investments': 'nrega', 
    'Bank Deposits': 'rbi_deposit', 
    'Depth to Water Leve': 'depth', 
    'Employment (NSSO)': 'plfs', 
    'Soil Health Index Nutrient Levels': 'shc_nutrient', 
    'groundwater - cycles of extraction': 'groundwater', 
    'groundwater - Data extraction stages': 'groundwater', 
    'Bank Credit': 'rbi_credit', 
    'Agricultre wages': 'rural_wages', 
    'SHC - Nutrient': 'shc_nutrient', 
    'Credet by Bank': 'rbi_credit', 
    'SHC - Nutrient State': 'shc_nutrient', 
    'Debt and Investnent': 'debt_invest', 
    'Agriculture Investments': 'nrega', 
    'Consumer Price Index and Inflation': 'cpi', 
    'finance status': 'shc_fund', 
    'agri wages': 'rural_wages', 
    'Agri wages': 'rural_wages', 
    'credit': 'rbi_credit', 
    'credts by bank': 'rbi_credit', 
    'credits': 'rbi_credit', 
    'credit by bank': 'rbi_credit', 
    'Debtt and Investment': 'debt_invest', 
    'bank deposit': 'rbi_deposit', 
    'bank deposits': 'rbi_deposit', 
    'deposits by bank': 'rbi_deposit', 
    'bank deposts': 'rbi_deposit', 
    'Employment by NSSSO': 'social_education', 
    'MNREGA - Employment': 'nrega_emp', 
    'NABARD': 'fis', 
    'NABRD': 'fis', 
    'NRLM': 'nrlm', 
    'NRIM': 'nrlm', 
    'NrLM': 'nrlm', 
    'SAAH': 'sas', 
    'SaaH': 'sas', 
    'saah': 'sas', 
    'SAH': 'sas', 
    'Agmarket': 'coc', 
    'NHB': 'nhb', 
    'APY': 'agcensus_crop', 
    'CoC': 'agcensus_noncrop', 
    'Fertiliser Sales': 'fertiliser_sales', 
    'Fertiliser sales': 'fertiliser_sales', 
    'fertiliser sales': 'fertiliser_sales', 
    'NFSM': 'nfsm', 
    'name of the source': 'nfsm', 
    'source name': 'pds', 
    'origin': 'nfsm', 
    'root': 'pds', 
    'source': 'pds', 
    'sources': 'pds', 
    'Agriculture Salary': 'rural_wages', 
    'bank credit': 'rbi_credit', 
    'cradits by bank': 'rbi_credit', 
    'NSSO data for Employment': 'plfs', 
    'Employment by NSSO': 'plfs', 
    'Debt and Investment data by NSSO': 'debt_invest', 
    'NSSO Debt and Investment': 'debt_invest', 
    'NSSO Debet and Investment': 'debt_invest', 
    'NSSO data for Debt and Investmnet': 'debt_invest', 
    'Employment data by MNREGA': 'nrga_emp', 
    'MGNREGA Agriculture Investments': 'nrega', 
    'Household Consumption on Education': 'social_education', 
    'NSSO Household Consumption on Edu': 'social_education', 
    'CPI and inflation': 'cpi', 
    'Financial Inclusion Survey': 'fis', 
    'NABARD Financial Inclusion Survey': 'fis', 
    'NABARD Financial Inclusion finding': 'fis', 
    'Self Help Groups': 'nrlm', 
    'NRLM SHGs': 'nrlm', 
    'Area Production Yield': 'agcensus_crop', 
    'Cost of Farming': 'agcensus_noncrop', 
    'Cost of Horticulture': 'agcensus_noncrop', 
    'Cost of Cultivation': 'agcensus_noncrop', 
    'Manure Sales': 'fertiliser_sales', 
    'Organic ferti Sales': 'fertiliser_sales', 
    'Food and Fertiliser Subsidy': 'subsidy', 
    'Food and Compost Subsidies': 'subsidy', 
    'Crop and Fertiliser Subsidy': 'subsidy', 
    'Input Survey Crop': 'input_crop', 
    'crop Input Survey': 'input_crop', 
    'Procurement of Foodgrains': 'procurement', 
    'Procure of Foodgrains': 'procurement', 
    'foodgrains procurement': 'procurement', 
    'Foodgrains Procurement': 'procurement', 
    'Public Distribution System': 'pds', 
    'PDS': 'pds', 
    'National Food Security Mission Spending': 'nfsm', 
    'Pradhan Mantri Krishi Sinchai Yojana': 'pmksy', 
    'PM Krishi Sinchai Yojana': 'pmksy', 
    'Pradhan Mantri Krishi Sinchai Program': 'pmksy', 
    'PMSKY': 'pmksy', 
    'rural wages': 'rural_wages', 
    'rbi credits': 'rbi_credit', 
    'debt investment': 'debt_invest', 
    'rbi deposit': 'rbi_deposit', 
    'employment under national sample survey': 'rbi_deposit', 
    'household consumption on eduction': 'social_education', 
    'agri investment': 'nrega', 
    'Employment under the MGNREGA': 'nrga_emp', 
    'Non-Agri Enterprises': 'non_agri', 
    'non-crop Survey': 'input_noncrop', 
    'self health group': 'nrlm', 
    'agri households situations': 'sas', 
    '2010-11 Agricultural Survey for crops': 'census', 
    'Agriculture survey 2010-11 Non Crop': 'apy', 
    'agri survey of 2015-16 for crops': 'agcensus_c', 
    'agri survey of 2015-16 for non crops': 'agcensus_nc', 
    'AgMarket': 'coc', 
    'area production': 'nhb', 
    'Area Production Yeild': 'agcensus_crop', 
    'Cultivation Expenses': 'agcensus_noncrop', 
    'Sales of Fertiliser': 'fertiliser_sales', 
    'subsidy for food and ferti': 'subsidy', 
    'Survey of public opinion for hybrid crops': 'input_composite', 
    'input survey for crops': 'input_crop', 
    'National food security mission': 'nfsm', 
    'shc funds': 'shc_fund', 
    'nutrients under shc': 'shc_nutrient', 
    'depth of water level': 'depth', 
    'Rainfall': 'rainfall', 
    'Soil': 'soil', 
    'temperature': 'temperature', 
    'Crop insurance under pmfby': 'pmfby', 
    'minimum support price': 'msp', 
    'Antodaya mission': 'antyodaya', 
    'Socio-economic Caste Census': 'census_household', 
    'pca demography': 'agmarknet'}
         


template_names_variations =['granularity','source_name','methodology','frequency','last_updated_date'
                        'source_link','data_extraction_page']
def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(list(master_dic_dataset_name.keys()) + template_names_variations)

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    #Most probable spelling correction for word.

    # key : key function where the iterables are passed and comparsion is performed
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]

    # Deletes words one by one
    deletes    = [L + R[1:]               for L, R in splits if R]

    # transposes are done on first and second place
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))