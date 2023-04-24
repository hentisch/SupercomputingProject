import pickle
import matplotlib.pyplot as plt

with open("history_4.pkl", "rb") as f:
    hist = pickle.load(f)

plt.figure(figsize=(20, 9))
plt.plot(hist['val_accuracy'])
plt.title("Accuracy After Epochs of Training", fontsize=25)
plt.ylabel("Categorical Accuracy", fontsize=20)
plt.xlabel("Epochs of Training", fontsize=20)
plt.savefig("training_graph.png")
plt.show()
