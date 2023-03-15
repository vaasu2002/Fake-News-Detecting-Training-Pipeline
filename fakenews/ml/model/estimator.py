class TargetValueMapping:
    def __init__(self):
        self.Fake: int = 0
        self.Truth: int = 1

    def to_dict(self):
        """
        Returns:
            dict: {'Fake': 0, 'Truth': 1}
        """
        return self.__dict__ 

    def reverse_mapping(self):
        """
        Returns:
            dict: {0: 'Fake', 1: 'Truth'}
        """
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))