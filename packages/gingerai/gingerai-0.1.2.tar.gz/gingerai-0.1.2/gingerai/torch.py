import pickle
import copy


class TorchWrapper:
    """
    Wrapper class for torch model to save and load the model according to the ginger format.
    """
    def __init__(self, model, optimizer, loss_fn, dataset):
        self.model = copy.deepcopy(model)

        def reset_parameters(layer):
            if hasattr(layer, "reset_parameters"):
                layer.reset_parameters()

        self.model.apply(reset_parameters)

        self.optimizer = optimizer
        self.loss = loss_fn
        self.dataset = dataset

    def save_torch_model(self, save_path):
        f = open(save_path, "wb")
        pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    def load_torch_model(self, ginger_path):
        f = open(ginger_path, "rb")
        pickle.load(f)
        f.close()
