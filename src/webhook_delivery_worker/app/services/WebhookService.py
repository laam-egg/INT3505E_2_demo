from pymongo.collection import Collection

class WebhookService:
    """
    Currently manages webhook deletion only.
    """

    def __init__(self, collection: Collection):
        self.collection = collection

    def delete_item_by_id(self, id: str) -> None:
        """
        Deletes a webhook by its ID.
        """
        self.collection.delete_one({"id": id})
    
    def get_collection_by_eventName_and_targetUrl(
        self,
        eventName: str | None,
        targetUrls: list[str] | None,
        page: int,
        size: int,
    ):
        """
        Retrieves a paginated list of webhooks,
        optionally filter by eventName and/or targetUrls.
        """
        q = {}
        if eventName:
            q['eventName'] = eventName
        if targetUrls and len(targetUrls) > 0:
            q['targetUrl'] = { '$in': targetUrls }

        skip = (page - 1) * size
        limit = size

        return [
            *self.collection.find(
                q
            ).skip(skip).limit(limit)
        ]
