import enum
from collections import namedtuple


class TrainClass(enum.Enum):
    ALL = '2'
    對號 = ("'1100','1101','1102','1103','1107','1108','1109',"
          "'110A','110B','110C','110D','110E','110F','1110',"
          "'1111','1114','1115','1120'")
    非對號 = "'1131','1132','1140'"


RESULT_FIELDS = {
    'train_type': "./td[1]//div/span",
    'train_code': "./td[2]//a",
    'versa': "./td[3]/font",
    'route': "./td[4]/font",
    'launch_time': "./td[5]/font",
    'arrive_time': "./td[6]/font",
    'duration': "./td[7]/font",
    'comment': "./td[8]//div/span[@id='Comment']",
    'price': "./td[9]//span",
    'order_url': "./td[10]//a/@href",
}

ResultEntry = namedtuple('ResultEntry', RESULT_FIELDS.keys())
