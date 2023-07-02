#type: ignore

import matplotlib.pyplot as plt
import matplotlib as mpl
from keras.models import model_from_json


class Model():
    def save(hypermodel, name):
        # serialize model to JSON
        model_json = hypermodel.to_json()
        with open(f'models/{name}.json', "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        hypermodel.save_weights(f'models/{name}.h5')

    
    def recover(name):
        # load json and create model
        json_file = open(f'models/{name}.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(f'models/{name}.h5')

        return loaded_model


    def plot_metrics(history):
        # define figure size
        mpl.rcParams['figure.figsize'] = (12, 10)
        # define colors
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        # define metrics
        metrics = ['loss', 'prc', 'precision', 'recall', 'f1_score_macro', 'accuracy']

        # plot each metric per epoch
        for n, metric in enumerate(metrics):
            name = metric.replace("_"," ").capitalize()
            plt.subplot(2,3,n+1)
            plt.plot(history.epoch, history.history[metric], color=colors[0], label='Train')
            plt.plot(history.epoch, history.history['val_'+metric],
                    color=colors[0], linestyle="--", label='Val')
            plt.xlabel('Epoch')
            plt.ylabel(name)

            if metric == 'loss':
                plt.ylim([0, plt.ylim()[1]])
            elif metric == 'auc':
                plt.ylim([0.8,1])
            else:
                plt.ylim([0,1])

            plt.legend()


    def save_results(file_path, row_number, results_row):    
        # Open file in read mode
        read_file = open(file_path, 'r')
        replaced_content = ""
        row_count = 0

        for row in read_file:
            row = row.strip()
            # replacing the text if the row number is reached
            if row_count == row_number:
                new_row = results_row
            else:
                new_row = row
            replaced_content = replaced_content + new_row + "\n"
            row_count += 1
        read_file.close()

        # Open file in write mode
        write_file = open(file_path, "w")
        # overwriting the old file contents with the new/replaced content
        write_file.write(replaced_content)
        write_file.close()