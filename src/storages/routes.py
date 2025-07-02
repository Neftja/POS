from typing import Optional, List
from fastapi import APIRouter
from src.storages.schema import Suppliers, Storages, Receipts, TypeProducts, Recipes, SellProducts, Orders, TypeProduct, RecipeIngredient, TypeRecipes, TypeRecipes
from typing import List, Optional, Union
from datetime import datetime
from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemPublic, SuppliersPublic, ItemUpdate, Message, TypeProductsPublic, ReceiptsPublic, RecipesPublic, TypeRecipesPublic, RecipeIngredientPublic
from sqlmodel import select, delete
from typing import Any
from sqlmodel import func, select
from sqlalchemy import text

storages_router = APIRouter(prefix="/v1/storages", tags=['Storages (Склады)'])
suppliers_router = APIRouter(prefix="/v1/suppliers", tags=['Suppliers (Поставщики)'])
typeproducts_router = APIRouter(prefix="/v1/typeproducts", tags=['TypeProducts (Товар на складе)'])
receipts_router = APIRouter(prefix="/v1/receipts", tags=['Receipts (Поступающий товар)'])
recipes_router = APIRouter(prefix="/v1/recipes", tags=['Recipes (Тех Карта)'])

sellproducts_router = APIRouter(prefix="/v1/sellproducts", tags=['SellProducts (Карточка продаваемого товара)'])



#ПОСТАВЩИКИ DONE
# @suppliers_router.get("/all")
# async def get_all_suppliers(session: SessionDep):
#     statement = select(Suppliers)
#     results = session.exec(statement).all()
#     return results
@suppliers_router.get("/all", response_model=SuppliersPublic)
async def read_itemss(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(Suppliers)).one()
    items = session.exec(select(Suppliers).offset(skip).limit(limit)).all()
    
    return SuppliersPublic(data=items, count=count)

@suppliers_router.get("/{supplier}")
async def get_supplier(supplier: str, session: SessionDep):
    statement = select(Suppliers).where(Suppliers.name == supplier)
    results = session.exec(statement).one()
    return results

@suppliers_router.post("/{supplier}")
async def create_new_supplier(supplier: str, session: SessionDep, phone: int | None = None, description: str | None = None):
    "Добавить нового поставщика"
    query = Suppliers(name=supplier, phone=phone, description=description)
    session.add(query)
    session.commit()
    
@suppliers_router.delete("/{supplier}")
async def delete_new_supplier(supplier: str, session: SessionDep, phone: int | None = None, description: str | None = None):
    "Удалить поставщика"
    session.exec(delete(Suppliers).where(Suppliers.name == supplier))
    session.commit()





# СКЛАДЫ DONE
@storages_router.get("/all", response_model=SuppliersPublic)
async def read_items(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(Storages)).one()
    items = session.exec(select(Storages).offset(skip).limit(limit)).all()
   
    return SuppliersPublic(data=items, count=count)


@storages_router.get("/{storage}")
async def get_storage(storage: str, session: SessionDep):
    results = session.exec(select(Storages).where(Storages.name == storage)).all()
    return results

@storages_router.post("/{storage}")
async def create_new_storage(storage: str, session: SessionDep, description: str | None = None):
    "Добавить новый склад"
    session.add(Storages(name=storage, description=description))
    session.commit()
    

@storages_router.delete("/{storage}")
async def delete_storage(storage: str, session: SessionDep):
    "Удалить склад"
    session.exec(delete(Storages).where(Storages.name == storage))
    session.commit()


# НАЗВАНИЕ СЫРЬЯ DONE
@typeproducts_router.get("/all")
async def get_all_typeproduct(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(TypeProducts)).one()
    items = session.exec(select(TypeProducts).offset(skip).limit(limit)).all()
    return TypeProductsPublic(data=items, count=count)

@typeproducts_router.get("/products/all")
async def get_all_typeproduct(session: SessionDep) -> Any:
    items = session.exec(select(TypeProducts).where(TypeProducts.type_product == TypeProduct.grams and TypeProducts.type_product == TypeProduct.boxing)).all()
    return TypeProductsPublic(data=items, count=0)

@typeproducts_router.get("/packagess")
async def get_all_typeproduct(session: SessionDep) -> Any:
    items = session.exec(select(TypeProducts.id, TypeProducts.name).where(TypeProducts.type_product == TypeProduct.package)).all()
    return TypeProductsPublic(data=items, count=0)

@typeproducts_router.get("/packages")
async def get_all_typeproduct(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(TypeProducts).where(TypeProducts.type_product == TypeProduct.package)).one()
    items = session.exec(select(TypeProducts).where(TypeProducts.type_product == TypeProduct.package).offset(skip).limit(limit)).all()
    return TypeProductsPublic(data=items, count=count)

@typeproducts_router.get("/products")
async def get_all_typeproduct(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(TypeProducts).where(TypeProducts.type_product == TypeProduct.product)).one()
    items = session.exec(select(TypeProducts).where(TypeProducts.type_product == TypeProduct.product).offset(skip).limit(limit)).all()
    return TypeProductsPublic(data=items, count=count)

@typeproducts_router.get("/water")
async def get_all_typeproduct(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(TypeProducts).where(TypeProducts.type_product == TypeProduct.water)).one()
    items = session.exec(select(TypeProducts).where(TypeProducts.type_product == TypeProduct.water).offset(skip).limit(limit)).all()
    return TypeProductsPublic(data=items, count=count)

@typeproducts_router.post("/{name}")
async def add_new_typeproduct(name: str, type_product: TypeProduct, session: SessionDep, item: int | None = None, weight: float | None = None):
    """Добавить новый ингридиент(сырье)
    Если товар имеет упаковку с штучным товаром, то при добавлении указываем вес одного предмета в упаковке
    """
    if type_product == TypeProduct.boxing:
        query = TypeProducts(name=name, type_product=type_product, item=item, weight=weight)
           
    elif type_product == TypeProduct.grams:
        query = TypeProducts(name=name, type_product=type_product)
    
    elif type_product == TypeProduct.package:
        query = TypeProducts(name=name, type_product=type_product, item=item)
        
    elif type_product == TypeProduct.product:
        query = TypeProducts(name=name, type_product=type_product, item=item)

    elif type_product == TypeProduct.water:
        query = TypeProducts(name=name, type_product=type_product, item=item)
        
    session.add(query)
    session.commit()

    
@typeproducts_router.get("/{name}")
async def get_typeproduct(name: str, session: SessionDep):
    results = session.exec(select(TypeProducts).where(TypeProducts.name == name)).one()
    return results

@typeproducts_router.delete("/{name}")
async def del_typeproduct(name: str, session: SessionDep):

    results = session.exec(select(TypeProducts).where(TypeProducts.name == name)).one()
    
    session.exec(delete(Receipts).where(Receipts.typeproducts_id == results.id))
    session.delete(results)
    session.commit()

@typeproducts_router.delete("/{package}")
async def del_package(package: str, session: SessionDep):
    "Удалить упаковку во всех таблицах"
    results = session.exec(select(TypeProducts).where(TypeProducts.name == package)).one()
    
    session.exec(delete(Receipts).where(Receipts.typeproducts_id == results.id))
    qq  = session.exec(select(RecipeIngredient).where(RecipeIngredient.typeproduct_id == results.id))
    session.delete(results)
    session.delete(qq)
    session.commit()


# РАБОТА С ПОСИУПАЮЩИМ СЫРЬЕМ НА СКЛАДЫ ОТ ПОСТАВЩИКОВ EDIT?
@receipts_router.get("/all")
async def get_all_receipts(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    #count = session.exec(select(func.count()).select_from(Receipts)).one()
    #items = session.exec(select(Receipts.dates, Receipts.count, TypeProducts.name).join(TypeProducts).where(TypeProducts.id == Receipts.typeproducts_id).offset(skip).limit(limit)).all()
    res = []
    item = session.exec(text("""SELECT id, count, dates,
                            (SELECT Storages.name FROM Storages WHERE Storages.id = Receipts.storage_id) as name_storage,
                            (SELECT TypeProducts.name FROM TypeProducts WHERE TypeProducts.id = Receipts.typeproducts_id) as name_typeproducts,
                            (SELECT Suppliers.name FROM Suppliers WHERE Suppliers.id = Receipts.supplier_id) as name_suppliers
                        FROM Receipts
                        ORDER BY id DESC"""))
    rr = {}
    for row in item:
        rr['id'] = row[0]
        rr['count'] = row[1]
        rr['dates'] = row[2]
        rr['storage'] = row[3]
        rr['name'] = row[4]
        rr['supplier'] = row[5]
        res.append(rr)
        rr = {}
    return ReceiptsPublic(data=res, count=100)


@receipts_router.post("/add/{name}") # НУЖНО ЛОГИ НА ОШИБКУ
async def add_receipt(name: str, price_unit: int, count: float, storage: str, supplier: str, session: SessionDep):
    """Добавить на склад поступивший typeproduct(сырье)"""
    
    dates = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    results_i = session.exec(select(TypeProducts).where(TypeProducts.name == name)).one()
    results_s = session.exec(select(Storages).where(Storages.name == storage)).one()
    results_su = session.exec(select(Suppliers).where(Suppliers.name == supplier)).one()
        
    if results_i.type_product == TypeProduct.package:
        query = Receipts(price_unit=price_unit, count=results_i.item * count, dates=dates, typeproducts_id=results_i.id, storage_id=results_s.id, supplier_id=results_su.id)
   
    else: 
        query = Receipts(price_unit=price_unit, count=count, dates=dates, typeproducts_id=results_i.id, storage_id=results_s.id, supplier_id=results_su.id)
    
    session.add(query)
    session.commit()

@receipts_router.delete("/{id}")
async def del_receipt(id: int, session: SessionDep):
    session.exec(delete(Receipts).where(Receipts.id == id))
    session.commit()
    


# СОЗДАНИЕ ТОВАРА/БЛЮДА #DONE
@sellproducts_router.get("/all")
async def get_all_sellproducts(session: SessionDep):
    results = session.exec(select(SellProducts.name)).all()
    return results

@sellproducts_router.post("/{product}")
async def create_new_product(product: str, price: str, session: SessionDep, description: str | None = None, description_recip: str | None = None):
    """Создаем новое блюдо или товар"""
    
    query = SellProducts(name=product, price=price, description=description, description_recip=description_recip)
    session.add(query)
    session.commit()

@sellproducts_router.delete("/{product}")
async def del_product(product: str, session: SessionDep):
    session.exec(delete(Recipes).where(Recipes.name == product))
    session.exec(delete(SellProducts).where(SellProducts.name == product))
    session.commit()


    
    
    
# ТЕХ КАРТА EDIT?
@recipes_router.get("/all")
async def get_all_recipes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(Recipes)).one()
    items = session.exec(select(Recipes).offset(skip).limit(limit)).all()
    return RecipesPublic(data=items, count=count)

@recipes_router.get("/type_recipes")
async def get_all_recipes(session: SessionDep) -> Any:
    items = session.exec(select(TypeRecipes)).all()
    return TypeRecipesPublic(data=items)

@recipes_router.get("/{id_recipes}/packages")
async def get_all_recipes(id_recipes: int, session: SessionDep):
    res = []
    items = session.exec(select(TypeProducts.name, RecipeIngredient.count, RecipeIngredient.id).join(TypeProducts).where(RecipeIngredient.recipe_id == id_recipes and RecipeIngredient.typeproduct_id == TypeProducts.id)).all()
    r = {}
    for row in items:
        r['name'] = row[0]
        r['count'] = int(row[1])
        r['id'] = row[2]
        res.append(r)
        r = {}
    return RecipeIngredientPublic(data=res)

@recipes_router.post("/{recipe}")
async def create_new_recipe(recipe: str, recipes_type: str, session: SessionDep):
    session.add(Recipes(name=recipe, recipes_type=recipes_type))
    session.commit()
    

@recipes_router.get("/{id_recipe}/all")
async def get_ingredient_recipe(id_recipe: int, session: SessionDep):
    """Получить ингредиенты тех карты"""
    
    recip = session.exec(select(Recipes).where(Recipes.id == id_recipe)).one()
    items = session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == recip.id)).all()
    return RecipeIngredientPublic(data=items)
    
    
@recipes_router.post("/{recipe}/ingredient={ingredient}")
async def add_ingredient_recipe(recipe: int, name_ingredient: str, session: SessionDep, losses: float | None = None,  weight: float | None = 0, count: float | None = 0):
    """добавить ингредиент в тех карту"""
      
    product = session.exec(select(TypeProducts).where(TypeProducts.name == name_ingredient and (TypeProducts.type_product == TypeProduct.grams or TypeProducts.type_product == TypeProduct.boxing))).one()
    
    if product.type_product == TypeProduct.grams:
        query = RecipeIngredient(recipe_id=recipe, weight=weight, losses=losses, typeproduct_id=product.id, typeproduct=product.type_product)
    
    elif product.type_product == TypeProduct.boxing:
        query = RecipeIngredient(recipe_id=recipe, count=count, weight=product.weight, losses=losses, typeproduct_id=product.id, typeproduct=product.type_product)
    
    session.add(query)
    session.commit()
 
@recipes_router.post("/{recipe}/packege={packege}")
async def add_packege_recipe(recipe: int, packege: str, count: int, session: SessionDep):
    """добавить упаковку в тех карту"""
    
    #recip = session.exec(select(Recipes).where(Recipes.id == recipe)).one()
    product = session.exec(select(TypeProducts).where(TypeProducts.name == packege)).one()
    session.add(RecipeIngredient(recipe_id=recipe, count=count, typeproduct_id=product.id))
    session.commit()

@recipes_router.delete("/{recipe}")
async def delete_recipe(recipe: str, session: SessionDep):
    recip = session.exec(select(Recipes).where(Recipes.name == recipe)).one()
    
    session.exec(delete(Recipes).where(Recipes.name == recipe))
    session.exec(delete(RecipeIngredient).where(RecipeIngredient.recipe_id == recip.id))
    session.commit()

