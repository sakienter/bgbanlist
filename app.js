(() => {
  "use strict";

  const rows = Array.isArray(window.BG_BAN_ROWS) ? window.BG_BAN_ROWS : [];
  const tbody = document.getElementById("tbody");
  const query = document.getElementById("q");
  const type = document.getElementById("type");
  const status = document.getElementById("status");
  const summary = document.getElementById("summary");

  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);

  const fillSelect = (element, key) => {
    [...new Set(rows.map((row) => row[key]).filter(Boolean))]
      .sort((a, b) => a.localeCompare(b, "ja"))
      .forEach((value) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        element.appendChild(option);
      });
  };

  const render = () => {
    const needle = query.value.trim().toLowerCase();
    const filtered = rows.filter((row) => {
      const haystack = Object.values(row).join(" ").toLowerCase();
      return (!needle || haystack.includes(needle))
        && (!type.value || row.restriction === type.value)
        && (!status.value || row.status === status.value);
    });

    summary.textContent = `${filtered.length} / ${rows.length} 件　異常 ${new Set(filtered.map((row) => row.anomaly)).size} 種　対象 ${new Set(filtered.map((row) => row.target)).size} 種`;
    tbody.innerHTML = filtered.map((row) => `
      <tr>
        <td>${escapeHtml(row.section)}</td>
        <td>${escapeHtml(row.anomaly)}</td>
        <td>${escapeHtml(row.restriction)}</td>
        <td>${escapeHtml(row.target)}</td>
        <td><span class="status ${row.status.includes("旧") ? "old" : ""}">${escapeHtml(row.status)}</span></td>
        <td class="note">${escapeHtml(row.note)}</td>
      </tr>`).join("");
  };

  fillSelect(type, "restriction");
  fillSelect(status, "status");
  [query, type, status].forEach((element) => element.addEventListener("input", render));
  render();
})();
