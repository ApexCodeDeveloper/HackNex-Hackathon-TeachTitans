// NyayVeritas Reactive Client Controller
document.addEventListener("DOMContentLoaded", () => {
  // Navigation Tabs
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add("active");
      if (btn.dataset.tab === "eval-tab") loadEvaluationData();
    });
  });

  // Sub-tabs (Evidence Ledger vs Confidence Report)
  const subTabBtns = document.querySelectorAll(".sub-tab-btn");
  const ledgerView = document.getElementById("ledger-view");
  const confidenceView = document.getElementById("confidence-view");

  subTabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      subTabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      if (btn.dataset.subtab === "ledger") {
        ledgerView.style.display = "block";
        confidenceView.style.display = "none";
      } else {
        ledgerView.style.display = "none";
        confidenceView.style.display = "block";
      }
    });
  });

  // Drawer Close
  const closeDrawerBtn = document.getElementById("drawer-close-btn");
  const drawer = document.getElementById("inspector-drawer");
  if (closeDrawerBtn) {
    closeDrawerBtn.addEventListener("click", () => {
      drawer.classList.remove("open");
    });
  }

  // Drafting Action
  const btnRunDraft = document.getElementById("btn-run-draft");
  const btnRunBaseline = document.getElementById("btn-run-baseline");
  const promptInput = document.getElementById("draft-prompt-input");
  const docTypeSelect = document.getElementById("doc-type-select");
  const draftViewer = document.getElementById("draft-viewer");
  const ledgerList = document.getElementById("ledger-list");
  const gaugeVal = document.getElementById("confidence-gauge-val");
  const contradictionsContainer = document.getElementById("contradictions-container");
  const missingContainer = document.getElementById("missing-fields-container");
  const gateStatusDot = document.getElementById("gate-status-dot");
  const gateStatusText = document.getElementById("gate-status-text");

  async function executeDraft(isBaseline = false) {
    const task = promptInput.value.trim() || "Draft regular bail application for Rajesh Sharma citing health conditions and seizure status";
    const docType = docTypeSelect.value;

    draftViewer.innerHTML = `<div style="text-align: center; padding: 3rem; color: var(--gold-light);">
      <div style="font-size: 2rem; margin-bottom: 1rem;">⚖️</div>
      <p>Orchestrating agents & verifying against closed-world registry...</p>
    </div>`;

    try {
      const resp = await fetch("/api/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          task_prompt: task,
          document_type: docType,
          run_baseline: isBaseline
        })
      });
      const data = await resp.json();

      // Render Draft
      if (isBaseline) {
        draftViewer.innerHTML = `<div style="border-left: 3px solid #ef4444; padding-left: 1rem; margin-bottom: 1rem; color: #fca5a5;">
          <strong>[BASELINE RAG OUTPUT]</strong> No Source Registry, No Claim Verifier, No Repair Loop.
        </div>` + (data.rendered_html || `<pre>${data.draft_text}</pre>`);
      } else {
        draftViewer.innerHTML = data.draft_with_html_anchors || `<pre>${data.draft_text}</pre>`;
      }

      // Attach Click Handlers to rendered badges
      attachBadgeListeners();

      // Render Ledger
      renderLedger(data.verification_ledger);

      // Render Confidence & Gaps
      if (data.confidence_report) {
        renderConfidenceReport(data.confidence_report);
      }

      // Render Gate
      if (data.fabrication_gate && gateStatusDot && gateStatusText) {
        gateStatusText.textContent = data.fabrication_gate.passed ? "PASSED (0 Violations)" : "FAILED (Violations)";
        gateStatusDot.className = data.fabrication_gate.passed ? "chip-dot green" : "chip-dot crimson";
      }

    } catch (err) {
      draftViewer.innerHTML = `<p style="color: var(--crimson-violation);">Execution error: ${err.message}</p>`;
    }
  }

  if (btnRunDraft) btnRunDraft.addEventListener("click", () => executeDraft(false));
  if (btnRunBaseline) btnRunBaseline.addEventListener("click", () => executeDraft(true));

  // Render Ledger
  function renderLedger(ledger) {
    if (!ledger || !ledger.claims) {
      ledgerList.innerHTML = "<p style='color: var(--text-dim);'>No atomic claims extracted.</p>";
      return;
    }

    let html = `<div style="margin-bottom: 1rem; font-size: 0.85rem; color: var(--text-muted);">
      Groundedness: <strong style="color: var(--emerald-verified);">${ledger.overall_groundedness_pct}%</strong> | 
      Fabrications: <strong style="color: ${ledger.fabrication_count === 0 ? 'var(--emerald-verified)' : 'var(--crimson-violation)'};">${ledger.fabrication_count}</strong> |
      Supported: ${ledger.supported_count} | Partial: ${ledger.partial_count} | Unsupported: ${ledger.unsupported_count}
    </div>`;

    ledger.claims.forEach(c => {
      const spans = (c.found_quote_spans && c.found_quote_spans.length > 0) 
        ? `<div class="claim-quote-box">"${c.found_quote_spans[0]}"</div>` 
        : "";

      html += `
        <div class="claim-card status-${c.status}">
          <div class="claim-card-header">
            <span class="claim-id">${c.claim_id}</span>
            <span class="verdict-tag ${c.status}">${c.status}</span>
          </div>
          <div class="claim-text">${c.sentence_text}</div>
          ${spans}
          <div class="claim-expl">🔍 ${c.entailment_explanation}</div>
        </div>
      `;
    });

    ledgerList.innerHTML = html;
  }

  // Render Confidence Report
  function renderConfidenceReport(rep) {
    if (!gaugeVal) return;
    gaugeVal.textContent = `${Math.round(rep.overall_confidence * 100)}%`;

    // Contradictions
    if (rep.contradictions && rep.contradictions.length > 0) {
      let cHtml = "";
      rep.contradictions.forEach(ct => {
        cHtml += `
          <div class="contradiction-alert-box">
            <div class="contradiction-header">⚠️ CONTRADICTION: ${ct.field_name}</div>
            <p style="font-size: 0.85rem; margin-bottom: 0.5rem; color: #fecaca;">${ct.explanation}</p>
            <div style="font-size: 0.78rem; color: var(--text-muted);">
              <strong>${ct.doc_a}:</strong> "${ct.quote_a}"<br/>
              <strong>${ct.doc_b}:</strong> "${ct.quote_b}"
            </div>
          </div>
        `;
      });
      contradictionsContainer.innerHTML = cHtml;
    } else {
      contradictionsContainer.innerHTML = `<p style="font-size: 0.85rem; color: var(--emerald-verified);">✓ No cross-document contradictions detected in retrieved set.</p>`;
    }

    // Missing fields
    if (rep.missing_fields && rep.missing_fields.length > 0) {
      let mHtml = "";
      rep.missing_fields.forEach(m => {
        mHtml += `
          <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 0.75rem; border-radius: var(--radius-sm); margin-bottom: 0.5rem;">
            <div style="font-size: 0.82rem; font-weight: 600; color: #fca5a5;">● ${m.field_name} (${m.status})</div>
            <div style="font-size: 0.76rem; color: var(--text-dim);">${m.legal_significance}</div>
          </div>
        `;
      });
      missingContainer.innerHTML = mHtml;
    } else {
      missingContainer.innerHTML = `<p style="font-size: 0.85rem; color: var(--emerald-verified);">✓ All critical procedural parameters accounted for.</p>`;
    }
  }

  // Badge Click Listener
  function attachBadgeListeners() {
    document.querySelectorAll(".src-badge").forEach(badge => {
      badge.addEventListener("click", async () => {
        const chunkId = badge.dataset.chunkId;
        openChunkDrawer(chunkId);
      });
    });

    document.querySelectorAll(".auth-badge").forEach(badge => {
      badge.addEventListener("click", async () => {
        const authId = badge.dataset.authId;
        openAuthDrawer(authId);
      });
    });
  }

  async function openChunkDrawer(chunkId) {
    const drawerTitle = document.getElementById("drawer-title");
    const drawerBody = document.getElementById("drawer-body");
    drawerTitle.textContent = `Source Chunk Provenance`;
    drawerBody.innerHTML = "<p>Loading source chunk...</p>";
    drawer.classList.add("open");

    try {
      const resp = await fetch(`/api/chunk/${chunkId}`);
      const ch = await resp.json();
      drawerBody.innerHTML = `
        <span class="provenance-tag-pill">${ch.chunk_id}</span>
        <div style="margin-bottom: 1rem; font-size: 0.82rem; color: var(--text-dim);">
          Document: <strong>${ch.provenance.doc_id}</strong> (${ch.provenance.doc_type})<br/>
          Line Range: ${ch.provenance.line_start} - ${ch.provenance.line_end}<br/>
          Section Hierarchy: ${ch.provenance.legal_hierarchy || 'N/A'}
        </div>
        <div style="background: rgba(0,0,0,0.4); border-left: 3px solid var(--cyan-accent); padding: 1rem; border-radius: var(--radius-sm); color: #e2e8f0; font-size: 0.9rem; white-space: pre-wrap;">
          ${ch.text}
        </div>
      `;
    } catch (e) {
      drawerBody.innerHTML = `<p style="color: var(--crimson-violation);">Failed to load chunk.</p>`;
    }
  }

  async function openAuthDrawer(authId) {
    const drawerTitle = document.getElementById("drawer-title");
    const drawerBody = document.getElementById("drawer-body");
    drawerTitle.textContent = `Canonical Legal Authority`;
    drawerBody.innerHTML = "<p>Loading authority...</p>";
    drawer.classList.add("open");

    try {
      const resp = await fetch(`/api/authority/${authId}`);
      const a = await resp.json();
      drawerBody.innerHTML = `
        <span class="provenance-tag-pill" style="background: rgba(212,175,55,0.15); color: var(--gold-light);">${a.registry_id}</span>
        <h3 style="color: var(--gold-light); font-size: 1.1rem; margin-bottom: 0.5rem;">${a.title}</h3>
        <div style="margin-bottom: 1rem; font-size: 0.82rem; color: var(--text-dim);">
          Citation: <strong>${a.citation_string}</strong><br/>
          Court / Legislature: ${a.court_or_legislature} (${a.year})<br/>
          Corpus Grounding: <strong style="color: var(--emerald-verified);">VERIFIED CLOSED-WORLD SOURCE</strong>
        </div>
        <div style="background: rgba(0,0,0,0.4); border-left: 3px solid var(--gold-primary); padding: 1rem; border-radius: var(--radius-sm); color: #e2e8f0; font-size: 0.9rem; white-space: pre-wrap;">
          ${a.canonical_text_snippet}
        </div>
      `;
    } catch (e) {
      drawerBody.innerHTML = `<p style="color: var(--crimson-violation);">Failed to load authority.</p>`;
    }
  }

  // Chat Interface
  const chatInput = document.getElementById("chat-input");
  const btnChatSend = document.getElementById("btn-chat-send");
  const chatMessages = document.getElementById("chat-messages");

  async function sendChatMessage() {
    const query = chatInput.value.trim();
    if (!query) return;

    // Append user message
    appendChatBubble("user", query);
    chatInput.value = "";

    try {
      const resp = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
      });
      const data = await resp.json();
      appendChatBubble("assistant", data.reply, data.is_refusal, data.citations);
    } catch (e) {
      appendChatBubble("assistant", "Chat service error.", true);
    }
  }

  function appendChatBubble(role, text, isRefusal = false, citations = []) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${role} ${isRefusal ? 'refusal' : ''}`;
    let citHtml = "";
    if (citations && citations.length > 0) {
      citHtml = `<div style="margin-top: 0.5rem; display: flex; gap: 0.4rem; flex-wrap: wrap;">` +
        citations.map(c => `<span class="src-badge">📄 ${c}</span>`).join("") +
        `</div>`;
    }
    bubble.innerHTML = text + citHtml;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  if (btnChatSend) btnChatSend.addEventListener("click", sendChatMessage);
  if (chatInput) {
    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") sendChatMessage();
    });
  }

  // Unseen Document Ingestion
  const btnIngestUnseen = document.getElementById("btn-ingest-unseen");
  const unseenTextInput = document.getElementById("unseen-text-input");
  const unseenTaskInput = document.getElementById("unseen-task-input");
  const unseenResultBox = document.getElementById("unseen-result-box");

  if (btnIngestUnseen) {
    btnIngestUnseen.addEventListener("click", async () => {
      const text = unseenTextInput.value.trim();
      const task = unseenTaskInput.value.trim() || "Draft regular bail application";
      if (!text) {
        alert("Please paste document text to ingest.");
        return;
      }
      unseenResultBox.innerHTML = "<p style='color: var(--gold-light);'>Ingesting unseen record into pipeline...</p>";

      try {
        const resp = await fetch("/api/unseen", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, task_prompt: task })
        });
        const d = await resp.json();
        unseenResultBox.innerHTML = `
          <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid var(--emerald-verified); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1rem;">
            <strong>✓ Successfully Ingested Unseen File:</strong> ${d.doc_id} (${d.chunks_indexed} structural chunks indexed)
          </div>
          <div class="draft-viewer-container">${d.draft_output.draft_with_html_anchors}</div>
        `;
        attachBadgeListeners();
      } catch (e) {
        unseenResultBox.innerHTML = `<p style="color: var(--crimson-violation);">Ingestion failed: ${e.message}</p>`;
      }
    });
  }

  // Load Evaluation Dashboard
  async function loadEvaluationData() {
    const tableBody = document.getElementById("ablation-table-body");
    try {
      const resp = await fetch("/api/eval");
      const data = await resp.json();
      if (data && data.ablation_table) {
        let rows = "";
        data.ablation_table.forEach(r => {
          rows += `
            <tr>
              <td><strong>${r.step}</strong></td>
              <td style="color: ${r.groundedness_pct >= 90 ? 'var(--emerald-verified)' : 'var(--amber-warning)'}; font-weight: 700;">${r.groundedness_pct}%</td>
              <td style="color: ${r.fabrication_count === 0 ? 'var(--emerald-verified)' : 'var(--crimson-violation)'}; font-weight: 700;">${r.fabrication_count}</td>
              <td>${r.recall_at_8}</td>
              <td>${r.abstention_acc_pct}%</td>
              <td>${r.latency_ms} ms</td>
              <td style="font-size: 0.8rem; color: var(--text-dim);">${r.notes}</td>
            </tr>
          `;
        });
        tableBody.innerHTML = rows;
      }
    } catch (e) {
      console.error("Failed to load eval data:", e);
    }
  }

  // Initial trigger
  attachBadgeListeners();
  initLLMConfiguration();

  // LLM API Key & Model Configuration
  function initLLMConfiguration() {
    const modal = document.getElementById("llm-modal");
    const openBtn = document.getElementById("btn-open-llm-modal");
    const closeBtn = document.getElementById("llm-modal-close");
    const cancelBtn = document.getElementById("btn-cancel-llm-modal");
    const saveBtn = document.getElementById("btn-save-llm-modal");
    const providerSelect = document.getElementById("llm-provider-select");
    const apiKeyGroup = document.getElementById("api-key-group");
    const apiKeyInput = document.getElementById("api-key-input");
    const apiKeyLabel = document.getElementById("api-key-label");
    const keyStatusHint = document.getElementById("key-status-hint");
    const ollamaGroup = document.getElementById("ollama-url-group");
    const ollamaInput = document.getElementById("ollama-url-input");
    const docsBox = document.getElementById("llm-provider-docs");
    const statusText = document.getElementById("llm-status-text");
    const statusDot = document.getElementById("llm-status-dot");
    const toggleKeyVisibility = document.getElementById("btn-toggle-key-visibility");

    const providerDocs = {
      offline: "⚡ <strong>Offline Deterministic Engine:</strong> Operates 100% locally with zero cloud dependencies and zero cost. Adheres strictly to the closed-world statutory corpus.",
      gemini: "🤖 <strong>Google Gemini:</strong> Uses <code>gemini-1.5-flash</code>. You can obtain a free API key at <a href='https://aistudio.google.com/' target='_blank' style='color:var(--cyan-accent);'>Google AI Studio</a>. Set temperature=0.0 with full citation enforcement.",
      openai: "🧠 <strong>OpenAI:</strong> Uses <code>gpt-4o</code>. Provide your OpenAI API key from <a href='https://platform.openai.com/api-keys' target='_blank' style='color:var(--cyan-accent);'>OpenAI Platform</a>.",
      anthropic: "📜 <strong>Anthropic Claude:</strong> Uses <code>claude-3-5-sonnet</code>. Provide your API key from <a href='https://console.anthropic.com/' target='_blank' style='color:var(--cyan-accent);'>Anthropic Console</a>.",
      ollama: "🖥️ <strong>Local Ollama:</strong> Connects to your local Ollama daemon (e.g. <code>ollama run llama3.1</code>) at <code>http://localhost:11434</code>."
    };

    let cachedConfig = {};

    async function loadConfig() {
      try {
        const resp = await fetch("/api/config/llm");
        const data = await resp.json();
        cachedConfig = data;

        if (statusText) statusText.innerText = "LLM: " + data.active_provider_label;
        if (statusDot) {
          statusDot.className = "chip-dot " + (data.cloud_enabled ? "green" : "cyan");
        }
      } catch (e) {
        console.error("Failed to load LLM config:", e);
      }
    }

    function updateFormFields() {
      const p = providerSelect.value;
      docsBox.innerHTML = providerDocs[p] || "";

      if (p === "offline") {
        apiKeyGroup.style.display = "none";
        ollamaGroup.style.display = "none";
      } else if (p === "ollama") {
        apiKeyGroup.style.display = "none";
        ollamaGroup.style.display = "block";
      } else {
        apiKeyGroup.style.display = "block";
        ollamaGroup.style.display = "none";
        apiKeyLabel.innerText = p.toUpperCase() + " API Key";
        apiKeyInput.placeholder = p === "gemini" ? "AIzaSy..." : "sk-...";

        if (p === "gemini" && cachedConfig.gemini_configured) {
          keyStatusHint.innerText = `Active Key: ${cachedConfig.gemini_key_masked} (Configured)`;
        } else if (p === "openai" && cachedConfig.openai_configured) {
          keyStatusHint.innerText = `Active Key: ${cachedConfig.openai_key_masked} (Configured)`;
        } else if (p === "anthropic" && cachedConfig.anthropic_configured) {
          keyStatusHint.innerText = `Active Key: ${cachedConfig.anthropic_key_masked} (Configured)`;
        } else {
          keyStatusHint.innerText = "No key currently set for this provider.";
        }
      }
    }

    if (openBtn) {
      openBtn.addEventListener("click", () => {
        modal.style.display = "flex";
        if (cachedConfig.preferred_provider) {
          providerSelect.value = cachedConfig.preferred_provider;
        }
        updateFormFields();
      });
    }

    function closeModal() {
      modal.style.display = "none";
    }

    if (closeBtn) closeBtn.addEventListener("click", closeModal);
    if (cancelBtn) cancelBtn.addEventListener("click", closeModal);
    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
      });
    }

    if (providerSelect) {
      providerSelect.addEventListener("change", updateFormFields);
    }

    if (toggleKeyVisibility && apiKeyInput) {
      toggleKeyVisibility.addEventListener("click", () => {
        apiKeyInput.type = apiKeyInput.type === "password" ? "text" : "password";
      });
    }

    if (saveBtn) {
      saveBtn.addEventListener("click", async () => {
        const prov = providerSelect.value;
        const key = apiKeyInput.value.trim();
        const ollamaUrl = ollamaInput.value.trim();

        saveBtn.disabled = true;
        saveBtn.innerText = "Saving...";

        try {
          const resp = await fetch("/api/config/llm", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              provider: prov,
              api_key: key,
              ollama_url: ollamaUrl
            })
          });
          const res = await resp.json();
          cachedConfig = res.config;
          if (statusText) statusText.innerText = "LLM: " + res.config.active_provider_label;
          if (statusDot) {
            statusDot.className = "chip-dot " + (res.config.cloud_enabled ? "green" : "cyan");
          }
          apiKeyInput.value = "";
          closeModal();
          alert(`Configuration updated successfully!\nActive Engine: ${res.config.active_provider_label}`);
        } catch (e) {
          alert("Error saving configuration: " + e.message);
        } finally {
          saveBtn.disabled = false;
          saveBtn.innerHTML = "<span>💾</span> Save & Activate";
        }
      });
    }

    loadConfig();
  }
});

