"use strict";

async function refreshApplicationStatus() {
  const label = document.getElementById("status-label");
  const labelContainer = label.closest(".status-label");

  try {
    const response = await fetch("/api/status", { headers: { Accept: "application/json" } });
    if (!response.ok) {
      throw new Error("The status endpoint returned an error.");
    }

    const status = await response.json();
    label.textContent = status.status === "operational" ? "Application operational" : "Application needs attention";
    document.getElementById("environment-value").textContent = status.environment;
    document.getElementById("version-value").textContent = status.version;
    document.getElementById("commit-value").textContent = status.commit || "local build";
    labelContainer.classList.toggle("is-error", status.status !== "operational");
  } catch (_error) {
    label.textContent = "Status unavailable";
    labelContainer.classList.add("is-error");
    document.getElementById("environment-value").textContent = "—";
    document.getElementById("version-value").textContent = "—";
    document.getElementById("commit-value").textContent = "—";
  }
}

refreshApplicationStatus();
