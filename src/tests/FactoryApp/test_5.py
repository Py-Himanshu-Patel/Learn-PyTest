import pytest


@pytest.mark.parametrize(
    "title, category, description, slug, regular_price, discount_price, validity",
    [
        ("Netflix", 3, "New Series", "", 50.99, 45.99, 400),
        ("Netflix", 3, "New Series", "netflix", "", 45.99, 400),
    ]
)
@pytest.mark.django_db
def test_product_instance(
    client,		# client to make request
    title,
    category,
    description,
    slug,
    regular_price,
    discount_price,
    validity
):
    response = client.post(
        '/api/product/',
        data = {
            'title': title,
            'category': category,
            'description': description,
            'slug': slug,
            'regular_price': regular_price,
            'discount_price': discount_price,
        }
    )

    print(response.status_code)
    print(response.data)

    assert response.status_code == validity
