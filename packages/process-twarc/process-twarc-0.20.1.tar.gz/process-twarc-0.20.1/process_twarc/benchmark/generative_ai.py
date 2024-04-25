import json
import pandas as pd
from process_twarc.util import load_dict, load_dataset, make_dir, save_dict
import re
import os
import numpy as np
from sklearn.metrics import f1_score



def prompt_for_few_shot_classification(
    instructions: dict,
    datasets: dict,
    n_examples_per_class: int = 2,
    lang: str="en"
    ):
        if lang == "en":
            txt = {
                "Examples": "Examples",
                "text": "text",
                "label": "label",
                "end": "What is the sentiment of this tweet? (positive, negative, mixed, neutral)"
            }
        elif lang == "jp":
            txt = {
                "Examples": "例",
                "text": "テキスト",
                "label": "ラベル",
                "end": "このツイートの感情は？(ポジティブ、ネガティブ、ミックス、ニュートラル）"
            }
        
        if lang not in ["en", "jp"]:
            raise ValueError("Language must be either 'en' or 'jp'")
        
        def init_prompt():
            prompt = []
            for key, value in instructions.items():
                prompt.append(key + ":\n\n")
                if isinstance(value, dict):
                    for k, v in value.items():
                        prompt.append(k + ":\n")
                        prompt.append(json.dumps(v, ensure_ascii=False) + "\n")
                elif isinstance(value, list):
                    for item in value:
                        prompt.append(item + "\n")
                elif isinstance(value, str): 
                    prompt.append(value + "\n")
                prompt.append("\n")
            
            prompt = "".join(prompt)
            return prompt

        def get_examples(prompt, n=n_examples_per_class):


            train = datasets["train"].groupby("label").apply(lambda x: x.sample(n)).sample(frac=1).reset_index(drop=True)
            prompt += f"{txt['Examples']}:\n\n```"
            for _, row in train.iterrows():
                prompt += f"{txt['text']}:\n{row['text']}\n\n"
                prompt += f"{txt['label']}:\n{row['label']}\n\n"
            prompt += "```\n\n"
            return prompt
        
        def get_test_data(prompt):
            test = datasets["test"].sample(1).reset_index(drop=True)
            test_id = test["tweet_id"].values[0]

            prompt += f"{txt['text']}:\n{test['text'].values[0]}\n\n"
            prompt += f"{txt['end']}\n\n"
            

            return prompt, test_id

        prompt = init_prompt()
        prompt = get_examples(prompt)
        prompt, test_id = get_test_data(prompt)
        return prompt, test_id

def extract_label(response):
    # Compile regex pattern to match expected labels, allowing for non-alphanumeric characters surrounding the label
    pattern = re.compile(r'(positive|negative|mixed|neutral|ニュートラル|ポジティブ|ネガティブ|ミックス)', re.IGNORECASE)
    
    # Search for the first occurrence of any of the labels
    match = pattern.search(response)
    
    # Return the found label in a consistently formatted case or None if no label is found
    if match:
        return match.group(1).lower()  # Ensure consistent formatting
    else:
        return None

def format_response(response, test_id):
    label = extract_label(response)
    if not label:
        return pd.DataFrame()
    output = pd.DataFrame({
        "tweet_id": [test_id],
        "predicted_label": [label]
    })
    return output

def init_prompt_response_io(
        model_name: tuple,
        path_to_api_key: str
):
    
    if model_name[0] == "openai":
        import openai

        openai.api_key = load_dict(path_to_api_key)["api_key"]
        get_response = lambda prompt: openai.ChatCompletion.create(
            model=model_name[1],
            messages=[{"role": "system", "content": prompt}]
        ).choices[0].message["content"]
    
        return get_response
    
    elif model_name[0] == "google":
        import vertexai
        from vertexai.preview.generative_models import GenerativeModel
        api_key = load_dict(path_to_api_key)

        vertexai.init(project = api_key["project_id"], location = api_key["location"])

        def get_response(prompt: str):
            model = GenerativeModel(model_name[1])
            chat = model.start_chat(response_validation=False)
            response = chat.send_message(prompt).text
            return response
        return get_response

    elif model_name[0] in ["meta", "mistralai"]:
        print("Using Replicate API")

        import replicate

        os.environ["REPLICATE_API_TOKEN"] = load_dict(path_to_api_key)["api_key"]

        def get_response(prompt: str):
            input = {
                "prompt": prompt,
                "system_prompt": "Label the sentiment. Do not explain your reasoning.",
                "temperature": 0.0,
                "stop_sequences": "\n\n"}

            response = replicate.run(
                "/".join(model_name),
                input=input
            )

            response = "".join(response)
            return response
        return get_response
    
    elif model_name[0] == "HuggingFace":


        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

        tokenizer = AutoTokenizer.from_pretrained(model_name[1])
        model = AutoModelForCausalLM.from_pretrained(model_name[1], torch_dtype = "auto")

        if torch.cuda.is_available():
            model = model.to("cuda")
        
        def get_response(prompt: str, model=model):
            formatted_prompt = "{bos_token}{b_inst} {system}{prompt} {e_inst} ".format(
                bos_token=tokenizer.bos_token,
                b_inst=B_INST,
                system=f"{B_SYS}感情にラベルを付ける。理由を説明しないこと。{E_SYS}",
                prompt=prompt,
                e_inst=E_INST,
            )

            with torch.no_grad():
                token_ids = tokenizer.encode(formatted_prompt, add_special_tokens=False, return_tensors="pt")

                output_ids = model.generate(
                    token_ids.to(model.device),
                    temperature=0.0,
                    top_p=0.9,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id
                )
            response = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1) :], skip_special_tokens=True)
            return response
        return get_response

def get_evaluation_metrics(output, output_dir):
    metrics = {
        "accuracy": (output["label"] == output["predicted_label"]).mean(),
        "macro_f1": f1_score(output["label"], output["predicted_label"], average="macro"),
        "micro_f1": f1_score(output["label"], output["predicted_label"], average="micro"),
        "weighted_f1": f1_score(output["label"], output["predicted_label"], average="weighted")
    }
    for label in output["label"].unique():
        metrics[f"{label}_f1"] = f1_score(output["label"] == label, output["predicted_label"] == label)

    metrics = {k:v.round(3) for k, v in metrics.items()}
    for k, v in metrics.items():
        print(f"{k}: {v}")
    save_dict(metrics, os.path.join(output_dir, "metrics.json"))

def build_confusion_matrix(output, id2label, output_dir):
    # Initialize the confusion matrix
    cm = np.zeros((len(id2label), len(id2label)))

    # Convert dataset columns to numpy arrays
    true_labels = np.array([label.lower() for label in output["label"].tolist()])
    predicted_labels = np.array([label.lower() for label in output["predicted_label"].tolist()])

    # Create label to index mapping
    label2idx = {v:k for k, v in id2label.items()}
    sorted_labels = [k for k, v in sorted(label2idx.items(), key=lambda x: x[1])]

    # Fill the confusion matrix
    for t, p in zip(true_labels, predicted_labels):
        cm[label2idx[t], label2idx[p]] += 1

    print(cm)
    # Save the confusion matrix and labels
    np.savez_compressed(os.path.join(output_dir, "cm.npz"), cm=cm, labels=sorted_labels)

def benchmark_gai_pipeline(
    data_dir: str,
    column_dict: dict,
    lang: str,
    model_name: tuple,
    path_to_api_key: str,
    instructions: dict,
    output_dir: str,
):
    
    output_dir = os.path.join(output_dir, model_name[0], model_name[1])
    path_to_output = os.path.join(output_dir, "response.parquet")
    make_dir(output_dir)

    def get_id2label(lang=lang):
        if lang == "en":
            id2label = {
                0: "neutral",
                1: "positive",
                2: "negative",
                3: "mixed"
            }
        elif lang == "jp":
            id2label = {
                0: "ニュートラル",
                1: "ポジティブ",
                2: "ネガティブ",
                3: "ミックス"
            }
        return id2label
    
    id2label = get_id2label()

    def load_datasets(
        data_dir = data_dir,
        column_dict = column_dict,
        id2label = id2label,
        path_to_output = path_to_output
        ):
        def load_ (split):
            dataset = load_dataset(
                file_path = os.path.join(data_dir, f"{split}.parquet"),
                columns = list(column_dict.values())
            )
            dataset = dataset.rename(columns={column_dict["label"]: "label"})
            dataset["label"] = dataset["label"].map(id2label)
            return dataset
        
        datasets = {k:v for k, v in zip( ["train", "test"], map(load_, ["train", "test"]))}
        datasets["response"] = load_dataset(path_to_output) if os.path.exists(path_to_output) else pd.DataFrame()
        return datasets
    
    def get_next_batch():
        datasets = load_datasets()
        response = datasets["response"]
        test = datasets["test"]
        if not response.empty:
            test = datasets["test"][~datasets["test"]["tweet_id"].isin(response["tweet_id"])]
        datasets["test"] = test
        remainder = test.shape[0]
        if not remainder:
            print("All tweets have been classified")
            return None
        print(f"Remaining tweets: {remainder}")
        return datasets
    
    def evaluate_response():
        def merge_response():
            datasets = load_datasets()
            if not "label" in datasets["response"].columns:
                output = datasets["test"].merge(datasets["response"], on="tweet_id")
                output.to_parquet(path_to_output, index=False)
            else:
                output = datasets["response"]
            return output
        
        output = merge_response()
        get_evaluation_metrics(output, output_dir)
        build_confusion_matrix(output, id2label, output_dir)

    datasets = get_next_batch()
    get_response = init_prompt_response_io(model_name, path_to_api_key)
    while datasets is not None:
        prompt, test_id = prompt_for_few_shot_classification(instructions, datasets)
        response = get_response(prompt)
        print (response)
        output = format_response(response, test_id)
        print(f"{output=}")
        if output.empty:
            print("No response received")
            continue
        datasets["response"] = pd.concat([datasets["response"], output])
        # datasets["response"] = datasets["response"].dropna().reset_index(drop=True)
        datasets["response"].to_parquet(path_to_output, index=False)
        datasets = get_next_batch()
    evaluate_response()
    
