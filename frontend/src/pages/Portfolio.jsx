import React, { useEffect, useState } from "react";
import { fetchPositions } from "../api/portfolio";
import SummaryCard from "../components/SummaryCard";
import PositionsTable from "../components/PositionsTable";

export default function Portfolio() {
    const [positions, setPositions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchPositions()
            .then(setPositions)
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <div style={{ padding: 50, textAlign: "center" }}>Loading portfolio...</div>;
    if (error) return <div style={{ padding: 50, textAlign: "center", color: "red" }}>Error: {error}</div>;

    const totalValue = positions.reduce((sum, p) => sum + (p.marketValue || 0), 0);
    const totalCost = positions.reduce((sum, p) => sum + (p.quantity * p.averagePrice || 0), 0);
    const totalPnL = totalValue - totalCost;

    return (
        <div style={{ padding: 40, fontFamily: "Arial, sans-serif" }}>
            <h1>Portfolio Summary</h1>

            <div style={{ display: "flex", gap: 20, marginBottom: 30 }}>
                <SummaryCard title="Total Value" value={`$${totalValue.toLocaleString()}`} />
                <SummaryCard title="Total P/L" value={`$${totalPnL.toLocaleString()}`} color={totalPnL >= 0 ? "green" : "red"} />
                <SummaryCard title="Positions" value={positions.length} />
            </div>

            <PositionsTable positions={positions} />
        </div>
    );
}
