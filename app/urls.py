from app.views import ItemList, SearchItem, Item

urls = {
    '/items': ItemList,
    '/items/<int:item_id>': Item,
    '/search/<string:name>': SearchItem,
}
