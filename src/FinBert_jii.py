




# 코랩을 시작할 때 아래코드를 한 번 돌려줍니다.
!pip install selenium
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin




!git clone https://gist.github.com/c1a8c0359fbde2f6dcb92065b8ffc5e3.git






"""# 새 섹션"""











import pandas


headlines_df = pandas.read_csv('c1a8c0359fbde2f6dcb92065b8ffc5e3/300_stock_headlines.csv')
headlines_df.head(5)

import numpy as np


headlines_array = np.array(headlines_df)
np.random.shuffle(headlines_array)
headlines_list = list(headlines_array[:,2])


print(headlines_list)



from transformers import AutoTokenizer, AutoModelForSequenceClassification
  
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

inputs = tokenizer(headlines_list, padding = True, truncation = True, return_tensors='pt')
print(inputs)

outputs = model(**inputs)
print(outputs.logits.shape)

import torch


predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
print(predictions)

import pandas as pd


positive = predictions[:, 0].tolist()
negative = predictions[:, 1].tolist()
neutral = predictions[:, 2].tolist()


table = {'Headline':headlines_list,
         "Positive":positive,
         "Negative":negative, 
         "Neutral":neutral}
      
df = pd.DataFrame(table, columns = ["Headline", "Positive", "Negative", "Neutral"])


df.head(5)

!pip install wandb
import wandb

wandb.init(project="FinBERT_Sentiment_Analysis_Project")

wandb.run.log({"Financial Sentiment Analysis Table" : wandb.Table(dataframe=df)})
wandb.run.finish()

cd /content/drive/MyDrive/Colab Notebooks/Git

!git clone https://[jyj0993@naver.com]:[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]@github.com/[jyj0993@naver.com]/[GPT].git









