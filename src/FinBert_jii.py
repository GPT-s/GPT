




 #!git clone https://gist.github.com/c1a8c0359fbde2f6dcb92065b8ffc5e3.git

#import pandas



#headlines_df = pandas.read_csv('c1a8c0359fbde2f6dcb92065b8ffc5e3/300_stock_headlines.csv')
#headlines_df.head(5)

#import numpy as np

#headlines_array = np.array(headlines_df)
#np.random.shuffle(headlines_array)
#headlines_list = list(headlines_array[:,2])


#print(headlines_list)

from crawler import top5_text
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import torch


# finbert 시작
# data =crawler사용
def bert(data):
    # 모델 설정
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
  
    inputs = tokenizer(data, padding = True, truncation = True, return_tensors='pt')
    print(inputs)
    
    outputs = model(**inputs)
    print(outputs.logits.shape)

    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)   
    print(predictions)

    positive = predictions[:, 0].tolist()
    negative = predictions[:, 1].tolist()
    neutral = predictions[:, 2].tolist()

    table = {'data':data,
             "Positive":positive,
             "Negative":negative, 
             "Neutral":neutral}
      
    df = pd.DataFrame(table, columns = ["data", "Positive", "Negative", "Neutral"])
    
    return df







