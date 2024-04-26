import pickle
import copy


class TorchNetWrapper:
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
        with open(save_path, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_torch_model(ginger_path):
        try:
            with open(ginger_path, "rb") as f:
                loaded_data = pickle.load(f)

            new_instance = TorchNetWrapper()

            for key, value in loaded_data.__dict__.items():
                setattr(new_instance, key, value)

            return new_instance

        except (pickle.UnpicklingError, AttributeError, KeyError) as e:
            print(f"Error loading model from {ginger_path}: {e}")
            raise

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise
