# ======================================================================================================================

"""
GRNN architecture will be implemented here

GRNN PARAMETERS
    train_set: Training data set
    test_set: Testing data set
    target: str
    predictor: list
    loss function: str
    sigma: list --> sigma_info[0] = sigma_min
                    sigma_info[1] = sigma_max
                    sigma_info[2] = sigma_search
                    default = 'default'
    rounded: bool
"""

# ======================================================================================================================
import pandas as pd
import numpy as np
from utility import GET_TARGET_INDEX
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt

class GRNN:
    def __init__(self, train_set, test_set, target, predictors, loss_function, sigma_info='default', rounded=False):
        # keep the filtered real dataframe for visualization
        self.train_set_df = train_set[predictors + target]
        self.test_set_df = test_set[predictors]

        # create numpy array copies of the dataframe
        self.train_set = train_set[predictors+target].to_numpy().transpose()
        self.test_set = test_set[predictors].to_numpy().transpose()

        # more parameters
        self.predictors = predictors
        self.target = target
        self.sigma_info = sigma_info
        self.loss_function = loss_function
        self.rounded = rounded

        # layers
        self.hiddenlayer = []
        self.summationlayer = []

        # optimum sigma will be searched in Train() and will be used int Test()
        self.optimum_sigma = 0

        # variable will be used in Train(), with every different sigma, this changes
        self.final_output_train = list()

        # variable will be used in Test(), the output with optimum sigma
        self.final_output = list()

        # performance metrices
        self.mse = float()
        self.mae = float()
        self.rmse = float()

        # if sigma is set to default, just test it with given sigma. Metrices = false
        if self.sigma_info is 'default':
            self.optimum_sigma = ((len(self.train_set[0]) - 1) / 2) / 3
            self.Test()

        # if sigma is not default, train the model and then test it afterwards
        else:
            self.Train()
            self.Test()


    def Test(self):
        """
        # Tests the model
        """

        # X_train: input of trainset // Y_train: output of trainset // X_test: input of
        X_train = []
        X_test = []
        for i in range(len(self.train_set) - 1):
            X_train.append(self.train_set[i])
            X_test.append(self.test_set[i])

        # transpose the arrays to make the proccess easier for the next steps
        X_train = np.array(X_train).transpose()
        X_test = np.array(X_test).transpose()

        Y_train = self.train_set[-1].tolist()

        # start with a fresh list
        self.final_output = []
        for sample in X_test:
            eucd = self.eucDistance(sample, X_train)
            self.hiddenlayer = self.actFunction(eucd, self.optimum_sigma)
            num, denom = self.SUMMATION(Y_train)
            self.OUTPUT(num, denom, test=True)

    def Train(self):
        # prepare data for training

        X_train = []
        X_test = []
        Y_train = []
        Y_test = []
        for i in range(len(self.train_set)-1):
            X1, X2 = train_test_split(self.train_set[i], test_size=0.2, shuffle=False)
            X_train.append(X1)
            X_test.append(X2)

        Y_train, Y_test = train_test_split(self.train_set[-1], test_size=0.2, shuffle=False)

        # transpose the arrays to make the proccess easier for the next steps
        X_train = np.array(X_train).transpose()
        Y_train = np.array(Y_train).transpose()

        # sigma preferences
        sigma_min = self.sigma_info[0]
        sigma_max = self.sigma_info[1]
        sigma_search = self.sigma_info[2]

        # set sigma values according to info taken
        # for i in range(sigma_search+1)
        #   p = (sigma_max - sigma_min) / (sigma_search + 1)
        #   sigma_values.append(sigma_min+p*i)
        sigma_values = [(sigma_min + (((sigma_max - sigma_min) / (sigma_search + 1)) * i)) for i in
                        range(1, sigma_search + 1)]

        # for each sigma, predict the output and check the loss value
        loss = np.inf
        new_loss = 0
        for sigma in sigma_values:

            # reset final output
            self.final_output_train = []

            # predict Y of every X in X_train
            for sample in X_train:
                eucd = self.eucDistance(sample, X_train)
                self.hiddenlayer = self.actFunction(eucd, sigma)
                num, denom = self.SUMMATION(Y_train)
                self.OUTPUT(num,denom, test=False)

            # calculate loss, if get lesser, assign it, then update optimum_sigma and final_output
            new_loss = self.getLoss(Y_train, self.final_output_train)
            if loss > new_loss:
                loss = new_loss
                self.optimum_sigma = sigma
                self.final_output = self.final_output_train

        # calculate errors
        self.mse = mean_squared_error(Y_train, self.final_output)
        self.mae = mean_absolute_error(Y_train, self.final_output)
        self.rmse = r2_score(Y_train, self.final_output)

    # return euclidean distances
    def eucDistance(self, sample, X_train):
        eucd = []
        for i in range(len(sample)):
            e = []
            for j in range(len(X_train)):
                e.append(float(pow(sample[i] - X_train[j][i], 2)))
            eucd.append(e)
        return eucd

    # return weights
    def actFunction(self, eucd, sigma):
        weight = []
        for i in range(len(self.predictors)):
            w = []
            for j in range(len(eucd[0])):
                w.append(np.exp(-(float(pow(eucd[i][j], 2)) / float(2 * pow(sigma, 2)))))
            weight.append(w)
        return weight

    # return num and denom
    def SUMMATION(self, Y_train):       #FIX THE BUG
        num, denom = 0, 0
        for i in range(len(self.predictors)):
            for j in range(len(self.hiddenlayer[0])):
                num += self.hiddenlayer[i][j] * Y_train[j]
                denom += self.hiddenlayer[i][j]
        return num, denom

    # in train state, append to final_output_train. in test state, append to final_output
    def OUTPUT(self, num, denom, test):
        Y = num/denom
        if test is True:
            self.final_output.append(Y)
        else:
            self.final_output_train.append(Y)

    # decide which function to use in training
    def getLoss(self, Y_train, OUTPUT):
        if self.loss_function == 'MSE':
            return mean_squared_error(Y_train, OUTPUT)
        elif self.loss_function == 'MAE':
            return mean_absolute_error(Y_train, OUTPUT)
        elif self.loss_function == 'RMSE':
            return r2_score(Y_train, OUTPUT)

    # Frequency of predictor
    def Visualize2(self):
        # TODO
        # will be changed
        sns.set()
        x = self.train_set_df[self.predictor]
        ax = sns.distplot(x)
        plt.show()

    # Dot-linear (Scatter) graph
    def Visualize(self):
        # TODO
        # will be changed
        sns.set(style='whitegrid', palette='hsv')

        sns.lmplot(x=self.predictor,y=self.target, data=self.train_set_df)
        plt.show()
