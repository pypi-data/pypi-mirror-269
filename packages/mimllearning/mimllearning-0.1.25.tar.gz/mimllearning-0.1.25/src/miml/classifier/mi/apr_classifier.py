import mil.models


class APRClassifier:

    def __init__(self) -> None:
        """

        """
        self.classifier = mil.models.APR(verbose=0)

    def fit(self, x_train, y_train) -> None:
        """

        Parameters
        ----------
        x_train
        y_train
        """
        self.classifier.fit(x_train, y_train)

    def predict(self, x):
        x = x.reshape(1, x.shape[0], x.shape[1])
        return self.classifier.predict(x)
