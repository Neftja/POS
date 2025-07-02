from datetime import date, datetime
from sqlmodel import Field, SQLModel
from enum import Enum
from sqlalchemy import Column, String



class TypeProduct(str, Enum):
    grams = "grams" #граммы
    boxing = "boxing" #коробки с сырьем для приготовления
    
    package = "package" #упаковка (пример соусники)
    product = "product" #продукция на продажу (пример вода)
    water = "water" #продукция на продажу (пример вода)

class TypeOrder(str, Enum):
    edostav = 'edostav'
    yandex = 'yandex'
    dostav = 'dostav'
    window = 'window'  
    samovivoz = 'samovivoz'
   
    
class TypeRecipes(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str    
    value: str
    
    
class Suppliers(SQLModel, table=True): 
    'Поставщики'
    
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    phone: int | None = None
    description: str | None
    
    #receipts_suppliers: list["Receipts"] = Relationship(back_populates="suppliers")
 
    
class Storages(SQLModel, table=True): 
    'Склады'
    
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None    

    #receipts_storages: list["Receipts"] = Relationship(back_populates="storages")
    
class TypeProducts(SQLModel, table=True):
    """Ингридиенты блюда
    midle_price средняя цена 
    total всего на складе 
    weight вес одной упаковки/вес предмета в пачке
    """
        
    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column('name', String, unique=True))
    weight:      float | None = None
    item:          int | None = None
    midle_price: float | None = None 
    total:         int | None = None
    type_product: TypeProduct

    
class Receipts(SQLModel, table=True):
    "Поступление товара/сырья на склады"
    
    id: int = Field(default=None, primary_key=True)
    price_unit: int
    count: float
    dates: datetime
    
    supplier_id: int | None = Field(default=None, foreign_key="suppliers.id")
    
    storage_id: int | None = Field(default=None, foreign_key="storages.id")
    
    typeproducts_id: int | None = Field(default=None, foreign_key="typeproducts.id")
 

class SellProducts(SQLModel, table=True):
    """Таблица с отпускным товаром
    name название блюда/товара, 
    price цена, 
    description описание товара, 
    description_recip описание приготовления, 
    #налогооблажение в % соотношении
    flag_show отображение блюда на агрегаторах"""
    
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    description: str | None = None
    description_recip: str | None = None
    flag_show: bool = False
    

class Recipes(SQLModel, table=True):
    """Название тех карты
    """
    
    id: int | None = Field(default=None, primary_key=True)
    name: str # Уникальное поле
    recipes_type : str
    

class RecipeIngredient(SQLModel, table=True):  
    """Тех карта 
    Параметры, сколько спиcывать при заказе 1 блюда
    
    count - количество
    weight - вес росыпью/вес шт. на количество
    average_price средняя цена от веса/цена от количества, одбновляется после добавления тех картыХраним ингредиенты и упаковку для тех карт
    """
     
    id: int = Field(default=None, primary_key=True)
    weight: float | None = None
    count: float | None = None
    losses: float | None = None
    average_price: float | None = None 
    
    recipe_id: int  = Field(default=None, foreign_key="recipes.id")
    typeproduct_id: int = Field(default=None, foreign_key="typeproducts.id")

      
class Orders(SQLModel, table=True):
    """Храним все поступающие заказы
    
    price_dostav стоимость доставки агрегаторами или нашим курьером
    price отпускная цена в этом заказе
    """
    
    id: int = Field(default=None, primary_key=True)
    product_name: str
    count: int
    type_order: TypeOrder
    price: float
    price_dostav: float | None = None
    status: str | None = None
    flag_pakeges: bool
    