from app.views import ItemList, SearchItem, Item, Images

urls = {
    '/items/': ItemList,
    '/items/<int:item_id>/': Item,
    '/search/<string:name>': SearchItem,
    '/images/': Images,
}
