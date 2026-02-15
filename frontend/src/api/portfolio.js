export async function fetchPositions() {
    const res = await fetch("/api/portfolio/positions");
    if (!res.ok) throw new Error("Failed to fetch positions");
    return res.json();
}
