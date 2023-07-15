# # 概要
# - streamlitを使ってwebアプリを作る
# - .pyにしてから作業を進める
# ## ライブラリ
import streamlit as st
import pandas as pd

import numpy as np

from time import sleep, time
from datetime import datetime, date

OUTPUT_PATH = "streamlit_出力表.csv"
columns=["No", "日付", "支払者", "商品", "金額", "支払済み"]

try:
    if type(st.session_state["df"]) == pd.DataFrame:
        pass      
except KeyError:
    print("初回使用")
    st.session_state["df"] = pd.DataFrame(columns=columns)

st.session_state["sample"] = "sample"


st.title("割り勘アプリ")



# ## 名前入力欄、比率作成
st.sidebar.header("基本設定")
st.sidebar.header("名前、割合入力")
st.sidebar.text("参加者と支払割合を記入してください")

user1 = st.sidebar.text_input("名前（1人目）", "A")
ratio1 = st.sidebar.slider("割合（1人目）", min_value=0.0, max_value=1.0, value=0.5)
user2 = st.sidebar.text_input("名前（2人目）", "B")
ratio2 = st.sidebar.slider("割合（2人目）", min_value=0.0, max_value=1.0, value=0.5)

if ratio1 + ratio2 != 1:
    st.sidebar.write(":red[合計割合は1.0にしてください]")

"名前：", user1, "、割合", ratio1
"名前：", user2, "、割合", ratio2

st.session_state['user'] = [[user1, ratio1], [user2, ratio2]]


# ## 金額入力機能


list_name = [user1, user2]


df = pd.DataFrame(columns=columns)

st.header("金額入力")
st.text("払った金額を記入してください")

date = st.text_input('日付', "0715")
name = st.selectbox("支払者", list_name)
goods = st.text_input("商品", "パンダ")
cost = st.text_input("金額", 2000)

if st.button('リストに追記'):
    
    df_add = pd.DataFrame([[date, name, goods, cost]], columns=["日付", "支払者", "商品", "金額"])
    
    # １回目の場合は、空のDFと結合
    if 'count' not in st.session_state:
        # 明細Noを付与
        st.session_state["no"] = 1
        df_add["No"] = 1

        # 支払い状況
        df_add["支払済み"] = "まだ"

        df = pd.concat([df, df_add], axis=0)
        st.session_state['df'] = df
        st.session_state['count'] = 1

        

        st.write('入力しました')
        
    # 2回目以降は、すでに作成済みのDFと結合
    else:
        # 明細Noを付与
        st.session_state["no"] = st.session_state["no"] + 1
        df_add["No"] = st.session_state["no"]

        # 支払い状況
        df_add["支払済み"] = "まだ"

        st.session_state['df'] = pd.concat([st.session_state['df'], df_add], axis=0)
        st.write('追記しました')
    
# 削除機能（支払済み機能）実装
st.header("支払済み入力")
st.text("すでに支払った項目を選んでください")

No_del = st.selectbox('No', list(st.session_state['df']["No"].unique()))

if st.button('支払済みに追記'):
    st.session_state['df']["支払済み"] = st.session_state['df']["支払済み"].mask(st.session_state['df']["No"] == No_del, "済")

st.dataframe(st.session_state['df'], 600, 300)

# ## 支払金額計算

st.header("購入金額")

df_calc = st.session_state['df'].loc[st.session_state['df']["支払済み"] == "まだ" ,:].copy()
df_calc["金額"] = df_calc["金額"].astype(int)

# 利用者ごとの合計
sum_user1 = df_calc.loc[df_calc["支払者"] == st.session_state['user'][0][0], "金額"].sum()
sum_user2 = df_calc.loc[df_calc["支払者"] == st.session_state['user'][1][0], "金額"].sum()
sum_cost = df_calc["金額"].sum()
st.write(st.session_state['user'][0][0], ':', sum_user1, "円")
st.write(st.session_state['user'][1][0], ':', sum_user2, "円")


# 払うべき額の計算
pay_user1 = sum_cost * st.session_state['user'][0][1]
pay_user2 = sum_cost * st.session_state['user'][1][1]
pay_num = (pay_user1 - sum_user1).round(1)

st.header("調整")

# 払った金額が少ない人が多い人に払う
if pay_num > 0:
    st.write(st.session_state['user'][0][0], "が", st.session_state['user'][1][0], "に", pay_num, "円払う")
elif pay_num < 0:
    st.write(st.session_state['user'][1][0], "が", st.session_state['user'][0][0], "に", pay_num * -1, "円払う")
else:
    st.write("どちらも払う必要なし")


# ## セッション情報を削除

st.header("初期化")


if st.button('金額情報削除'):
    st.session_state['count'] = None
    st.session_state['df'] = pd.DataFrame(columns=columns)
    st.write('金額情報を削除しました')

if st.button('ユーザー情報削除'):
    st.session_state['user'] = None
    st.write('ユーザー情報を削除しました')


# ## CSV出力

# パスワードつける
password = st.text_input("Pass", type="password")
if password == "mikiT":
    if st.button('CSV出力する'):
        df_calc.to_csv(OUTPUT_PATH, encoding="cp932")


