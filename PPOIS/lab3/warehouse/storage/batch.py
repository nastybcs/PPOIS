import datetime
class Batch:
    def __init__(self, product, batch_id, quantity, exp_date=None):
        self.product = product
        self.batch_id = batch_id
        self.quantity = quantity
        self.exp_date = exp_date
        self.received_at = datetime.datetime.now()


    def age_days(self):
        return (datetime.datetime.now() - self.received_at).days
    def is_expired(self):
        if self.exp_date:
            return self.exp_date < datetime.date.today()
        return False
