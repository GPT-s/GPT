from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import torch


# finbert 시작
# data =crawler(top5_text) 사용
class FinBert:
    def __init__(self):
        
    # 모델 설정
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    

    def sentiment(self,data):
        
        inputs = self.tokenizer(data, padding = True, truncation = True, return_tensors='pt')
        #print(inputs)
        
        outputs = self.model(**inputs)
        #print(outputs.logits.shape)

        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)   
        #print(predictions)

        max_elements, max_idxs = torch.max(predictions, dim=1)

        values=[]
        for max in max_idxs:
            if max==0:
                values.append('Positive')
            elif max==1:
                values.append('Negative')
            elif max==2:
                values.append('Netural')

        table={'data':data,
               'value':values}

        sentiment_data = pd.DataFrame(table, columns = ["data", "value"])
        print("")
        print("핀 버트 완")
        print("핀 버트 완")
        print("핀 버트 완")
        print("핀 버트 완")
        print("핀 버트 완")

        return sentiment_data       


        # # ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        # # 테스트 점
        # print("핀 버트 완")
        # print("핀 버트 완")
        # print("핀 버트 완")
        # print("핀 버트 완")
        # print("핀 버트 완")
        # return data       