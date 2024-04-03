from sentence_transformers import CrossEncoder
import json
import jsonlines
import gradio as gr
import argparse
import os
import sys
# Load the model, here we use our base sized model
model = None

parser = argparse.ArgumentParser(description='Semantic Search chatbot')
parser.add_argument('--knowledge-base','-k', type=str, help='Path to the knowledge base file in jsonl format', default='17megabot.jsonl')
parser.add_argument('--examples','-e', choices=['0','1','2','3'], help='Number of examples to show in the chat interface', default='3')
parser.add_argument('--wipe-cache','-w', action='store_true', help='Wipe the cache of the chat interface', default=False)
parser.add_argument('--share','-s', action='store_true', help='Enable the share button in the chat interface', default=False)
args = parser.parse_args()

if args.wipe_cache:
    if os.path.exists("gradio_cached_examples"):
        os.system("rm -r gradio_cached_examples")
        print("Cache wiped")
# load faq from jsonl file
questions = []
answers = []
with jsonlines.open(args.knowledge_base) as reader:
    for obj in reader:
        questions.append(obj['q'])
        answers.append(obj['a'])

examples  = [[q] for q in questions[:int(args.examples)]]

def get_related_question_index(query):
    related = model.rank(query, questions, top_k=3)
    i = -1
    if len(related) > 0 and related[0]["score"] > 0.9:
        i = related[0]["corpus_id"]
    return i

def llm(query, history):
    # encode the question
    global model
    if model is None:
        model = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-2")
    response = model.rank(query, answers, return_documents=True, top_k=3)
    if response[0]["score"] > 0.9:
        answer = response[0]["text"]
    else:
        position = get_related_question_index(query)
        if position > -1:
            answer = answers[position]
        else:
            answer = "Can you please rephrase your question?"
    return answer
gr.ChatInterface(llm, title="Semantic Search chatbot",
                 description="Micro llm (less than 8MB) based on TinyBERT for semantic search. It uses the MS Marco encoder for training.",
                 cache_examples=True,
                 examples=examples, delete_cache=[3600,3600]).launch(share=args.share)
