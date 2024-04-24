from matplotlib import pyplot as plt

def plot_training_metric_history(history,metrics_list):
    metrics_values_list=[]
    for metric in metrics_list:
        metrics_values_list.append(history.history[metric])
    for index,metric in enumerate(metrics_values_list):
        print(index)
        plt.subplot(1,2,1+index)
        plt.plot(metric,label=metrics_list[index])
    plt.tight_layout()
    plt.show()    

def plot_validation_metric_history(history,metrics_list):
    metrics_values_list=[]
    for metric in metrics_list:
        metrics_values_list.append(history.history[metric])
    for index,metric in enumerate(metrics_values_list):
        print(index)
        plt.subplot(1,2,1+index)
        plt.plot(metric,label=metrics_list[index])
    plt.tight_layout()
    plt.show()   

def plot_metric_history(history,metric_list,training_or_validation="training"):
    if training_or_validation=="training":
        plot_training_metric_history(history,metric_list)
    elif training_or_validation=="validation":
        plot_validation_metric_history(history,metric_list)
    else:
        print(f"{training_or_validation} not recognized")