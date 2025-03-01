import pickle 
import os


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', '.'))


pickle_hyper_filepath = os.path.join(parent_dir, 'hyperparams.pickle')

class HyperParamList:
    """
    A class representing a list of hyperparameters.

    Attributes:
        f_location (str): The file location of the hyperparameters.

    Methods:
        __init__: Initializes the HyperParamList object.
        update: Updates the hyperparameter list in the file.
        get: Gets the hyperparameter list from the file.
        add: Adds a new hyperparameter to the list.
        remove: Removes a hyperparameter from the list.
        edit_default_value: Edits the default value of a hyperparameter in the list.
    """
    def __init__(self):
        """
        Initializes the HyperParamList object and loads the hyperparameters from a pickle file.
        If the file does not exist, it creates it with some default hyperparameters.
        """
        try:
            with open(pickle_hyper_filepath,"rb") as handle:
                self.hyper_param_list=pickle.load(handle)

        except FileNotFoundError:
            print("file not found")
            with open(pickle_hyper_filepath, "wb") as handle:
                hyper_param_list = [
                    ('epochs', 100, 'Number of epochs to train for'),
                    ('patience', 50, 'Epochs to wait for no observable improvement for early stopping of training'),
                    ('cache', False, 'True/ram, disk or False. Use cache for data loading'),
                    ('batch', 16, 'Number of images per batch (-1 for AutoBatch)'),
                    ('imgsz', 640, 'Size of input images as integer or w,h'),
                    ('save', True, 'Save train checkpoints and predict results'),
                    ('save_period', -1, 'Save checkpoint every x epochs (disabled if < 1)'),
                    ('device', "None", 'Device to run on, i.e. cuda device=0 or device=0,1,2,3 or device=cpu'),
                    ('workers', 8, 'Number of worker threads for data loading (per RANK if DDP)'),
                    ('project', "None", 'Project name'),
                    ('name', "None", 'Experiment name'),
                    ('exist_ok', False, 'Whether to overwrite existing experiment'),
                    ('pretrained', False, 'Whether to use a pretrained model'),
                    ('optimizer', 'SGD', 'Optimizer to use, choices=[\'SGD\', \'Adam\', \'AdamW\', \'RMSProp\']'),
                    ('verbose', False, 'Whether to print verbose output'),
                    ('seed', 0, 'Random seed for reproducibility'),
                    ('deterministic', True, 'Whether to enable deterministic mode'),
                    ('single_cls', False, 'Train multi-class data as single-class'),
                    ('image_weights', False, 'Use weighted image selection for training'),
                    ('rect', False, 'Support rectangular training'),
                    ('cos_lr', False, 'Use cosine learning rate scheduler'),
                    ('close_mosaic', 10, 'Disable mosaic augmentation for final 10 epochs'),
                    ('resume', False, 'Resume training from last checkpoint'),
                    ('amp', True, 'Automatic Mixed Precision (AMP) training, choices=[True, False]'),
                    ('lr0', 0.01, 'Initial learning rate (i.e. SGD=1E-2, Adam=1E-3)'),
                    ('lrf', 0.01, 'Final learning rate (lr0 * lrf)'),
                    ('momentum', 0.937, 'SGD momentum/Adam beta1'),
                    ('weight_decay', 0.0005, 'Optimizer weight decay 5e-4'),
                    ('warmup_epochs', 3.0, 'Warmup epochs (fractions ok)'),
                    ('warmup_momentum', 0.8, 'Warmup initial momentum'),
                    ('warmup_bias_lr', 0.1, 'Warmup initial bias lr'),
                    ('box', 7.5, 'Box loss gain'),
                    ('cls', 0.5, 'Cls loss gain (scale with pixels)'),
                    ('dfl', 1.5, 'Dfl loss gain'),
                    ('fl_gamma', 0.0, 'Focal loss gamma (efficientDet default gamma=1.5)'),
                    ('label_smoothing', 0.0, 'Label smoothing (fraction)'),
                    ('nbs', 64, 'Nominal batch size'),
                    ('overlap_mask', True, 'Masks should overlap during training (segment train only)'),
                    ('mask_ratio', 4, 'Mask downsample ratio (segment train only)'),
                    ('dropout', 0.0, 'Use dropout regularization (classify train only)'),
                    ('val', True, 'Validate/test during training')
                ]

                pickle.dump(hyper_param_list,handle)

    def update(self):
        """Updates the hyperparameter list in the file."""
        with open(pickle_hyper_filepath, "wb") as handle:
            pickle.dump(self.hyper_param_list, handle)

    def get(self):
        """Gets the hyperparameter list from the file."""
        with open(pickle_hyper_filepath, "rb") as handle:
            self.hyper_param_list = pickle.load(handle)
        return self.hyper_param_list

    def add(self, name, default_value, tooltip):
        """Adds a new hyperparameter to the list.

        Args:
            name (str): The name of the hyperparameter.
            default_value: The default value of the hyperparameter.
            tooltip (str): The tooltip of the hyperparameter.
        """
        self.hyper_param_list.append((name, default_value, tooltip))

        # update file
        self.update()

    def remove(self, name):
        """Removes a hyperparameter from the list.

        Args:
            name (str): The name of the hyperparameter.
        """
        for param in self.hyper_param_list:
            if param[0] == name:
                self.hyper_param_list.remove(param)
                break

        # update file
        self.update()

    def edit_default_value(self, key, new_value):
        """Edits the default value of a hyperparameter in the list.

        Args:
            key (str): The name of the hyperparameter to be edited.
            new_value: The new default value of the hyperparameter.
        """
        for i, param in enumerate(self.hyper_param_list):
            if param[0] == key:
                self.hyper_param_list[i] = (key, new_value, param[2])
                break

        self.update()


if __name__ == '__main__':
    hl = HyperParamList()

    print(hl.get())