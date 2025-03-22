import pandas as pd
import sqlite3

class DataParser():
    def __init__(self, data, tag, ddate, qtr, segment=None, company=None):
        
        self.conn = sqlite3.connect(":memory:")
        self.data = data.to_sql("my_table", self.conn, if_exists="replace", index=False)
        self.tag = tag
        self.segment = segment
        self.ddates = [ddate] if not isinstance(ddate, list) else ddate  
        self.qtr = qtr
        self.company = company
    
    def filter_data(self, segment_avg=False, segment_add=False):
        """Apply SQL filtering based on provided parameters"""
        query = "SELECT name, segments, value FROM my_table WHERE tag = ? AND qtrs = ?"
        params = [self.tag, self.qtr]
        
        placeholders = ",".join(["?"] * len(self.ddates))  
        query += f" AND ddate IN ({placeholders})"
        params.extend(self.ddates)

        if self.segment:
            query += " AND segments = ?"
            params.append(self.segment)
            
        if segment_avg:
            query = f"""
            SELECT name, AVG(value) AS average_value
            FROM my_table
            WHERE tag = ? AND qtrs = ? AND ddate IN ({placeholders})
            GROUP BY name
            """
            params = [self.tag, self.qtr] + self.ddates
        
        if segment_add:
           query = f"""
           SELECT name, SUM(value) AS total_value
           FROM my_table
           WHERE tag = ? AND qtrs = ? AND ddate IN ({placeholders})
           GROUP BY name
           """
           params = [self.tag, self.qtr] + self.ddates

        if self.company:
            query += " AND name = ?"
            params.append(self.company)

        return pd.read_sql(query, self.conn, params=params)

    def close(self):
        """Close database connection"""
        self.conn.close()
    
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
    
    def name_history_mapping(self, sub1, sub2):
        
        """sub1 contains mappings between former and current company names
           sub2 contains the former company names to be mapped"""
           
        name_mapping = dict(zip(sub1["former"], sub1["name"]))
        sub2["name"] = sub2["name"].replace(name_mapping)
        return sub2
    
    def merge_sub_num(self, sub, num, company_map=False, sub2=None):
        
        """sub == submission data set
            num == number data set"""
        
        if company_map is False:
            merged_sub_num = pd.merge(sub, num, on="adsh", how="inner")
        else:
            try:
                mapped_sub = self.name_history_mapping(sub2, sub)
                merged_sub_num = pd.merge(mapped_sub, num, on="adsh", how="inner")
            except Exception as e:
                raise Exception(f"An error occured: {str(e)}. sub2 must be defined")
        return merged_sub_num