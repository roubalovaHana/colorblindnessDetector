class ReportResultObject:
    """
    Auxiliary object for storing information about the triggered warnings.
    """
    def __init__(self, title: str):
        self.title = title
        self.found = False
        self.colors = []
        self.simulated = None
