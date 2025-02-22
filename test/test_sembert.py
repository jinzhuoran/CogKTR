import torch
import torch.nn as nn
import torch.optim as optim
from cogktr import *
from cogktr.core.evaluator import Evaluator
from cogktr.utils.general_utils import init_cogktr
from cogktr.data.processor.qnli_processors.qnli_sembert_processor import QnliSembertProcessor
# from cogktr.models.old_sembert_model import BertForSequenceClassificationTag
from transformers import BertConfig
from argparse import Namespace
from cogktr.models.sembert_model import SembertForSequenceClassification
from cogktr.modules.encoder.sembert import SembertEncoder
# import wandb
# wandb.init(project="CogKTR",entity="hongbangyuan")


# device, output_path = init_cogktr(
#     device_id=9,
#     output_path="/data/hongbang/CogKTR/datapath/sentence_pair/QNLI/experimental_result/",
#     folder_tag="sembert_without_tag_use_for_demo",
# )
#
reader = QnliReader(raw_data_path="/data/hongbang/CogKTR/datapath/sentence_pair/QNLI/raw_data")
train_data, dev_data, test_data = reader.read_all()
vocab = reader.read_vocab()

# enhancer = Enhancer(reprocess=False,
#                     return_srl=True,
#                     save_file_name="pre_enhanced_data",
#                     datapath="/data/hongbang/CogKTR/datapath",
#                     enhanced_data_path="/data/hongbang/CogKTR/datapath/sentence_pair/QNLI/enhanced_data")
# enhanced_train_dict = enhancer.enhance_train(train_data,enhanced_key_1="sentence",enhanced_key_2="question")
# enhanced_dev_dict = enhancer.enhance_dev(dev_data,enhanced_key_1="sentence",enhanced_key_2="question")
# enhanced_test_dict = enhancer.enhance_test(test_data,enhanced_key_1="sentence",enhanced_key_2="question")
enhancer = LinguisticsEnhancer(load_ner=False,
                               load_srl=True,
                               load_syntax=False,
                               load_wordnet=False,
                               cache_path="/data/hongbang/CogKTR/datapath/sentence_pair/QNLI//enhanced_data",
                               cache_file="linguistics_data",
                               reprocess=True)

enhanced_train_dict = enhancer.enhance_train(train_data,enhanced_key_1="sentence",enhanced_key_2="question",return_srl=True)
enhanced_dev_dict = enhancer.enhance_dev(dev_data,enhanced_key_1="sentence",enhanced_key_2="question",return_srl=True)
enhanced_test_dict = enhancer.enhance_test(test_data,enhanced_key_1="sentence",enhanced_key_2="question",return_srl=True)

processor = QnliSembertProcessor(plm="bert-base-uncased", max_token_len=256, vocab=vocab,debug=False)
train_dataset = processor.process_train(train_data,enhanced_train_dict)
dev_dataset = processor.process_dev(dev_data,enhanced_dev_dict)
# test_dataset = processor.process_test(test_data,enhanced_test_dict)

early_stopping = EarlyStopping(mode="max",patience=3,threshold=0.001,threshold_mode="abs",metric_name="F1")

tag_config = {
   "tag_vocab_size":len(vocab["tag_vocab"]),
   "hidden_size":10,
   "output_dim":10,
   "dropout_prob":0.1,
   "num_aspect":3
}
# model = BertForSequenceClassificationTag.from_pretrained(
#     "bert-base-uncased",
#     cache_dir="/data/hongbang/.pytorch_pretrained_bert/distributed_-1",
#     num_labels=2,
#     tag_config=tag_config,
# )
# # plm = SembertEncoder.from_pretrained("bert-large-uncased",tag_config=tag_config)
plm = SembertEncoder.from_pretrained("bert-base-uncased",tag_config=None)
model = SembertForSequenceClassification(
    vocab=vocab,
    plm=plm,
)
# # model = SembertForSequenceClassification(
# #     vocab=vocab,
# #     plm="bert-large-uncased",
# #     tag_config=tag_config
# # )
#
# # model = BaseSentencePairClassificationModel(plm="bert-base-cased", vocab=vocab)
# metric = BaseClassificationMetric(mode="binary")
# loss = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=2e-5)
# # config = wandb.config
# # config.lr = 2e-5
#
# trainer = Trainer(model,
#                   train_dataset,
#                   dev_data=dev_dataset,
#                   n_epochs=20,
#                   batch_size=16,
#                   loss=loss,
#                   optimizer=optimizer,
#                   scheduler=None,
#                   metrics=metric,
#                   train_sampler=None,
#                   dev_sampler=None,
#                   drop_last=False,
#                   gradient_accumulation_steps=1,
#                   num_workers=5,
#                   print_every=None,
#                   scheduler_steps=None,
#                   # checkpoint_path="/data/hongbang/CogKTR/datapath/sentence_pair/QNLI/experimental_result/simple_test1--2022-05-30--13-02-12.95/model/checkpoint-300",
#                   validate_steps=2000,  # validation setting
#                   save_steps=None,  # when to save model result
#                   output_path=output_path,
#                   grad_norm=1,
#                   use_tqdm=True,
#                   device=device,
#                   callbacks=None,
#                   metric_key=None,
#                   fp16=False,
#                   fp16_opt_level='O1',
#                   )
# trainer.train()
# print("end")

# evaluator = Evaluator(
#     model=model,
#     checkpoint_path="/data/hongbang/CogKTR/datapath/sentence_pair/QNLI/experimental_result/simple_test1--2022-05-30--13-02-12.95/model/checkpoint-400",
#     dev_data=dev_dataset,
#     metrics=metric,
#     sampler=None,
#     drop_last=False,
#     collate_fn=None,
#     file_name="models.pt",
#     batch_size=32,
#     device=device,
#     user_tqdm=True,
# )
# evaluator.evaluate()
# print("End")
