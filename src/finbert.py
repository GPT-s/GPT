from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import torch


# finbert 시작
# data =crawler(top5_text) 사용
def bert(data):
    # 모델 설정
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
  
    inputs = tokenizer(data, padding = True, truncation = True, return_tensors='pt')
    #print(inputs)
    
    outputs = model(**inputs)
    #print(outputs.logits.shape)

    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)   
    #print(predictions)

    positive = predictions[:, 0].tolist()
    negative = predictions[:, 1].tolist()
    neutral = predictions[:, 2].tolist()

    table = {'data':data,
             "Positive":positive,
             "Negative":negative, 
             "Neutral":neutral}


    sentiment_data = pd.DataFrame(table, columns = ["data", "Positive", "Negative", "Neutral"])
    
    return sentiment_data







