from datetime import datetime


def test_yearly_sales_empty(
    client,
    auth_headers,
):
    """
    Test yearly sales report when there are no orders.
    """

    current_year = datetime.now().year

    response = client.get(
        f"/reports/yearly-sales?year={current_year}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["year"] == current_year
    assert data["total_orders"] == 0
    assert data["total_revenue"] == "0"
    assert data["monthly_sales"] == []


def test_yearly_sales_with_orders(
    client,
    auth_headers,
    create_report_order,
    test_product,
):
    """
    Test yearly sales report with existing orders.
    """

    current_year = datetime.now().year

    create_report_order(
        product_id=test_product["id"],
        quantity=2,
        price=100000,
    )

    response = client.get(
        f"/reports/yearly-sales?year={current_year}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["year"] == current_year
    assert data["total_orders"] == 1
    assert data["total_revenue"] == "200000"

    assert len(data["monthly_sales"]) == 1

    monthly = data["monthly_sales"][0]

    assert 1 <= monthly["month"] <= 12
    assert monthly["total_orders"] == 1
    assert monthly["revenue"] == "200000"


def test_yearly_sales_requires_auth(
    client,
):
    """
    Test yearly sales endpoint authentication requirement.
    """

    current_year = datetime.now().year

    response = client.get(
        f"/reports/yearly-sales?year={current_year}",
    )

    assert response.status_code == 401


def test_yearly_sales_invalid_year(
    client,
    auth_headers,
):
    """
    Test yearly sales report with invalid year input.
    """

    response = client.get(
        "/reports/yearly-sales?year=0",
        headers=auth_headers,
    )

    assert response.status_code in [400, 422]