import matplotlib.pyplot as plt
import pickle
import tensorflow as tf

with open("history_4.pkl", "rb") as f:
    history = pickle.load(f)

print(type(history))
print(history["val_accuracy"])
