
import pandas as pd
from tqdm.auto import tqdm
import time
from fuzzywuzzy import fuzz

def catch_typo(to_correct, presented):
    # short entries are sent to further processing then 
    # Check Levenshtein distance against potential matches

    if len(to_correct) > 3:
        potential_matches = [b for b in presented if fuzz.partial_ratio(to_correct, b) >= 85]
        if len(potential_matches) > 0:
            return True
        # Check common typo patterns against potential matches (add your patterns)
        typo_patterns = {'l': 'i', 'i': 'l', 'p': 'b', 'b': 'p', 'o': 'a', 'a': 'o', 'e': 'i', 'i': 'e'}
        for char, typo in typo_patterns.items():
            if any(typo in to_correct and char in match for match in potential_matches):
                return True
    return False

def clean_text_ai(brands_presented, brands_to_clean, model):
    res_all = []
    for brand_to_correct in tqdm(brands_to_clean):

        prompt = f"""
            You are a professional Brand Name Spell Checker. 
            Given 2 variables:
                potential_responses = {brands_presented}
                brand_to_check = {brand_to_correct}
            Identify if brand_to_check is in the potential_responses, it can be misspelled, using: 
                - spelling similarity of at least 98%
                - edit distance <= 2
                - semantic similairy of 90%.
            Return "Not Found" if brand_to_check is not in the potential_responses or no close match exists.
                Examples of acceptable variations: "Addidas" -> "Adidas", "Nke" -> "Nike", "ume" -> "Puma",  "Bang"->"Bang & Olufsen"
                Examples of brand_to_check that must return "Not Found": "Can\'t remember", "don\'t know", "None"
                Further examples of Unacceptable variations: "I don't know" -> "Panasonic", "Sony" -> "Panasonic" , "Life"->"Bang & Olufsen"
                
             **Only return ONE option FROM the potential_responses OR "Not Found" as a response**
            """
        
        res = model.predict(prompt)

        #res = model.generate_content(prompt, stream=False) # used for Gemini-pro ai text generating model.
        try: 
            res_all.append({'given_response_label_presented':brand_to_correct, 'typed_brand':res.text})
        except:
            res_all.append({'given_response_label_presented':brand_to_correct, 'typed_brand':"Not Found"})

        time.sleep(0.3)
    
    df_cleaned = pd.DataFrame(res_all)
    df_cleaned.columns = ['original','corrected']
    #df_cleaned = df_cleaned.loc[df_cleaned.corrected.isin(brands_presented)].reset_index(drop=True)

    return df_cleaned

def add_correct_entries(df, brand_cleaned):
    brand_cleaned.columns = ['given_response_label_presented', 'corrected', 'method']
    merged_df = pd.merge(df, brand_cleaned, on='given_response_label_presented', how='left')
    merged_df['recalled_brand'] = merged_df['corrected'].fillna('Not Found')
    merged_df = merged_df.drop(['corrected'], axis=1)
    return merged_df

    
def calculate_corrected_brands(df, brands_presented):
    """
    Calculates the total number of the updated/ corrected brand names obtained from the free text recall
    Args:
        df (pandas df): data frame that contains typed_brand column
    Returns:
        grouped_df: aggregated dataframe per group with counts of corrected brand names.
    """
    count_df = df.loc[df.recalled_brand.isin(brands_presented)].reset_index(drop=True)

    count_df = count_df.drop_duplicates(['participant_id', 'recalled_brand', 'method'])
    corrected_counts = count_df.groupby(['group_id','method']).recalled_brand.value_counts()
    pd.set_option('display.max_rows', None)
    print('\n***** Corrected Entries: *****')
    print(corrected_counts)
    pd.reset_option('display.max_rows')     
    corrected_counts = corrected_counts.reset_index()

    return corrected_counts

def clean_free_recall (df, brands_presented, brands_to_clean, model):

    corrected_brands = {}
    for brand in brands_to_clean:
        if catch_typo(brand, brands_presented):
            closest_match = sorted(brands_presented, key=lambda b: fuzz.partial_ratio(brand, b), reverse=True)[0]
            corrected_brands[brand] = closest_match
        else:
            if fuzz.ratio(brand, brands_presented) <= 15:
                corrected_brands[brand] = "not_match"
            else:
                corrected_brands[brand] = "maybe"

    corrected_df = pd.DataFrame(list(corrected_brands.items()), columns=['original', 'corrected'])
    df_not_match = corrected_df[corrected_df.corrected=='not_match']
    df_maybe = corrected_df[corrected_df.corrected=='maybe'].original.unique().tolist()
    corrected_df = corrected_df[(corrected_df.corrected!='maybe') & (corrected_df.corrected!='not_match')].reset_index(drop=True)
    corrected_df['method'] = 'wuzzy'

    print(f'\nThere are {corrected_df.shape[0]} entries that indentified as match to targeted Brands.')
    print(f'\nThere are {df_not_match.shape[0]} entries that do not match targeted Brands.')

    if len(df_maybe)>0:
        print(f'\nThere are {len(df_maybe)} entries that have to be processed further:')
        clean_df_2 = clean_text_ai(brands_presented, df_maybe, model = model)
        clean_df_2['method'] = 'ai'
        corrected_df = pd.concat([clean_df_2, corrected_df], axis=0, ignore_index=True)
    corrected_df = corrected_df[corrected_df.corrected!='Not Found']
    corrected_df = corrected_df.drop_duplicates()

    df = add_correct_entries(df, corrected_df[['original','corrected', 'method']])
    corrected_counts =  calculate_corrected_brands(df, brands_presented)
    return df, corrected_counts, corrected_df


