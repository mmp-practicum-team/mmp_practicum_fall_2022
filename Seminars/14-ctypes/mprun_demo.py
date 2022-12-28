import numpy as np

def replace_zeros_to_means_numpy(X):
    Y = np.copy(X).astype(np.float32)
    
    zero_mask = Y == 0
    selected_columns = np.any(~zero_mask, axis=0)
    means = np.zeros([1, Y.shape[1]], dtype=np.float32)
    means[:, selected_columns] = np.mean(
        Y[:, selected_columns], axis=0, where=~zero_mask[:, selected_columns], keepdims=True
    )
    Y[zero_mask] = np.repeat(means, Y.shape[0], axis=0)[zero_mask]

    return Y
