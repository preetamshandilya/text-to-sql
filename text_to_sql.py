#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from langchain import OpenAI, SQLDatabase
# from langchain_community.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
# # from langchain.chains import SQLDatabaseSequentialChain
# from langchain.sql_database import SQLDatabase
# from langchain_experimental.sql import SQLDatabaseChain

from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


# In[16]:


# Connect the database

username = "postgres" 
host = "localhost"
#password = "@%^*())_&^%"
port = "5432"
mydatabase = "dbadmin"

pg_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{mydatabase}"
db = SQLDatabase.from_uri(pg_uri)




# In[17]:


#Setup LLM

#OPENAI_API_KEY = ""

llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)


# In[18]:


def retrieve_from_db(query: str) -> str:
    db_context = db_chain(query)
    db_context = db_context['result'].strip()
    return db_context


# In[19]:


def generate(query: str) -> str:
    db_context = retrieve_from_db(query)
    
    system_message = """You are a professional representative of an employment agency.
        You have to answer user's queries and provide relevant information to help in their job search. 
        Example:
        
        Input:
        Where are the most number of jobs for an English Teacher in Canada?
        
        Context:
        The most number of jobs for an English Teacher in Canada is in the following cities:
        1. Ontario
        2. British Columbia
        
        Output:
        The most number of jobs for an English Teacher in Canada is in Toronto and British Columbia
        """
    
    human_qry_template = HumanMessagePromptTemplate.from_template(
        """Input:
        {human_input}
        
        Context:
        {db_context}
        
        Output:
        """
    )
    messages = [
      SystemMessage(content=system_message),
      human_qry_template.format(human_input=query, db_context=db_context)
    ]
    response = llm(messages).content
    return response


# In[39]:


generate("How many courses are available ?")


# In[40]:


generate("what is the name of courses available?")


# In[6]:


generate("How many students are in university?")


# In[20]:


generate("How many students are in university ? please explain your table selection approach. also explain the approch of selecting the table name")


# In[13]:


generate("How did you determine the table you selected in previous response?")


# In[ ]:




