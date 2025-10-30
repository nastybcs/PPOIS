class Report:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.generated_at = None
        self.data = None
        self.generated_at = None

    def generate(self):
        raise NotImplementedError("Метод generate должен быть реализован в подклассе")
