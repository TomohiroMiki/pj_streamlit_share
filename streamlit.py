#!/usr/bin/env python
# coding: utf-8

# # 概要

# - streamlitを使ってwebアプリを作る
# - .pyにしてから作業を進める

# ## ライブラリ

# In[45]:


import streamlit as st
import pandas as pd
import numpy as np


# In[57]:


from time import sleep, time
from datetime import datetime, date


# ## 定数定義

# In[ ]:


OUTPUT_PATH = "streamlit_出力表.csv"


# # 本処理

# ## タイトル作成

# In[2]:


st.title("割り勘アプリ")
st.text("streamlitを使っています")


# ## 名前入力欄、比率作成

# In[ ]:


st.header("名前、割合入力")


# In[35]:


user1 = st.text_input("名前（1人目）")
ratio1 = st.slider("割合（1人目）", min_value=0.0, max_value=1.0, value=0.5)
user2 = st.text_input("名前（2人目）")
ratio2 = st.slider("割合（2人目）", min_value=0.0, max_value=1.0, value=0.5)

if ratio1 + ratio2 != 1:
    st.write(":red[合計割合は1.0にしてください]")

"名前：", user1, "、割合", ratio1
"名前：", user2, "、割合", ratio2

st.session_state['user'] = [[user1, ratio1], [user2, ratio2]]


# ## 金額入力機能

# In[32]:


columns=["日付", "支払者", "商品", "金額"]
list_name = [user1, user2]


# In[33]:


df = pd.DataFrame(columns=columns)


# In[ ]:


st.header("金額入力")


# In[ ]:


date = st.text_input('日付')
name = st.selectbox("支払者", list_name)
goods = st.text_input("商品")
cost = st.text_input("金額")


# In[ ]:


if st.button('リストに追記'):
    
    df_add = pd.DataFrame([[date, name, goods, cost]], columns=columns)
    
    # １回目の場合は、空のDFと結合
    if 'count' not in st.session_state:
        df = pd.concat([df, df_add], axis=0)
        st.session_state['df'] = df
        st.session_state['count'] = 1
        st.write('入力しました')
        
    # 2回目以降は、すでに作成済みのDFと結合
    else:
        st.session_state['df'] = pd.concat([st.session_state['df'], df_add], axis=0)
        st.write('追記しました')
    
    st.dataframe(st.session_state['df'], 600, 300)


# In[ ]:





# ## 支払金額計算

# In[ ]:


st.header("購入金額")


# In[ ]:


df_calc = st.session_state['df']
df_calc["金額"] = df_calc["金額"].astype(int)

# 利用者ごとの合計
sum_user1 = df_calc.loc[df_calc["支払者"] == st.session_state['user'][0][0], "金額"].sum()
sum_user2 = df_calc.loc[df_calc["支払者"] == st.session_state['user'][1][0], "金額"].sum()
sum_cost = df_calc["金額"].sum()
st.write(st.session_state['user'][0][0], ':', sum_user1, "円")
st.write(st.session_state['user'][1][0], ':', sum_user2, "円")


# In[ ]:


# 払うべき額の計算
pay_user1 = sum_cost * st.session_state['user'][0][1]
pay_user2 = sum_cost * st.session_state['user'][1][1]
pay_num = (pay_user1 - sum_user1).round(1)


# In[ ]:


st.header("調整")


# In[ ]:


# 払った金額が少ない人が多い人に払う
if pay_num > 0:
    st.write(st.session_state['user'][0][0], "が", st.session_state['user'][1][0], "に", pay_num, "円払う")
elif pay_num < 0:
    st.write(st.session_state['user'][1][0], "が", st.session_state['user'][0][0], "に", pay_num * -1, "円払う")
else:
    st.write("どちらも払う必要なし")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## セッション情報を削除

# In[ ]:


st.header("初期化")


# In[ ]:


if st.button('金額情報削除'):
    st.session_state['count'] = None
    st.session_state['df'] = None
    st.write('金額情報を削除しました')

if st.button('ユーザー情報削除'):
    st.session_state['user'] = None
    st.write('ユーザー情報を削除しました')


# ## CSV出力

# In[ ]:


# パスワードつける
password = st.text_input("Pass")
if password == "mikiT":
    if st.button('CSV出力する'):
        df_calc.to_csv(OUTPUT_PATH, encoding="cp932")
    

