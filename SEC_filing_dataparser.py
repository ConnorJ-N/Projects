import pandas as pd
import sqlite3

class DataParser():
    def __init__(self, data, tag, ddate, qtr, segment=None, company=None):
        
        if data is not None:
            self.conn = sqlite3.connect(":memory:")
            self.data = data.to_sql("my_table", self.conn, if_exists="replace", index=False)
        self.tag = tag
        self.segment = segment
        self.ddates = [ddate] if not isinstance(ddate, list) else ddate  
        self.qtr = qtr
        self.company = company
    
    def build_query(self, segment_avg=False, segment_add=False, segment_max=False):
        
        """Build dynamic query based on parameters"""
        base_query = "SELECT name, ddate, value"
        group_by = "GROUP BY name, ddate"
        where_conditions = ["tag = ?", "qtrs = ?"]
        params = [self.tag, self.qtr]

        # Handle ddate filter (if provided)
        placeholders = ",".join(["?"] * len(self.ddates))
        where_conditions.append(f"ddate IN ({placeholders})")
        params.extend(self.ddates)

        # Handle segment filter
        if self.segment == "null":
            where_conditions.append("segments IS NULL")
        else:
            where_conditions.append("segments = ?")
            params.append(self.segment)

        # Handle company filter (if provided)
        if self.company:
            where_conditions.append("name = ?")
            params.append(self.company)
        
        # Handle aggregation types: avg, sum, max
        if segment_avg:
            base_query = f"""
            SELECT name, ddate, value, AVG(value) AS average_value
            """
        elif segment_add:
            base_query = f"""
            SELECT name, ddate, value, SUM(value) AS total_value
            """
        elif segment_max:
            base_query = f"""
            SELECT name, ddate, value, MAX(value) AS max_value
            """
        
        # Combine everything into a single query
        where_clause = " AND ".join(where_conditions)
        print(where_clause, "where clause")
        final_query = f"{base_query} FROM my_table WHERE {where_clause} {group_by}"
        print(final_query, "Final clause")

        return final_query, params
    
    def filter_data(self, segment_avg=False, segment_add=False, segment_max=False):
        """Execute dynamically generated query"""
        query, params = self.build_query(segment_avg, segment_add, segment_max)
        
        # Execute the query and return results
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