import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub

import matplotlib.pyplot as plt

model = tf.keras.models.load_model("/home/henry/genes_code/my_model_4")

def graph_text(text:str):
    val = model(tf.constant([text]))[0]
    plt.figure(figsize=(10, 9))
    plt.title("Model Prediction of Like/Retweet Ratio", fontsize=25)
    plt.ylabel("Probaility of Classification", fontsize=20)
    plt.xlabel("Percentile Range", fontsize=20)
    plt.xticks(range(10), [f'[{i*10}% - {(i+1)*10}%)' for i in range(9)] + ["[90% - 100%]"])
    
    print(val[:10])
    plt.bar(range(10), val[:10])
    plt.show()

graph_text("""Stanford University’s Alex Stamos and Renee DiResta led an illegal US government effort to censor millions of American citizens in direct violation of the First Amendment and hundreds of years of American social norms""")

graph_text("Earth is our home. 💚 On #EarthDay and every day, we’re learning more about our world and how it’s changing – giving us a deeper appreciation for the planet we call home. Celebrate with us")
