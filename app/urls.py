from app.views import ItemList, SearchItem, Item, UserLogin, UserRegister

urls = {
    '/items/': ItemList,
    '/items/<int:item_id>/': Item,
    '/search/<string:name>': SearchItem,
    '/login/': UserLogin,
    '/register/': UserRegister,
}
