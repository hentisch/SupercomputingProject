import json
import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import time

path = "dataset-2.json"

f = open(path)

data = json.load(f)
#training_data,data = train_test_split(data, random_state=7)
data, training_data = train_test_split(data, random_state=7)
model = tf.keras.models.load_model("/home/henry/genes_code/my_model_3")

like_to_retweet_ratios = []
for post in data:
    try:
        ratio = post["likes"] / post["retweets"]
    except ZeroDivisionError:
        ratio = 2147483647 #32 bit signed int limit

    like_to_retweet_ratios.append(ratio)

percentiles = np.percentile(like_to_retweet_ratios, np.array(list(range(0, 11)))*10)
percentiles[1] += 0.001 # Neccisary to create a percentile range, has a very negligible impact
plt.figure(figsize=(20, 9))
plt.bar(range(10), percentiles[1:])
plt.yscale('log')
plt.ylabel("Like to Retweet Ratio (Log Scale)", fontsize=20)
plt.xlabel("Percentile Range", fontsize=20)
plt.xticks(range(10), [f'[{i*10}% - {(i+1)*10}%)' for i in range(9)] + ["[90% - 100%]"])
plt.title("Percentile Ranges of Like/Retweet Ratio Among Training Dataset Tweets", fontsize=25)
plt.savefig("Percentile_Ranges.png")

corpus = []
outputs = []
for data_point in data:
    text = data_point["content"]
    text = text.lower()

    corpus.append(tf.constant([text]))
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
    
    outputs.append(output_point)

# corpus = np.split(np.array(corpus), 256)
# outputs = np.split(np.array(outputs), 256)
percentile_distances = []
percentile_accurate_count = 0

misc_1_accurate_count = 0
misc_2_accurate_count = 0

# for i_1, batch in enumerate(corpus):
#     predictions = model(batch)
#     labels = outputs[i_1]
#     for i_2, prediction in enumerate(predictions):
#         max_index = np.argmax(prediction)[0]
#         if max_index == np.argmax(labels[i_2]):
#             percentile_accurate_count += 1
        
#         percentile_distances.append(abs(np.argmax(labels[i_2]) - max_index))

for i, post in enumerate(tqdm(corpus)):
    prediction = model(post)[0]
    label = outputs[i]
    predicted_max_index = np.argmax(prediction[:10])
    actual_max_index = np.argmax(label)
    if predicted_max_index == actual_max_index:
            percentile_accurate_count += 1
        
    percentile_distances.append(abs(predicted_max_index-actual_max_index))

print(f"{percentile_accurate_count / len(data)} - Percent Perfect")
print(f"{np.average(percentile_distances)} - Average Distance")

model.evaluate(corpus)
