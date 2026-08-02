import pytest


# ==================================================
# PAYMENT SUMMARY REPORT
# ==================================================


def test_payment_summary_report(
    client,
    admin_token,
):
    response = client.get(
        "/reports/payment-summary",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_transactions" in data
    assert "total_revenue" in data
    assert "methods" in data

    assert isinstance(
        data["methods"],
        list
    )


# ==================================================
# PAYMENT METHODS VALIDATION
# ==================================================


def test_payment_methods_structure(
    client,
    admin_token,
):
    response = client.get(
        "/reports/payment-summary",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    methods = response.json()["methods"]

    for method in methods:

        assert "method" in method
        assert "transactions" in method
        assert "revenue" in method
        assert "percentage" in method


# ==================================================
# PAYMENT SUMMARY CALCULATION
# ==================================================


def test_payment_percentage_total(
    client,
    admin_token,
    create_report_order,
    test_product,
):

    create_report_order(
        product_id=test_product["id"],
        quantity=1,
        price=100
    )

    response = client.get(
        "/reports/payment-summary",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    methods = response.json()["methods"]

    percentage = sum(
        item["percentage"]
        for item in methods
    )

    assert round(
        percentage
    ) == 100