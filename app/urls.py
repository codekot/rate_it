from app.views import ItemList, Item, UserLogin, UserRegister, UserProfile

urls = {
    '/api/items/': ItemList,
    '/api/items/<int:item_id>/': Item,
    '/api/login/': UserLogin,
    '/api/register/': UserRegister,
    '/api/profile/': UserProfile,
}
