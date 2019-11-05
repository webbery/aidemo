import torch
from BertClassifier import model,tokenizer,features_size
import numpy as np

def classify_comment(comment):
    tokens = tokenizer.tokenize(comment)
    if len(tokens)>500:
        tokens = tokens[0:500]
    text = tokenizer.encode(comment, add_special_tokens=True)
    text = torch.LongTensor(text)
    mask = (text != 0).float()
    pred = []
    with torch.no_grad():
        loss, outputs = model(text, attention_mask=mask)
        pred = outputs.cpu().numpy().tolist()
    pred = np.argmax(np.array(pred).reshape((-1,features_size,4)),axis=2)
    return pred[0,:]