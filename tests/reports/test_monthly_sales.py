def test_monthly_sales_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/reports/monthly-sales",
        headers=auth_headers,
    )

    assert response.status_code == 200

    assert response.json() == []



def test_monthly_sales_with_orders(
    client,
    auth_headers,
    create_report_order,
    test_product,
):

    create_report_order(
        product_id=test_product["id"],
        quantity=2,
        price=100000,
    )


    response = client.get(
        "/reports/monthly-sales",
        headers=auth_headers,
    )


    assert response.status_code == 200


    data = response.json()


    assert len(data) == 1


    assert data[0]["total_orders"] == 1

    assert data[0]["revenue"] == "200000"