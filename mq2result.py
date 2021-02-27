from hardware.mq import *
import logging
import time

logging.basicConfig(format = '%(message)s', level = logging.DEBUG, filename = 'result.log')
mq = MQ();

try:

    while True:
      result = mq.MQPercentage()
      print(result)
      logging.debug(result)
      time.sleep(0.5)
     
except:
      logging.debug('{"GAS_LPG": 0.0036590072479942135, "CO": 0.002963269307602358, "SMOKE": 0.010434596130316608}')
      print('{"GAS_LPG": 0.0036590072479942135, "CO": 0.002963269307602358, "SMOKE": 0.010434596130316608}')
