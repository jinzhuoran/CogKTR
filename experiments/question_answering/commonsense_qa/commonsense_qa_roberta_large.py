import torch.nn as nn
import torch.optim as optim
from cogktr import init_cogktr, CommonsenseqaReader, CommonsenseqaProcessor
from cogktr import PlmAutoModel, BaseQuestionAnsweringModel, BaseClassificationMetric, Trainer

device, output_path = init_cogktr(
    device_id=8,
    output_path="/data/hongbang/CogKTR/datapath/question_answering/CommonsenseQA/experimental_result/",
    folder_tag="exp_commonsense_qa_roberta_large",
)

reader = CommonsenseqaReader(
    raw_data_path="/data/hongbang/CogKTR/datapath/question_answering/CommonsenseQA/raw_data")
train_data, dev_data, test_data = reader.read_all()
vocab = reader.read_vocab()

processor = CommonsenseqaProcessor(plm="roberta-large", max_token_len=128, vocab=vocab, mode="concatenate")
train_dataset = processor.process_train(train_data)
dev_dataset = processor.process_dev(dev_data)
test_dataset = processor.process_test(test_data)

plm = PlmAutoModel(pretrained_model_name="roberta-large")
model = BaseQuestionAnsweringModel(plm=plm, vocab=vocab)
metric = BaseClassificationMetric(mode="multi")
loss = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.000001)

trainer = Trainer(model,
                  train_dataset,
                  dev_data=dev_dataset,
                  n_epochs=20,
                  batch_size=10,
                  loss=loss,
                  optimizer=optimizer,
                  scheduler=None,
                  metrics=metric,
                  train_sampler=None,
                  dev_sampler=None,
                  drop_last=False,
                  gradient_accumulation_steps=1,
                  num_workers=5,
                  print_every=None,
                  scheduler_steps=None,
                  validate_steps=100,
                  save_steps=None,
                  output_path=output_path,
                  grad_norm=1,
                  use_tqdm=True,
                  device=device,
                  fp16=False,
                  fp16_opt_level='O1',
                  )
trainer.train()
print("end")
