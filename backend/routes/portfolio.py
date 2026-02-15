from flask import Blueprint, jsonify
from services.schwab_client import SchwabClient

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/api/portfolio")


@portfolio_bp.route("/positions")
def positions():
    try:
        client = SchwabClient()
        accounts = client.get_positions()   # This is already a list

        output = []

        for account in accounts:
            securities = account.get("securitiesAccount", {})
            positions = securities.get("positions", [])

            for position in positions:
                instrument = position.get("instrument", {})

                output.append({
                    "symbol": instrument.get("symbol"),
                    "assetType": instrument.get("assetType"),
                    "quantity": position.get("longQuantity", 0),
                    "marketValue": position.get("marketValue"),
                    "averagePrice": position.get("averagePrice")
                })

        return jsonify(output)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
