#importing necessary libraries
import numpy as np

class Models():
    def __init__(self, dataframe):
        self.__classifier, self.__scores, self.__ct = self.select_model(dataframe)

    #getting the model
    @property
    def classifier(self):
        return self.__classifier

    #getting the score
    @property
    def scores(self):
        return self.__scores

    #getting preprocessing object for strings
    @property
    def ct(self):
        return self.__ct 

    '''
    selecting most optimal model by comparing all available models

    parameters:
    dataframe   - dataframe of the model

    returns:
    classifier  - model object
    scores      - accuracy score of the model
    '''
    def select_model(self, dataframe):
        #separating independent and dependent variables
        x = dataframe.iloc[:, :-1].values
        y = dataframe.iloc[:, -1].values

        #getting specific indices containing string values
        index = []
        for i in range(len(x[0])):
            if type(x[0][i]) == str:
                index.append(i)

        #encoding string variables for modelling
        ct = None
        if len(index) > 0:
            from sklearn.compose import ColumnTransformer
            from sklearn.preprocessing import OneHotEncoder
            ct = ColumnTransformer(transformers = [('encoder', OneHotEncoder(), index)], remainder = 'passthrough')
            x = np.array(ct.fit_transform(x))

        #separating training and testing set
        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

        #getting all models and predicted value
        models = [self.knn, self.logistic, self.naive, self.random_forest, self.svm]
        classifier = []
        pred = []
        for model in models:
            model_classifer, y_pred = model(x_train, x_test, y_train)
            classifier.append(model_classifer)
            pred.append(y_pred)

        #checking how specific the model is for identifying high cholesterol value
        specificity = []
        from sklearn.metrics import confusion_matrix, accuracy_score
        for i in range(len(pred)):
            cm = confusion_matrix(y_test, pred[i])
            specificity.append(cm[0][0] / (cm[0][0] + cm[0][1]))

        #getting accuracy scores of the models
        scores = []
        from sklearn.model_selection import cross_val_score
        for i in range(len(classifier)):
            scores.append(cross_val_score(classifier[i], x, y, cv = 20).mean())

        #removing models which does not meet accuracy criteria
        i = 0
        while i < len(scores):
            if ((scores[i] + specificity[i]) / 2) < 0.8:
                classifier.pop(i)
                pred.pop(i)
                specificity.pop(i)
                scores.pop(i)
            i += 1

        #selecting the most optimal model
        if len(specificity) > 0:
            optimal = (specificity[0] + scores[0]) / 2
            index = 0
            for i in range(1, len(specificity)):
                new_optimal = (specificity[i] + scores[i]) / 2
                if optimal < new_optimal:
                    optimal = new_optimal
                    index = i

            return classifier[i], scores[i], ct
        else:
            return None, None, None

    '''
    knn classification model
    '''
    def knn(self, x_train, x_test, y_train):
        #scaling the independent variables
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

        #creating the classifier
        from sklearn.neighbors import KNeighborsClassifier
        classifier = KNeighborsClassifier(n_neighbors = 5)
        classifier.fit(x_train, y_train)

        #predicting the dependent variables
        y_pred = classifier.predict(x_test)

        return classifier, y_pred

    def logistic(self, x_train, x_test, y_train):
        #scaling the independent variables
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

        #creating the classifier
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(class_weight = 'balanced')
        classifier.fit(x_train, y_train)

        #predicting the dependent variables
        y_pred = classifier.predict(x_test)

        return classifier, y_pred

    def naive(self, x_train, x_test, y_train):
        #scaling the independent variables
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

        #creating the classifier
        from sklearn.naive_bayes import GaussianNB
        classifier = GaussianNB()
        classifier.fit(x_train, y_train)

        #predicting the dependent variables
        y_pred = classifier.predict(x_test)

        return classifier, y_pred

    def random_forest(self, x_train, x_test, y_train):
        #creating the classifier
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(criterion = 'entropy', class_weight = 'balanced')
        classifier.fit(x_train, y_train)

        #predicting the dependent variables
        y_pred = classifier.predict(x_test)

        return classifier, y_pred

    def svm(self, x_train, x_test, y_train):
        #scaling the independent variables
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

        #creating the classifier
        from sklearn.svm import SVC
        classifier = SVC(kernel = 'rbf', class_weight = 'balanced')
        classifier.fit(x_train, y_train)

        #predicting the dependent variables
        y_pred = classifier.predict(x_test)

        return classifier, y_pred