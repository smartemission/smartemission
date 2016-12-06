`calibration.py` is the main file. It uses functions from 
`load_data.py`, `prepare_data.py`, `model_data.py` and 
`visualize_data.py`. 

The main function in `calibration.py` needs 1 arguments from the command
line: the column to predict. A standard call would look like this:

    python calibration.py "../../io/data/train.csv" O3_Waarden