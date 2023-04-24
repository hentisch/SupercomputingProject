import gradio as gr
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub


model = tf.keras.models.load_model("/home/henry/genes_code/my_model_4")

def graph_text(text:str):
    val = model(tf.constant([text]))[0]
    plt.figure(figsize=(16, 9))
    plt.title("Model Prediction of Like/Retweet Ratio", fontsize=25)
    plt.ylabel("Probaility of Classification", fontsize=20)
    plt.xlabel("Percentile Range", fontsize=20)
    plt.xticks(range(10), [f'[{i*10}% - {(i+1)*10}%)' for i in range(9)] + ["[90% - 100%]"])
    
    print(val[:10])
    plt.bar(range(10), val[:10])
    return plt

gr.Interface(fn=graph_text, inputs="text", outputs="plot").launch()