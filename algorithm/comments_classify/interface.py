import torch
from algorithm.comments_classify.BertClassifier import model,tokenizer,features_size
import numpy as np

def classify_comment(comment):
    tokens = tokenizer.tokenize(comment)
    sentence = comment
    if len(tokens)>400:
        sentence = comment[0:400]
    text = [tokenizer.encode(sentence, add_special_tokens=True)]
    text = torch.LongTensor(text)
    mask = (text != 0).float()
    pred = []
    with torch.no_grad():
        outputs = model(text, attention_mask=mask)[1]
        pred = outputs.cpu().numpy().tolist()
    pred = np.argmax(np.array(pred).reshape((-1,features_size,4)),axis=2)
    return pred[0,:]

# result = classify_comment('''
# 地理位置好，交通方便，就在124车站对面交通方便，很好，我晚上7点多去买的了，已经没有什么面包了，想吃金元宝蛋糕也没有了，那个蛋糕很好卖的，好吃，整体还算不错吧17元抵20元的券，还不错
# ''')
# print(result)
