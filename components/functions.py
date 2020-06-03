print("load function")
import pandas as pd
import numpy as np
import glob
import datetime as dt


price_history_path = "data/data_gia_test.csv"
ami_data_path = "data/price_for_faviz/*.csv"
finance_data_path = "data/data_export_test.csv"
thong_tin_co_ban_path = "data/thong_tin_co_ban.csv"

def list_vn30():
    vn30 = pd.read_csv("data/vn30.txt")
    return list(vn30.VN30)
list_vn30 = list_vn30()
def tai_chinh_tong_data():
    tai_chinh_tong_data = pd.read_csv(finance_data_path)
    tai_chinh_tong_data["San"] = tai_chinh_tong_data["San"].str.upper()
    print("import tai chinh data")
    return tai_chinh_tong_data
tai_chinh_tong_data = tai_chinh_tong_data()

def all_tickers():
    return tai_chinh_tong_data.Ticker.unique()
all_tickers = all_tickers()

def column_name():
    return tai_chinh_tong_data.columns
column_name = column_name()

def nganh_nghe_data():
    data_nganh = pd.read_csv(thong_tin_co_ban_path)
    data_nganh.rename(
        columns={"Sàn NY": "San", "Số CP niêm yết": "So_co_phieu"}, inplace=True
    )
    nganh_data = data_nganh.drop_duplicates(
        subset=["Ticker", "Level1", "Level2", "Level3", "Level4"]
    )
    data_nganh.set_index("Ticker", inplace=True)
    print("import data_nganh")
    return data_nganh


nganh_nghe_data = nganh_nghe_data()


def price_history():
    data_gia = pd.read_csv(price_history_path)
    data_gia["Ngay"] = pd.to_datetime(data_gia["Ngay"], format="%Y-%m-%d")
    data_gia["Index"] = data_gia["Ticker"] + data_gia["Ngay"].astype(str)
    data_gia['Mb_rong'] = data_gia['Gt_nn_mua'] - data_gia['Gt_nn_ban']
    data_gia.set_index("Index", inplace=True)
    print("import data_gia")
    # print(data_gia.head())
    return data_gia


price_history = price_history()


def price_realtime():
    filenames = glob.glob(ami_data_path)
    data_today = pd.DataFrame()
    for file in filenames:
        df_tempt = pd.read_csv(file)
        data_today = data_today.append(df_tempt)
    data_today = data_today.drop_duplicates(subset="Ticker", keep="last")
    data_today["Ngay"] = pd.to_datetime(data_today["Date"]).dt.strftime("%Y-%m-%d")
    data_today["Nam"] = pd.to_datetime(data_today["Date"]).dt.strftime("%Y").astype(int)
    data_today["Index"] = data_today["Ticker"] + data_today["Ngay"].astype(str)
    data_today.set_index("Index", inplace=True)
    data_today.drop(["Thanh_khoan", "Date"], axis=1, inplace=True)
    data_today["Gia"] = data_today["Gia"] * 1000
    # print(data_today.head())
    print("query today_data")
    return data_today


price_realtime = price_realtime()


def price_data():
    price_data = price_history.combine_first(price_realtime)
    price_data["Ten"] = price_data["Ticker"].map(nganh_nghe_data["shortname"])
    return price_data


price_data = price_data()


def heatmap_data():
    # price_data=price_data()
    heatmap_data = price_data.loc[price_data["Nam"] == 2020].copy()
    map_cols = ['San','Level1','Level2','Level3','Level4','So_co_phieu']
    for map_col in map_cols:
        heatmap_data[map_col] = heatmap_data["Ticker"].map(nganh_nghe_data[map_col])
   
    heatmap_data["Von_hoa"] = heatmap_data["Gia"] * heatmap_data["So_co_phieu"]
    heatmap_data.dropna(subset=["Level1", "San"], inplace=True)
    heatmap_data["Market"] = "Market"
    heatmap_data["Gia_tri"] = heatmap_data["Volume"] * heatmap_data["Gia"]
    date_take = (
        heatmap_data[heatmap_data.Ticker == "VNM"].iloc[-1]["Ngay"].strftime("%Y-%m-%d")
    )
    date_take
    clean_ticker = heatmap_data[
        (heatmap_data.Gia > 1000)
        & (heatmap_data.Volume > 100)
        & (heatmap_data.Ngay == date_take)
    ]["Ticker"].values
    heatmap_data = heatmap_data.loc[heatmap_data["Ticker"].isin(clean_ticker)]
    print("query heatmap")
    # heatmap_data.to_csv('a.csv')
    return heatmap_data

heatmap_data = heatmap_data()

def Busday():
    lastBusDay = dt.datetime.today()
    if dt.date.weekday(lastBusDay) == 5:  # if it's Saturday
        lastBusDay = lastBusDay - dt.timedelta(days=1)  # then make it Friday
    elif dt.date.weekday(lastBusDay) == 6:  # if it's Sunday
        lastBusDay = lastBusDay - dt.timedelta(days=2)
        # then make it Friday
    return lastBusDay


print("loaded function")
