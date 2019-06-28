from app.views import ItemList, Item, UserLogin, UserRegister

urls = {
    '/api/items/': ItemList,
    '/api/items/<int:item_id>/': Item,
    '/api/login/': UserLogin,
    '/api/register/': UserRegister,
}
