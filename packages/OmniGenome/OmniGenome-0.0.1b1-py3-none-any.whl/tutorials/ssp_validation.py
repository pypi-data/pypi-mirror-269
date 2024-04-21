# -*- coding: utf-8 -*-
# file: ssp_validation.py
# time: 16:43 04/04/2024
# author: YANG, HENG <hy345@exeter.ac.uk> (杨恒)
# github: https://github.com/yangheng95
# huggingface: https://huggingface.co/yangheng
# google scholar: https://scholar.google.com/citations?user=NPq5a_0AAAAJ&hl=en
# Copyright (C) 2019-2023. All Rights Reserved.
import tqdm
from transformers import AutoConfig, AutoModelForMaskedLM, AutoTokenizer
import torch
import RNA


def ss_validity_loss(rna_strct):
    dotCount = 0
    leftCount = 0
    rightCount = 0
    unmatched_positions = []  # 用于记录未匹配括号的位置
    uncoherentCount = 0
    prev_char = ""
    for i, char in enumerate(rna_strct):
        if prev_char != char:
            uncoherentCount += 1
        prev_char = char

        if char == "(":
            leftCount += 1
            unmatched_positions.append(i)  # 记录左括号位置
        elif char == ")":
            if leftCount > 0:
                leftCount -= 1
                unmatched_positions.pop()  # 移除最近的左括号位置
            else:
                rightCount += 1
                unmatched_positions.append(i)  # 记录右括号位置
        elif char == ".":
            dotCount += 1
        else:
            raise ValueError(f"Invalid character {char} in RNA structure")
    match_loss = (leftCount + rightCount) / (len(seq) - dotCount + 1e-5)
    return match_loss


def seq_to_logits(rna_seq, rna_strct=None, mlm_model=None, tokenizer=None):
    if rna_strct is None:
        input_ref = f"{rna_seq}"
    else:
        input_ref = f"{rna_seq}{tokenizer.eos_token}{rna_strct}"
    seq_ids = tokenizer(
        input_ref,
        return_tensors="pt",
        padding=True,
        truncation=True,
        add_special_tokens=True,
    )
    input_ids = seq_ids["input_ids"]
    attention_mask = seq_ids["attention_mask"]
    outputs = mlm_model(input_ids, attention_mask=attention_mask)
    mlm_positions = input_ids[0].eq(tokenizer.mask_token_id)
    return outputs.logits, mlm_positions


def fix_ss_mutation(rna_seq, rna_strct, mlm_model, tokenizer):
    logits, mlm_positions = seq_to_logits(rna_seq, rna_strct, mlm_model, tokenizer)
    pred_struct_ids = logits.argmax(-1)[0][mlm_positions]
    masked_base = tokenizer.decode(pred_struct_ids, skip_special_tokens=False).replace(
        " ", ""
    )
    pred_struct = rna_strct.replace("<mask>", masked_base).replace(" ", "")
    ss_loss = ss_validity_loss(pred_struct)
    return pred_struct, ss_loss


def find_invalid_ss_positions(rna_strct):
    left_brackets = []  # 存储左括号的位置
    right_brackets = []  # 存储未匹配的右括号的位置
    for i, char in enumerate(rna_strct):
        if char == "(":
            left_brackets.append(i)
        elif char == ")":
            if left_brackets:
                left_brackets.pop()  # 找到匹配的左括号，从列表中移除
            else:
                right_brackets.append(i)  # 没有匹配的左括号，记录右括号的位置
    return left_brackets + right_brackets


def run_rna_ss_repair(rna_seq, rna_strct, mlm_model, tokenizer):
    parents, offspring = [(rna_strct, ss_validity_loss(rna_strct))], []

    def min_ss_loss(parents):
        return min([ss_loss for _, ss_loss in parents])

    for _ in range(10):
        for _, (parent, ss_loss) in enumerate(tqdm.tqdm(parents)):
            for i in range(len(parent)):
                _parent = parent[:i] + "<mask>" + parent[i + 1 :]
                pred_struct, ss_loss = fix_ss_mutation(
                    rna_seq, _parent, mlm_model, tokenizer
                )
                if (
                    ss_loss <= min_ss_loss(parents)
                    and (pred_struct, ss_loss) not in parents
                ):
                    offspring.append((pred_struct, ss_loss))
                    break
            if parents == offspring or len(offspring) == 0:
                break
            parents = offspring
            offspring = []
    pred_structures = [parent for parent, ss_loss in parents if ss_loss == 0]
    pred_mfe_values = [RNA.fold(seq, pred_struct)[1] for pred_struct in pred_structures]
    pred_struct = [
        pred_struct
        for pred_struct, mfe in zip(pred_structures, pred_mfe_values)
        if mfe == min(pred_mfe_values)
    ]
    return pred_struct


# def run_rna_ss_repair(rna_seq, rna_strct, mlm_model, tokenizer):
#     parents, offspring = [(rna_strct, ss_validity_loss(rna_strct))], []
#     def min_ss_loss(parents):
#         return min([ss_loss for _, ss_loss in parents])
#     for _ in range(10):
#         for _, (parent, ss_loss) in enumerate(tqdm.tqdm(parents)):
#             for i in range(len(parent)):
#                 _parent = parent[:i] + '<mask>' + parent[i + 1:]
#                 pred_struct, ss_loss = fix_ss_mutation(rna_seq, _parent, mlm_model, tokenizer)
#                 if ss_loss <= min_ss_loss(parents) and (pred_struct, ss_loss) not in parents:
#                     offspring.append((pred_struct, ss_loss))
#             # for i in find_invalid_ss_positions(parent):
#             #     _parent = parent[:i] + '<mask>' + parent[i + 1:]
#             #     pred_struct, ss_loss = fix_ss_mutation(rna_seq, _parent, mlm_model, tokenizer)
#             #     if ss_loss <= min_ss_loss(parents) and (pred_struct, ss_loss) not in parents:
#             #         offspring.append((pred_struct, ss_loss))
#             if parents == offspring or len(offspring) == 0:
#                 break
#             parents = offspring
#             offspring = []
#     pred_structures = [parent for parent, ss_loss in parents if ss_loss == 0]
#     pred_mfe_values = [RNA.fold(seq, pred_struct)[1] for pred_struct in pred_structures]
#     pred_struct = [pred_struct for pred_struct, mfe in zip(pred_structures, pred_mfe_values) if mfe == min(pred_mfe_values)]
#     return pred_struct


if __name__ == "__main__":
    # RNA.params_load_RNA_Turner2004()
    RNA.params_load_RNA_Langdon2018()
    mlm_model = AutoModelForMaskedLM.from_pretrained(
        "pretrained_models/mprna_base_new", trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "pretrained_models/mprna_base_new", trust_remote_code=True
    )
    from sentence_transformers.util import pytorch_cos_sim

    with torch.no_grad():
        while True:
            # seq = input("Enter RNA sequence: ")
            # invalid_struct = input("Enter Predicted RNA structure: ")
            # if seq == 'exit':
            #     break
            seq = "GCUGGGAUGUUGGCUUAGAAGCAGCCAUCAUUUAAAGAGUGCGUAACAGCUCACCAGCGCUGGGAUGUUGGCUUAGAAGCAGCCAUCAUUUAAAGAGUGCGUAACAGCUCACCAGC"
            invalid_struct = "(((((((((((((((.......))))).))))....((((((......)))).))))))((((((((((((((.......))))).))))....(((((((.....)))).)))))"
            # ref_struct = '(((((((((..((((.......))))..)))........((((....)))).))))))(((((((((..((((.......))))..)))........((((....)))).))))))
            # seq = "GCGUCACACCGGUGAAGUCGCGCGUCACACCGGUGAAGUCGC"
            # invalid_struct = "(((((..(((((((..((((())))).))))))))..)))))"
            # ref_struct = "(((((.((((((((..((((())))).))))))))..)))))"
            # print(ref_struct)
            # RNA.svg_rna_plot(seq, ref_struct, f'ref_struct.svg')
            ref_struct = RNA.fold(seq)[0]
            ref_feature, _ = seq_to_logits(seq, ref_struct, mlm_model, tokenizer)
            max_cosine_sim = 0
            pred_structs = run_rna_ss_repair(seq, invalid_struct, mlm_model, tokenizer)
            for i, pred_struct in enumerate(pred_structs):
                pred_feature, _ = seq_to_logits(seq, pred_struct, mlm_model, tokenizer)
                cosine_sim = (
                    pytorch_cos_sim(ref_feature[0], pred_feature[0]).mean().item()
                )
                if cosine_sim > max_cosine_sim:
                    max_cosine_sim = cosine_sim
                    best_pred_struct = pred_struct
                    RNA.svg_rna_plot(seq, best_pred_struct, f"best_pred_struct.svg")
                print(pred_struct)
                RNA.svg_rna_plot(seq, pred_struct, f"pred_struct_{i}.svg")
            print("Best predicted RNA structure:", best_pred_struct)
