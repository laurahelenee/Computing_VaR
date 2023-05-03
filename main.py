import os
import historic_var as hv
import conditional_var as cv

path_to_write = ''
os.chdir(path_to_write)

if not os.path.exists('output_hvar'):
    os.makedirs('output_hvar')
if not os.path.exists('output_c_hvar'):
    os.makedirs('output_c_hvar')

sheet_name = ''
file = ''

def main():
    prices = hv.read_dataframe(file, sheet_name=sheet_name)
    hVaR_df = hv.hVaR_data(prices)
    cVaR_df = cv.cVaR_data(prices)
    hVaR_df.to_excel('output_hvar/hvar.xlsx', sheet_name='Historical VaR')
    cVaR_df.to_excel('output_cvar/cvar.xlsx', sheet_name='Conditional Historical VaR')

main()
