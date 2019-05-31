from app.views import ItemList, SearchItem, Item, UserLogin, UserRegister

urls = {
    '/api/items/': ItemList,
    '/api/items/<int:item_id>/': Item,
    '/api/search/<string:name>': SearchItem,
    '/api/login/': UserLogin,
    '/api/register/': UserRegister,
}
