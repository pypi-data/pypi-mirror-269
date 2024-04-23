import logging

class IMSLogger(logging.Logger):
  def __init__(self, name, level=logging.INFO):
    super().__init__(name, level)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    self.addHandler(handler)

def get_logger(name):
  logger = IMSLogger(name)
  return logger
