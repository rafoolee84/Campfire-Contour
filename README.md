# Campfire-Contour
## Northroom checkout pricing (server-side)

`/approve_cart` and `/approve_product` ignore any client-sent price. Unit prices, titles and the
price-matched flag come from `northroom_prices.json`, generated from the live storefront catalog:

    node tools/gen_prices.js            # fetches https://www.northroomhome.com/products.js + prices.js

Unknown or unpublished SKUs are rejected. Re-run the generator and deploy whenever storefront
prices or the published catalog change. Free US shipping at $50+ (else $5.99) and "no promo codes
on carts with price-matched items" (NORTH15 no-stack) are unchanged.
