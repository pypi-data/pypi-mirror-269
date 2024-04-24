import mil.models
from mil.bag_representation import MILESMapping
from sklearn.tree import DecisionTreeClassifier


class MILESClassifier:

    def __init__(self, sigma2=4.5 ** 2, c=0.5):
        """

        """
        self.classifier = mil.models.MILES()
        self.model = None
        self.mapping = None
        self.sigma2 = sigma2
        self.c = c
        self.trainer = None

    def fit(self, x_train, y_train):
        """

        Parameters
        ----------
        x_train
        y_train
        """

        self.classifier.check_exceptions(x_train)
        self.mapping = MILESMapping(self.sigma2)
        mapped_bags = self.mapping.fit_transform(x_train)

        # train the SVM
        # self.model = LinearSVC(penalty="l1", C=self.c, dual=False, class_weight='balanced',max_iter=100000)

        self.model = DecisionTreeClassifier()
        self.model.fit(mapped_bags, y_train.flatten())

    def predict(self, x) -> int:
        """

        Parameters
        ----------
        x

        Returns
        -------

        """
        x = x.reshape(1, x.shape[0], x.shape[1])
        mapped_x = self.mapping.transform(x)
        return self.model.predict(mapped_x)
