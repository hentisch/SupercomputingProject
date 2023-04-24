import json
from transformers import BertTokenizer
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import ssl
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
ssl._create_default_https_context = ssl._create_unverified_context

path = "dataset-2.json"

f = open(path)

data = json.load(f)

training_data, testing_data = train_test_split(data, random_state=7)
# like_to_retweet_ratios = [post["likes"] / post["retweets"] for post in training_data]
like_to_retweet_ratios = []
for post in training_data:
    try:
        ratio = post["likes"] / post["retweets"]
    except ZeroDivisionError:
        ratio = 2147483647

    like_to_retweet_ratios.append(ratio)

percentiles = np.percentile(like_to_retweet_ratios, np.array(list(range(0, 11)))*10)
percentiles[1] += 0.001 # Neccisary to create a percentile range, has a very negligible impact

print(percentiles)

corpora = []
outputs = []
for data in (training_data, testing_data):
    corpus = []
    output = []
    for data_point in data:
        text = data_point["content"]
        text = text.lower()

        corpus.append(text)
        # different levels of like/retweets
        output_point = []
        for i, percentile in enumerate(percentiles[1:]):
            try:
                ratio = data_point["likes"] / data_point["retweets"]
            except ZeroDivisionError:
                ratio = 2147483647

            if ratio < percentile and ratio >= percentiles[i-1]:
                output_point.append(1)
            else:
                output_point.append(0)
        
        output.append(output_point)
    corpora.append(corpus)
    outputs.append(output)

# training_corpus, training_output, testing_data, testing_output = train_test_split(corpus, output)
training_corpus, testing_corpus = corpora
training_data, testing_data = outputs


bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")
#These allow us to proccess our text into embeddings BERT can understand

text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
preprocessed_text = bert_preprocess(text_input)
outputs = bert_encoder(preprocessed_text)
#Preproccess the text for BERT

l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
l = tf.keras.layers.Dense(10, activation='sigmoid', name="output")(l)
#Setup our custom layers

model = tf.keras.Model(inputs=[text_input], outputs = [l])
#Create the model

METRICS = [
      tf.keras.metrics.CategoricalAccuracy(name='accuracy'),
      tf.keras.metrics.Precision(name='precision'),
      tf.keras.metrics.Recall(name='recall')
]
#Define the metrics to be used for 

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=METRICS)
model.summary()
#Compile the model through TensorFlow and print a summary of the compiled model

hist = model.fit(training_corpus, training_data, epochs=100, validation_data=(testing_corpus, testing_data))
#Train the model

model.save('my_model_4') # Save the model for future use and analysis

with open("history_4.pkl", "wb") as f:
    pickle.dump(hist.history, f)
    # Save the model history over the training proccess