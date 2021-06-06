import pytest
from apps.FactoryApp.models import Product


@pytest.mark.parametrize(
    "title, category, description, slug, regular_price, discount_price, validity",
    [
        ("NewProduct1", 1, "NewDesc", "slug", 2.99, 5.99, True),
        ("", 1, "NewDesc", "slug", 2.99, 5.99, True),
        # ("NewProduct3", 0, "NewDesc", "slug", 2.99, 5.99, False),      # can't test as None can't be given in Foreign Key
        ("NewProduct4", 1, "", "slug", 2.99, 5.99, True),
        ("NewProduct5", 1, "NewDesc", "", 2.34, 5.99, True),
        # ("NewProduct6", 1, "NewDesc", "slug", 2.99, 0, False)            # Can't give none in float field
    ]
)
def test_product_instance(
    db,						# to access database
    product_factory,		# to access factory
    title,
    category,
    description,
    slug,
    regular_price,
    discount_price,
    validity
):
    test = product_factory(
        title=title,
        category_id=category,
        description=description,
        slug=slug,
        regular_price=regular_price,
        discount_price=discount_price,
    )

    item = Product.objects.count()
    print(item)         # 1
    assert item == validity
