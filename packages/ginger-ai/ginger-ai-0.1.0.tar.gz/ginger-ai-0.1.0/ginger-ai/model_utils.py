import torch
import pickle
import copy

def save_torch_model(model, optimizer, loss_fn_class, save_path):
   """
    Save a PyTorch model to a serialized .ginger file.
    """
   
    new_model = copy.deepcopy(model)

    def reset_parameters(layer):
        if hasattr(layer, 'reset_parameters'):
            layer.reset_parameters()

    new_model.apply(reset_parameters)

    optimizer_info = {
        'class': optimizer.__class__,
        'state_dict': optimizer.state_dict(),
    }

    loss_info = {
        'class_name': loss_fn_class.__name__,
    }

    model_data = {
        'model': new_model,
        'optimizer': optimizer_info,
        'loss': loss_info,
    }

    with open(save_path, 'wb') as f:
        pickle.dump(model_data, f)

def load_torch_model(ginger_path):
    """
    Load a PyTorch model from a serialized .ginger file.
    """
    
    with open(ginger_path, 'rb') as f:
        model_data = pickle.load(f)

    model = model_data['model']
    optimizer_info = model_data['optimizer']

    loss_fn_mapping = {
        'CrossEntropyLoss': torch.nn.CrossEntropyLoss,
        'NLLLoss': torch.nn.NLLLoss,
    }

    loss_fn_class_name = model_data['loss']['class_name']
    loss_fn_class = loss_fn_mapping.get(loss_fn_class_name, torch.nn.CrossEntropyLoss)

    loss_fn = loss_fn_class()

    return model, optimizer_info, loss_fn
