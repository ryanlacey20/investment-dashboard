export default function SummaryCard({ title, value, color }) {
    return (
        <div style={{
            background: "white",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0 4px 10px rgba(0,0,0,0.05)"
        }}>
            <h3>{title}</h3>
            <p style={{ color: color || "black", fontSize: "20px" }}>{value}</p>
        </div>
    );
}
