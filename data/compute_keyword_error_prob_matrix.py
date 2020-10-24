#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


df = pd.read_csv('error_kws.csv')


# In[4]:


df


# In[14]:


key_words = {}


# In[21]:


df['Key_word'][0].split(', ')


# In[23]:


for index, row in df.iterrows():
    for w in row['Key_word'].split(', '):
        if w in key_words:
            key_words[w].add(row['Trouble'])
        else:
            key_words[w] = {row['Trouble']}
key_words


# In[49]:


p_mat = pd.DataFrame({e: [0]*len(key_words) for e in df['Trouble']}, dtype=float)


# In[50]:


p_mat.index = [w for w in key_words]


# In[51]:


p_mat['Noise for tool changing']['noise']


# In[52]:


len(key_words['noise'])


# In[53]:


for w in key_words:
    for e in key_words[w]:
        p_mat[e][w] = 1/len(key_words[w])


# In[54]:


p_mat['Noise for tool changing']


# In[55]:


p_mat


# In[56]:


import seaborn as sns


# In[58]:


hm = sns.heatmap(p_mat)


# In[59]:


df.to_csv('word_error_mat.csv')


# In[ ]:




