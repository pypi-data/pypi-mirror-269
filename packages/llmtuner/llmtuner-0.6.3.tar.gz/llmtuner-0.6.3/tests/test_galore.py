import matplotlib.pyplot as plt
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


model_id = "/home/incoming/LLM/qwen1_5/qwen1_5-0_5b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)

dataset = load_dataset("mlabonne/guanaco-llama2-1k", split="train[:200]").map(
    lambda x: tokenizer(x["text"], max_length=1024, truncation=True, add_special_tokens=False),
    batched=True,
)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="test_galore",
    learning_rate=1e-4,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=1,
    num_train_epochs=6.0,
    logging_steps=10,
    warmup_steps=10,
    optim="galore_adamw_layerwise",
    optim_args="scale=2.0,update_proj_gap=400",
    optim_target_modules="all-linear",
    gradient_checkpointing=True,
    report_to="none",
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)
trainer.train()

steps, losses = [], []
for i in range(len(trainer.state.log_history)):
    if "loss" in trainer.state.log_history[i]:
        steps.append(trainer.state.log_history[i]["step"])
        losses.append(trainer.state.log_history[i]["loss"])


plt.figure()
plt.plot(steps, losses)
plt.savefig("loss.png", format="png", dpi=100)
