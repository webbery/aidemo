import torch
import torch.nn as nn
import torch.optim as optim
from transformers import BertTokenizer, BertModel, AdamW, WarmupLinearSchedule, BertPreTrainedModel

features_size = 20

class BertClassifier(BertPreTrainedModel):
    
    def __init__(self, config):
        super(BertClassifier, self).__init__(config)
        self.bert = BertModel(config)
        self.classifier = nn.Linear(config.hidden_size, features_size*4)
        
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, position_ids=None, head_mask=None,
                
            labels=None):
        outputs = self.bert(input_ids,
                               attention_mask=attention_mask,
                               token_type_ids=token_type_ids,
                               position_ids=position_ids,
                               head_mask=head_mask)
        cls_output = outputs[1] # batch, hidden
        cls_output = self.classifier(cls_output)
        cls_output = torch.sigmoid(cls_output)
        criterion = nn.BCELoss()
        loss = 0
        if labels is not None:
            loss = criterion(cls_output.flatten(), labels)
        return loss, cls_output

device = torch.device('cpu')
model_path = './model'
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertClassifier.from_pretrained(model_path).to(device)
model.eval()