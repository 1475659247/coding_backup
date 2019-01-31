from config.config import *
from sql_orm.orm import *
import time
if __name__ == "__main__":
    #test parity_brand
    #删
    store_s.query(ParityBrand).filter(ParityBrand.brand_id != -1).delete()
    #加
    print(store_s.query(func.count('*')).select_from(ParityBrand).scalar())
    store_s.add(ParityBrand(1234,"测试1","nike","nike.jpg"))
    store_s.add(ParityBrand(5678,"测试2","adidass","nike.jpg"))
    #查
    brand = store_s.query(ParityBrand).all()
    print(brand)

    #改
    store_s.query(ParityBrand).filter(ParityBrand.brand_id == 1234).update({ParityBrand.brand_logo: "haha.jpg"}) 
    store_s.commit()
    brand = store_s.query(ParityBrand).all()
    print(brand)

    parity_brand = ParityBrand(9112,"测试3","nike2","wawa.jpg")
    #如果主键存在则更新，否则insert
    parity_brand.id = 69
    store_s.merge(parity_brand)
    store_s.commit()
    brand = store_s.query(ParityBrand).all()
    print(brand)
