import streamlit as st
import math
import pandas as pd
import numpy as np



def calculateUSTax(annual_salary):
    us_marginal_tax_interval = [(0,10275),(10275,41775),(41775,89075),(89075,170050),(170050,215950),(215950,539900),(539900,math.inf)]
    us_marginal_tax_dict = {0:0.1, 1:0.12, 2:0.22, 3:0.24, 4:0.32, 5:0.35, 6:0.37}

    for i in range(len(us_marginal_tax_interval)): 
        if us_marginal_tax_interval[i][0] <= annual_salary and annual_salary <= us_marginal_tax_interval[i][1]:
            taxed_annual_salary = annual_salary * (1 - us_marginal_tax_dict[i])
            return taxed_annual_salary


def calculateThaiTax(annual_salary):
    thai_marginal_tax_interval = [(0,150000),(150001,300000),(300001,500000),(500001,750000),(750001,1000000),(1000001,2000000),(2000001,5000000),(5000001, math.inf)]
    thai_marginal_tax_dict = {0:0, 1:0.05, 2:0.1, 3:0.15, 4:0.2, 5:0.25, 6:0.30, 7:0.35}

    for i in range(len(thai_marginal_tax_interval)): 
        if thai_marginal_tax_interval[i][0] <= annual_salary and annual_salary <= thai_marginal_tax_interval[i][1]:
            taxed_annual_salary = annual_salary * (1 - thai_marginal_tax_dict[i])
            return taxed_annual_salary 

def calculateMonthlySavings(taxed_monthly_salary, monthly_living_cost):
    montly_savings = taxed_monthly_salary - monthly_living_cost
    return montly_savings


def calculateCumulativeSavings(saving_list):
    cumulative_savings = 0
    cumulative_savings_list = []
    for monthly_savings in saving_list:
        cumulative_savings += monthly_savings
        cumulative_savings_list.append(cumulative_savings)
    
    return cumulative_savings_list

def usdConversion(income_usd):
    usd_to_thb = 32
    income_thb = income_usd * usd_to_thb
    return income_thb

us_tab, thai_tab, comparison_tab = st.tabs(["United States", "Thailand", "Comparison"])

with us_tab:
   st.markdown("#### United States Salary")
   us_annual_salary = st.number_input(label="Annual Salary (USD): ")
   st.markdown("")
   us_monthly_living_cost = st.number_input(label="Monthly Living Cost (USD): ")
   
   taxed_annual_salary = calculateUSTax(us_annual_salary)
   us_monthly_savings  = calculateMonthlySavings(taxed_annual_salary/12, us_monthly_living_cost)
   converted_us_monthly_savings = usdConversion(us_monthly_savings)
   us_monthly_savings_list = [converted_us_monthly_savings] * 12

   us_monthly_cumlative_savings = calculateCumulativeSavings(us_monthly_savings_list)
   

with thai_tab:
   st.markdown("#### Thailand Salary")
   thai_monthly_salary = st.number_input(label="Monthly Salary (THB): ")
   st.markdown("")
   thai_monthly_living_cost = st.number_input(label="Monthly Living Cost (THB): ")

   taxed_thai_monthly_salary = calculateThaiTax(thai_monthly_salary*12)
   thai_monthly_savings  = calculateMonthlySavings(taxed_thai_monthly_salary/12, thai_monthly_living_cost)
   thai_monthly_savings_list = [thai_monthly_savings] * 12

   thai_monthly_cumlative_savings = calculateCumulativeSavings(thai_monthly_savings_list)



with comparison_tab:
    st.markdown("#### Comparison")

    chart_data = pd.DataFrame({'United States':us_monthly_cumlative_savings, 'Thailand':thai_monthly_cumlative_savings})

    st.table(chart_data)

    st.line_chart(chart_data)





