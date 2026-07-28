def test_dashboard_report_empty(client):

    response = client.get(
        "/reports/dashboard"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["users"] == 0
    assert data["products"] == 0
    assert data["categories"] == 0
    assert data["orders"] == 0

    assert data["total_revenue"] == "0"
    assert data["average_order_value"] == "0"
    
    
def test_dashboard_report_with_orders(
    client,
    create_order
):

    create_order(100000)

    create_order(200000)


    response = client.get(
        "/reports/dashboard"
    )


    assert response.status_code == 200


    data = response.json()


    assert data["orders"] == 2

    assert data["total_revenue"] == "300000"

    assert data["average_order_value"] == "150000"