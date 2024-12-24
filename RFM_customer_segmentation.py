import datetime as dt
import pandas as pd


pd.set_option ('display.max_columns', None)
pd.set_option ('display.max_rows', None)
pd.set_option ('display.float_format', lambda x: '%.2f' % x)
pd.set_option ('display.width', 1000)

df_ = pd.read_csv(r'C:\Users\seda\OneDrive\Masaüstü\RFM\flo_data_20k.csv')
df = df_.copy()
df.head(10)
df['order_channel'].value_counts()
df['last_order_channel'].value_counts()
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.dtypes
df.info()

df['customer_value_total'] = df['customer_value_total_ever_offline'] + df['customer_value_total_ever_online']
df['order_num_total'] = df['order_num_total_ever_offline'] + df['order_num_total_ever_online']
# First way
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()
# Second way
df['first_order_date'] = pd.to_datetime(df['first_order_date'])
df['last_order_date'] = pd.to_datetime(df['last_order_date'])
df['last_order_date_online'] = pd.to_datetime(df['last_order_date_online'])
df['last_order_date_offline'] = pd.to_datetime(df['last_order_date_offline'])

df.groupby(by='order_channel').agg({ 'master_id': 'count',
                                    'order_num_total': ['sum', 'mean'],
                                    'customer_value_total': ['sum', 'mean']})

df.sort_values(by='customer_value_total', ascending=False).head(10)
df.sort_values(by='order_num_total', ascending=False).head(10)

def data_pre(dataframe):
    dataframe['customer_value_total'] = dataframe['customer_value_total_ever_offline'] + dataframe['customer_value_total_ever_online']
    dataframe['order_num_total'] = dataframe['order_num_total_ever_offline'] + dataframe['order_num_total_ever_online']

    # dataframe['first_order_date'] = pd.to_datetime(dataframe['first_order_date'])
    # dataframe['last_order_date'] = pd.to_datetime(dataframe['last_order_date'])
    # dataframe['last_order_date_online'] = pd.to_datetime(dataframe['last_order_date_online'])
    # dataframe['last_order_date_offline'] = pd.to_datetime(dataframe['last_order_date_offline'])
    date_columns = df.columns[df.columns.str.contains("date")]
    df[date_columns] = df[date_columns].apply(pd.to_datetime)

    return dataframe

data_pre(df)

# Calculating RFM Metrics

df['last_order_date'].max()
today_date = dt.datetime(2021, 6, 1)

# First Way
rfm = df.groupby("master_id").agg({"last_order_date": lambda date: (today_date - date.max()).days,
                                         "order_num_total": lambda num: num.sum(),
                                         "customer_value_total": lambda TotalPrice: TotalPrice.sum()})
# Second Way
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]


rfm.sort_values(by='customer_value_total',ascending=False).head(10)
rfm.sort_values(by='order_num_total',ascending=False).head(10)
rfm.head(10)
rfm.columns = ["recency", "frequency", "monetary"]
rfm = rfm[rfm["monetary"] > 0]

# Calculating RF Score
rfm['rec_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['freq_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['mon_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['RF_SCORE'] = (rfm["rec_score"].astype(str) +
                        rfm["freq_score"].astype(str))

seg_map = {
    r"[1-2][1-2]": "hibernating",
    r"[1-2][3-4]": "at_Risk",
    r"[1-2]5": "cant_loose",
    r"3[1-2]": "about_to_sleep",
    r"33": "need_attention",
    r"[3-4][4-5]": "loyal_customers",
    r"41": "promising",
    r"51": "new_customers",
    r"[4-5][2-3]": "potential_loyalists",
    r"5[4-5]": "champions"
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)
rfm.groupby('segment').agg({'recency': ['mean', 'count'],
                            'frequency':['mean', 'count'],
                            'monetary': ['mean', 'count'] })

#First Way
target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
#Second Way
n_df = df.merge(rfm, on="master_id", how="right")
n_df = n_df[n_df["interested_in_categories_12"].str.contains("KADIN", na=False)]
df_n = n_df[n_df["segment"].isin(["champions","loyal_customers"])]
cust_ids = df_n['master_id']
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
n_df = df.merge(rfm, on="master_id", how="right")

#First Way
df_x = n_df[n_df["interested_in_categories_12"].str.contains("ERKEK", na=False)]
df_n = n_df[n_df["interested_in_categories_12"].str.contains("COCUK", na=False)]
df_c = df_n[df_n["segment"].isin(["cant_loose", "atrisk", "hibernating", "new_customers"])]
df_d = df_x[df_x["segment"].isin(["cant_loose", "atrisk", "hibernating", "new_customers"])]
cust_ids = df_c.merge(df_d, on="master_id", how="outer")
cust_ids = cust_ids['master_id']
cust_ids.to_csv("%40_indirim_müşteri_id.csv", index=False)

# Second Way
target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["master_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

def create_rfm(dataframe):

    today_date = dt.datetime(2021, 6, 1)
    rfm = pd.DataFrame()
    rfm = dataframe.groupby("master_id").agg({"last_order_date": lambda date: (today_date - date.max()).days,
                                       "order_num_total": lambda num: num.sum(),
                                       "customer_value_total": lambda TotalPrice: TotalPrice.sum()})
    rfm.columns = ["recency", "frequency", "monetary"]
    rfm['rec_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['freq_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['mon_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    rfm['RF_SCORE'] = (rfm["rec_score"].astype(str) +
                       rfm["freq_score"].astype(str))

    seg_map = {
        r"[1-2][1-2]": "hibernating",
        r"[1-2][3-4]": "at_Risk",
        r"[1-2]5": "cant_loose",
        r"3[1-2]": "about_to_sleep",
        r"33": "need_attention",
        r"[3-4][4-5]": "loyal_customers",
        r"41": "promising",
        r"51": "new_customers",
        r"[4-5][2-3]": "potential_loyalists",
        r"5[4-5]": "champions"
    }

    rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

    return rfm.head(10)

create_rfm(df)

