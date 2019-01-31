from config.config import *
engine = create_engine(db_url,encoding='utf8', convert_unicode=True)
# 创建DBSession类型:
Session = sessionmaker(bind=engine) 
store_s = Session()
Base = declarative_base()
class ParityBrand(Base):
    __tablename__ = "ez_parity_brand"
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    brand_id = Column(INTEGER(unsigned=True),nullable=False)
    brand_zh_name = Column(String(255))
    brand_en_name = Column(String(255))
    brand_logo = Column(String(255))
    brand_logo_url = Column(String(255))
    status = Column(INTEGER(unsigned=True,zerofill=True))

    def __init__(self,brand_id=0,brand_url='',brand_zh_name='',brand_en_name='',brand_logo_url='',brand_logo='',status=0):
        self.brand_id = brand_id
        self.brand_zh_name = brand_zh_name
        self.brand_en_name = brand_en_name
        self.brand_logo = brand_logo
        self.brand_logo_url = brand_logo_url
        self.status = status

    def __repr__(self):
        return '<parity_brand:%s %d %s %s %s %s %s>' % (self.id,\
                self.brand_id,self.brand_zh_name,self.brand_en_name,\
                self.brand_logo,self.brand_logo_url,self.status) 

class ParityProduct(Base):
    __tablename__ = "ez_parity_product"
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    product_id = Column(String(32),nullable=False)
    model = Column(String(255),nullable=False)
    #class_id = Column(INTEGER(unsigned=True))
    site_id = Column(INTEGER(unsigned=True),nullable=False)
    brand_id = Column(INTEGER(unsigned=True),nullable=False)
    price_id = Column(INTEGER(unsigned=True),nullable=False)
    goods_time = Column(INTEGER(unsigned=True,zerofill=True))
    sales = Column(INTEGER(unsigned=True,zerofill=True),nullable=False)
    name = Column(String(255),nullable=False)
    image_url = Column(String(255))
    image = Column(String(255))
    url = Column(String(255),nullable=False)
    status = Column(INTEGER(unsigned=True,zerofill=True))
    type = Column(INTEGER(unsigned=True,zerofill=True))

    def __repr__(self):
        return '<parity_product id:%s product_id:%s model:%s site_id:%s brand_id:%s price_id:%s goods_time:%s sales:%s name:%s image_url:%s image:%s url:%s status:%s type:%s>' % \
                (self.id,self.product_id,self.model,self.site_id,\
                 self.brand_id,self.price_id,self.goods_time,self.sales,self.name,\
                 self.image_url,self.image,self.url,self.status,self.type)

class ParityPrice(Base):
    __tablename__ = "ez_parity_price"
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    product_id = Column(String(32),nullable=False)
    price = Column(Numeric(precision=10, scale=3),nullable=False) 
    update_time = Column(INTEGER(unsigned=True),nullable=False)

class ParitySite(Base):
    __tablename__ = "ez_parity_site"
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    site_id = Column(INTEGER(unsigned=True), nullable=False)
    site_name = Column(String(255),nullable=False)
    site_type = Column(INTEGER(unsigned=True,zerofill=True))
    site_telephone = Column(String(125))
    site_logo = Column(String(255),nullable=False)
    site_certification = Column(String(255))
    site_web = Column(String(255),nullable=False)
    status = Column(INTEGER(unsigned=True,zerofill=True))

    
'''
class ParityCLass(Base):
    __tablename__ = "parity_class"
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    class_id = Column(INTEGER(unsigned=True))
    class_name = Column(String(255),nullable=False)
    class_image = Column(String(255),nullable=False)
    def __init__(self,class_id,class_name,class_image):
        self.class_id = class_id
        self.class_name = class_name
        self.class_image = class_image

    def __repr__(self):
        return '<parity_class:%d %d %s %s>' % (self.id,\
                self.class_id,self.class_name,self.class_image)
'''
    
def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)
