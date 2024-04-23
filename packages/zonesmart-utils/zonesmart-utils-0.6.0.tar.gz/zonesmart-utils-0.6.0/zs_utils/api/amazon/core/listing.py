from zs_utils.api.amazon.base_api import AmazonAPI


class GetListingBySkuAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#get-listings2021-08-01itemsselleridsku
    """

    http_method = "GET"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = ["marketplaceIds"]
    allowed_params = [
        "issueLocale",
        "includedData",
    ]


class GetListingListAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/catalog-items-api-v2022-04-01-reference#get-catalog2022-04-01items
    """

    http_method = "GET"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = ["marketplaceIds"]
    allowed_params = [
        "identifiers",
        "identifiersType",
        "includedData",  # "[\"summaries\", \"fulfillmentAvailability\", \"offers\", \"attributes\"]"
        "locale",
        "sellerId",
        "keywords",
        "brandNames",
        "classificationIds",
        "pageSize",
        "pageToken",
        "keywordsLocale",
    ]


class PatchListingAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#patch-listings2021-08-01itemsselleridsku
    """

    http_method = "PATCH"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = [
        "marketplaceIds",
        "sku",
        "sellerId",
        "payload",
    ]
    allowed_params = [
        "includedData",
        "mode",
        "issueLocale",
        "sellerSku",
        "nextToken",
    ]


class CreateOrUpdateListingAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#put-listings2021-08-01itemsselleridsku
    """

    http_method = "PUT"
    resource_method = "listings/2021-08-01/items/{sellerId}/{sku}"
    required_params = [
        "marketplaceIds",
        "sku",
        "sellerId",
        "payload",
    ]
    allowed_params = [
        "includedData",
        "mode",
        "issueLocale",
        "sellerSku",
        "nextToken",
    ]


class GetInventoriesAPI(AmazonAPI):
    """
    Docs:
    https://developer-docs.amazon.com/sp-api/docs/fbainventory-api-v1-reference#get-fbainventoryv1summaries
    """

    http_method = "GET"
    resource_method = "fba/inventory/v1/summaries"
    required_params = [
        "marketplaceIds",
        "granularityType",
        "granularityId",
    ]
    allowed_params = [
        "details",
        "startDateTime",
        "sellerSkus",
        "sellerSku",
        "nextToken",
    ]
