{
    "name": "Mnist_LeNet",
    "n_gpu": 1,
    "istune" : true,
    "arch": {
        "type": "MnistModel",
        "args": {}
    },
    "data_loader": {
        "type": "MnistDataLoader",
        "args":{
            "data_dir": "data/",
            "batch_size": [4, 16, 32],
            "shuffle": true,
            "validation_split": 0.1,
            "num_workers": 2
        }
    },
    "optimizer": {
        "type": "Adam",
        "args":{
            "lr": [1e-4, 1e-1],
            "weight_decay": 0,
            "amsgrad": true
        }
    },
    "loss": "nll_loss",
    "metrics": [
        "accuracy", "top_k_acc"
    ],
    "lr_scheduler": {
        "type": "StepLR",
        "args": {
            "step_size": 50,
            "gamma": 0.1
        }
    },
    "trainer": {
        "epochs": 2,

        "save_dir": "saved/",
        "save_period": 1,
        "verbosity": 2,
        
        "monitor": "min val_loss",
        "early_stop": 10,

        "tensorboard": true
    }
}