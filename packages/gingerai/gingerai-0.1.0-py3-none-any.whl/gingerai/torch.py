import torch
import pickle
import copy
from torch import optim
from torch.nn import functional as F

def save_torch_model(model, optimizer_class, loss_fn_class, dataset, save_path):
    """
    Save a PyTorch model with its structure, optimizer, loss function, and dataset to a serialized file.
    """
    # Deep copy the model structure without weights
    new_model = copy.deepcopy(model)

    # Reset parameters to ensure no weights are copied
    def reset_parameters(layer):
        if hasattr(layer, 'reset_parameters'):
            layer.reset_parameters()

    new_model.apply(reset_parameters)

    # Store only the class of the optimizer and loss function
    optimizer_info = {
        'class_name': optimizer_class.__name__,
    }

    loss_info = {
        'class_name': loss_fn_class.__name__,
    }

    # Include the dataset in the serialized data structure
    model_data = {
        'model': new_model,
        'optimizer': optimizer_info,
        'loss': loss_info,
        'dataset': dataset,
    }

    # Serialize and save the model data along with the dataset
    with open(save_path, 'wb') as f:
        pickle.dump(model_data, f)

def load_torch_model(ginger_path):
    """
    Load a PyTorch model from a serialized .ginger file, re-creating the optimizer, loss function, and dataset.
    """
    with open(ginger_path, 'rb') as f:
        model_data = pickle.load(f)

    # Extract the model structure
    model = model_data['model']

    # Re-create the optimizer from the class name
    optimizer_class_name = model_data['optimizer']['class_name']
    optimizer_class = getattr(optim, optimizer_class_name, optim.SGD)
    optimizer = optimizer_class(model.parameters())

    # Re-create the loss function from the class name
    loss_fn_class_name = model_data['loss']['class_name']
    loss_fn_class = getattr(F, loss_fn_class_name, torch.nn.CrossEntropyLoss)
    loss_fn = loss_fn_class()

    # Retrieve the dataset from the serialized data
    dataset = model_data.get('dataset', None)

    return model, optimizer, loss_fn, dataset
