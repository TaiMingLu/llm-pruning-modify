import matplotlib.pyplot as plt


num_layers = [
    "2 layers",
    "4 layers",
    "8 layers",
    "16 layers",
]
labels = [
    "S50",
    "L200_S50"
]
S50_ppls      = [24.92, 17.29, 13.43, 11.22]
L200_S50_ppls = [30.79, 17.10, 12.67,  9.60]
S50_accs      = [49.41, 52.41, 53.43, 58.09]
L200_S50_accs = [51.14, 52.49, 55.96, 63.38]

S50_arc_c      = [25.94, 27.39, 32.51, 35.07]
L200_S50_arc_c = [24.74, 28.33, 34.04, 38.05]

S50_hs      = [35.67, 40.88, 52.16, 59.2]
L200_S50_hs = [35.29, 41.47, 54.52, 67.23]

fig, axes = plt.subplots(2, 2, figsize=(10, 10))


axes[0][0].plot(num_layers, S50_ppls, label = 'S50')
axes[0][0].plot(num_layers, L200_S50_ppls, label = 'L200_S50')
axes[0][0].legend()
axes[0][0].grid(True)
axes[0][0].set_ylabel("WikiText PPL")
axes[0][0].set_xlabel("Number of Layers")
axes[0][0].set_title("Model Size vs WikiText PPL")

axes[1][0].plot(num_layers, S50_accs, label = 'S50')
axes[1][0].plot(num_layers, L200_S50_accs, label = 'L200_S50')
axes[1][0].legend()
axes[1][0].grid(True)
axes[1][0].set_ylabel("Winogrande ACC")
axes[1][0].set_xlabel("Number of Layers")
axes[1][0].set_title("Model Size vs Winogrande ACC")

axes[0][1].plot(num_layers, S50_arc_c, label = 'S50')
axes[0][1].plot(num_layers, L200_S50_arc_c, label = 'L200_S50')
axes[0][1].legend()
axes[0][1].grid(True)
axes[0][1].set_ylabel("ARC-C ACC")
axes[0][1].set_xlabel("Number of Layers")
axes[0][1].set_title("Model Size vs ARC-C ACC")

axes[1][1].plot(num_layers, S50_hs, label = 'S50')
axes[1][1].plot(num_layers, L200_S50_hs, label = 'L200_S50')
axes[1][1].legend()
axes[1][1].grid(True)
axes[1][1].set_ylabel("Hellaswag ACC")
axes[1][1].set_xlabel("Number of Layers")
axes[1][1].set_title("Model Size vs Hellaswag ACC")

plt.tight_layout()

plt.savefig("tests/model_size_vs_ppl_acc.png")

