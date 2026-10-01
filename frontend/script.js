const COLORS = { PASS: "var(--pass)", FAIL: "var(--fail)", ERROR: "var(--fail)", SKIPPED: "gray" };

function cell(row, text) {
    const td = document.createElement("td");
    td.textContent = text;           // textContent, not innerHTML: messages come from the server
    row.appendChild(td);
    return td;
}

function render(results) {
    const body = document.getElementById("table-body");
    body.replaceChildren();

    results.forEach(r => {
        const row = document.createElement("tr");
        cell(row, r.id);
        cell(row, r.name);
        cell(row, `${r.duration}s`);

        const status = cell(row, r.status);
        status.style.color = COLORS[r.status] || "inherit";
        status.style.fontWeight = "bold";

        const details = cell(row, r.message || "-");
        if (r.screenshot) {
            const link = document.createElement("a");
            link.href = `/screenshots/${encodeURIComponent(r.screenshot)}`;
            link.target = "_blank";
            link.textContent = " [screenshot]";
            details.appendChild(link);
        }
        body.appendChild(row);
    });

    const failed = results.filter(r => r.status === "FAIL" || r.status === "ERROR").length;
    document.getElementById("metric-total").innerText = results.length;
    document.getElementById("metric-pass").innerText = results.filter(r => r.status === "PASS").length;
    document.getElementById("metric-fail").innerText = failed;
}

document.getElementById("btn-run").addEventListener("click", async function () {
    const btn = this;
    const statusLine = document.getElementById("status-line");
    const label = btn.innerText;
    btn.innerText = "Running...";
    btn.disabled = true;
    statusLine.textContent = "Running the suite (this opens Chrome and can take a minute)...";

    try {
        const response = await fetch("/run-test", { method: "POST" });
        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || `HTTP ${response.status}`);
        }
        render(await response.json());
        statusLine.textContent = `Finished at ${new Date().toLocaleTimeString()}`;
    } catch (e) {
        statusLine.textContent = `Run failed: ${e.message}`;
    } finally {
        btn.innerText = label;
        btn.disabled = false;
    }
});
