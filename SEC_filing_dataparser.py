import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DataParser():
    """sub == submission data set"""
    """num == number data set"""
    def __init__(self, sub, num, tag, ddate, qtr, segment=None, company=None):
        self.sub = sub
        self.num = num
        self.tag = tag
        self.segment = segment
        self.ddate = ddate
        self.qtr = qtr
        self.company = company
        self.data = pd.merge(sub, num, on="adsh", how="inner")
        
    def filter_tag(self, data, tag:str):
        filtered_data = data[data['tag'] == tag]
        return filtered_data
    
    def filter_segment(self, data, segment:str):
        filtered_data = data[data['segments'] == segment]
        return filtered_data
    
    def filter_date(self, data, ddate:int):
        filtered_data = data[data['ddate'] == ddate]
        return filtered_data
    
    def filter_qtr(self, data, qtr:int):
        filtered_data = data[data['qtrs'] == qtr]
        return filtered_data
    
    def filter_company(self, data, company:str):
        filtered_data = data[data['company'] == company]
        return filtered_data
    
    def mean_across_segments(self, data):
        filtered_data = data.groupby("name", as_index=False)["value"].mean()
        return filtered_data
    
    def dataset_generation(self):
        if self.company is not None:
            self.data = self.filter_company(self.data, self.company)
            
        self.filtered_data = self.filter_tag(self.data, self.tag)
        self.filtered_data = self.filter_date(self.filtered_data, self.ddate)
        self.filtered_data = self.filter_qtr(self.filtered_data, self.qtr)
        
        if self.segment is not None:
            filtered_data = self.filter_segment(self.filtered_data, self.segment)
        else:
            filtered_data = self.mean_across_segments(self.filtered_data)
        return filtered_data
    