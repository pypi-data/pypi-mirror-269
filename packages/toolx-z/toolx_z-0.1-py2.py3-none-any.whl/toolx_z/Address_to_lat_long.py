from geopy.geocoders import Nominatim
from importlib import resources
import io

class Geocoder:
    def __init__(self):
        self.app=Nominatim(user_agent="myappnamehere")

    def get_coordinates(self, location):
        result=self.app.geocode(location).raw
        lat_and_long={key: float(value) for key, value in result.items() if key in ['lat', 'lon']}
        return lat_and_long.get('lat'), lat_and_long.get('lon')

# ###########调用方式如下：####################
# from geocoder import Geocoder
# # 创建 Geocoder 实例
# geocoder = Geocoder()
# # 输入地址变量
# your_loc = 'Arcadia'
# # 获取经纬度
# MY_LAT, MY_LONG = geocoder.get_coordinates(your_loc)
# # 打印结果
# print(MY_LAT)
# print(MY_LONG)