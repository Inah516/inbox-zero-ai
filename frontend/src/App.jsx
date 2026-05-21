import React, { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Inbox,
  Target,
  CheckSquare,
  PenSquare,
  Calendar,
  Sparkles,
  Send,
  Loader2,
  RotateCcw,
  Flame,
  Coffee,
  AlertTriangle,
  Activity,
  ClipboardList,
  Upload,
} from "lucide-react";

const AGENT_META = {
  priority: { Icon: Target, color: "rose-300", grad: "from-rose-500/15 to-amber-500/5", border: "border-rose-500/30" },
  action: { Icon: CheckSquare, color: "amber-300", grad: "from-amber-500/15 to-orange-500/5", border: "border-amber-500/30" },
  reply: { Icon: PenSquare, color: "orange-300", grad: "from-orange-500/15 to-amber-500/5", border: "border-orange-500/30" },
  meeting: { Icon: Calendar, color: "yellow-300", grad: "from-yellow-500/15 to-orange-500/5", border: "border-yellow-500/30" },
  synth: { Icon: Sparkles, color: "ember", grad: "from-ember/20 to-flame/10", border: "border-ember/40" },
};

const TEMP_META = {
  calm: { Icon: Coffee, label: "calm", cls: "bg-emerald-500/15 text-emerald-200 border-emerald-500/40" },
  busy: { Icon: Activity, label: "busy", cls: "bg-amber-500/15 text-amber-200 border-amber-500/40" },
  hot: { Icon: Flame, label: "hot", cls: "bg-orange-500/15 text-orange-200 border-orange-500/40" },
  "on fire": { Icon: AlertTriangle, label: "on fire", cls: "bg-rose-500/15 text-rose-200 border-rose-500/40" },
};

function Header({ provider, model }) {
  return (
    <header className="border-b border-line bg-ink/70 backdrop-blur sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-ember to-flame flex items-center justify-center shadow-lg shadow-ember/20">
            <Inbox className="w-5 h-5 text-ink" strokeWidth={2.5} />
          </div>
          <div>
            <h1 className="font-serif font-semibold text-xl leading-tight text-paper">
              InboxZero <span className="text-ember">AI</span>
            </h1>
            <p className="text-xs text-paper/50">drown in email · surface in 60s</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="px-2 py-1 rounded bg-ink2 border border-line text-paper/60 font-mono">
            {provider || "—"}
          </span>
          <span className="px-2 py-1 rounded bg-ink2 border border-line text-paper/60 font-mono">
            {model || "—"}
          </span>
        </div>
      </div>
    </header>
  );
}

function ExampleChips({ examples, onPick }) {
  if (!examples || !examples.length) return null;
  return (
    <div className="flex flex-wrap gap-2">
      <span className="text-xs text-paper/40 self-center">Try:</span>
      {examples.map((ex) => (
        <button
          key={ex.id}
          type="button"
          onClick={() => onPick(ex.id)}
          className="text-xs px-3 py-1.5 rounded-full bg-ink2 border border-line hover:border-ember/60 hover:text-ember transition flex items-center gap-1.5"
        >
          <span>{ex.title}</span>
          <span className="text-paper/40 text-[10px]">{ex.size}</span>
        </button>
      ))}
    </div>
  );
}

function InputPanel({ onRun, busy, examples, onLoadExample, parsedCount, text, setText }) {
  const fileInputRef = useRef(null);

  const handleFile = async (file) => {
    const t = await file.text();
    setText(t);
  };

  const onDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  };

  const submit = (e) => {
    e.preventDefault();
    if (!text.trim() || busy) return;
    onRun(text);
  };

  return (
    <form
      onSubmit={submit}
      onDragOver={(e) => e.preventDefault()}
      onDrop={onDrop}
      className="bg-ink2 border border-line rounded-2xl p-5 space-y-4"
    >
      <div className="flex items-center justify-between">
        <label className="block text-xs uppercase tracking-wider text-paper/50">
          Paste email batch · or drag a .eml / .txt file
        </label>
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="text-xs px-2.5 py-1 rounded-md bg-ink3 border border-line hover:border-ember/60 hover:text-ember transition flex items-center gap-1.5"
        >
          <Upload className="w-3 h-3" />
          Upload
        </button>
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept=".eml,.txt,.json"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />
      </div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={10}
        placeholder={`Separate emails with --- or paste raw .eml.\n\nFrom: someone@x.com\nSubject: Need a hand\n\nHey can you review the deck by tomorrow?\n\n---\n\nFrom: newsletter@y.com\nSubject: Daily roundup\n\n...`}
        className="w-full bg-ink3 border border-line rounded-lg px-3 py-2.5 text-sm font-mono text-paper/90 focus:outline-none focus:border-ember/60 resize-none scroll-soft"
      />

      <ExampleChips examples={examples} onPick={onLoadExample} />

      <div className="flex items-center justify-between gap-3">
        <span className="text-xs text-paper/40">
          {text.trim() ? `${text.length.toLocaleString()} chars` : "empty"}
        </span>
        <button
          type="submit"
          disabled={busy || !text.trim()}
          className="bg-gradient-to-r from-ember to-flame disabled:opacity-50 disabled:cursor-not-allowed text-ink font-semibold rounded-lg px-5 py-2.5 flex items-center gap-2 hover:brightness-110 transition shadow-md shadow-ember/20"
        >
          {busy ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Reading…
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              Triage inbox
            </>
          )}
        </button>
      </div>

      {parsedCount > 0 && (
        <div className="text-xs text-paper/50">
          Parsed <span className="text-ember font-semibold">{parsedCount}</span> emails on the last run.
        </div>
      )}
    </form>
  );
}

function StatPill({ label, value }) {
  return (
    <span className="px-2 py-1 rounded bg-ink2 border border-line text-paper/60 text-[11px] font-mono">
      {label}: <span className="text-paper">{value}</span>
    </span>
  );
}

function PipelineHero({ stats, busy, agents }) {
  const completed = agents.filter((a) => a.status === "done").length;
  const running = agents.filter((a) => a.status === "running").length;
  return (
    <div className="bg-ink2 border border-line rounded-2xl p-5">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h2 className="font-serif font-semibold text-paper">Pipeline</h2>
          <p className="text-xs text-paper/50 mt-1 leading-relaxed">
            Four specialists read the whole inbox at once via{" "}
            <code className="text-ember font-mono">asyncio.gather()</code>. A long-chain
            synthesizer then condenses their work into a 60-second digest.
          </p>
        </div>
        {busy && <Loader2 className="w-4 h-4 animate-spin text-ember shrink-0" />}
      </div>
      <div className="flex flex-wrap gap-2">
        <StatPill label="phase 1" value={`${completed}/${agents.length}`} />
        {running > 0 && <StatPill label="running" value={running} />}
        {stats?.total_tokens_estimate && (
          <StatPill label="~tokens" value={stats.total_tokens_estimate.toLocaleString()} />
        )}
        {stats?.email_count && <StatPill label="emails" value={stats.email_count} />}
      </div>
    </div>
  );
}

function AgentCard({ id, label, icon, state }) {
  const meta = AGENT_META[id] || AGENT_META.priority;
  const Icon = meta.Icon;
  const status = state?.status || "idle";
  const statusLabel = status === "idle" ? "WAITING" : status === "running" ? "READING…" : status.toUpperCase();
  return (
    <div className={`bg-gradient-to-br ${meta.grad} border ${meta.border} rounded-xl p-4 transition`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-base">{icon}</span>
          <Icon className={`w-4 h-4 text-${meta.color}`} />
          <h3 className="font-serif font-semibold text-paper">{label}</h3>
        </div>
        <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-wider">
          {status === "running" && <Loader2 className={`w-3 h-3 animate-spin text-${meta.color}`} />}
          <span className="text-paper/50">{statusLabel}</span>
          {state?.elapsed_s && <span className="text-paper/40">{state.elapsed_s}s</span>}
        </div>
      </div>
      <div className="markdown text-sm max-h-72 overflow-y-auto pr-2 scroll-soft">
        {state?.text ? (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{state.text}</ReactMarkdown>
        ) : (
          <p className="text-paper/40 italic text-xs">Waiting for trigger…</p>
        )}
      </div>
    </div>
  );
}

function TempBadge({ text }) {
  const m = text.match(/Inbox feels:\s*(?:\*\*)?(calm|busy|hot|on fire)/i);
  const t = m ? m[1].toLowerCase() : null;
  if (!t || !TEMP_META[t]) return null;
  const { Icon, label, cls } = TEMP_META[t];
  return (
    <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border ${cls} text-[11px] font-mono uppercase tracking-wider`}>
      <Icon className="w-3.5 h-3.5" />
      {label}
    </div>
  );
}

function Digest({ text, complete }) {
  if (!text) return null;
  return (
    <div className="bg-gradient-to-br from-ember/10 to-flame/5 border border-ember/40 rounded-2xl p-5 shadow-lg shadow-ember/5">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-ember" />
          <h2 className="font-serif font-semibold text-ember">60-Second Digest</h2>
          {complete && <TempBadge text={text} />}
        </div>
        <button
          onClick={() => navigator.clipboard.writeText(text)}
          className="text-xs px-2.5 py-1 rounded-md bg-ink3 border border-line hover:border-ember/60 hover:text-ember transition flex items-center gap-1.5"
        >
          <ClipboardList className="w-3 h-3" />
          Copy
        </button>
      </div>
      <div className="markdown">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
      </div>
    </div>
  );
}

export default function App() {
  const [config, setConfig] = useState({ provider: null, model: null });
  const [examples, setExamples] = useState([]);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [agents, setAgents] = useState({});
  const [agentList, setAgentList] = useState([]);
  const [synth, setSynth] = useState({ status: "idle", text: "" });
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/config").then((r) => r.json()).then(setConfig).catch(() => {});
    fetch("/api/examples").then((r) => r.json()).then(setExamples).catch(() => {});
  }, []);

  const loadExample = async (id) => {
    setBusy(true);
    try {
      const r = await fetch(`/api/examples/${id}`);
      const j = await r.json();
      const txt = j.emails
        .map((e) => `From: ${e.from}\nSubject: ${e.subject}\nDate: ${e.date}\n\n${e.body}`)
        .join("\n\n---\n\n");
      setText(txt);
    } finally {
      setBusy(false);
    }
  };

  const reset = () => {
    setAgents({});
    setSynth({ status: "idle", text: "" });
    setStats(null);
    setError(null);
  };

  const runTriage = async (raw) => {
    reset();
    setBusy(true);
    try {
      const r = await fetch("/api/triage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: raw }),
      });
      if (!r.ok || !r.body) throw new Error(`HTTP ${r.status}`);

      const reader = r.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const blocks = buf.split("\n\n");
        buf = blocks.pop() || "";
        for (const blk of blocks) {
          let evt = "message", data = "";
          for (const ln of blk.split("\n")) {
            if (ln.startsWith("event: ")) evt = ln.slice(7).trim();
            else if (ln.startsWith("data: ")) data += ln.slice(6);
          }
          if (!data) continue;
          let pl;
          try { pl = JSON.parse(data); } catch { continue; }
          handleEvent(evt, pl);
        }
      }
    } catch (e) {
      setError(e.message || "Unknown error");
    } finally {
      setBusy(false);
    }
  };

  const handleEvent = (event, payload) => {
    if (event === "pipeline_start") {
      setAgentList(payload.agents || []);
      setAgents(Object.fromEntries((payload.agents || []).map((a) => [a.id, { status: "idle", text: "" }])));
      return;
    }
    if (event === "phase") return;
    if (event === "agent_start") {
      const id = payload.agent;
      if (id === "synth") setSynth({ status: "running", text: "" });
      else setAgents((s) => ({ ...s, [id]: { ...(s[id] || {}), status: "running", text: "" } }));
      return;
    }
    if (event === "agent_token") {
      const id = payload.agent;
      if (id === "synth") setSynth((s) => ({ ...s, text: (s.text || "") + payload.text }));
      else setAgents((s) => ({ ...s, [id]: { ...(s[id] || {}), text: ((s[id] && s[id].text) || "") + payload.text } }));
      return;
    }
    if (event === "agent_done") {
      const id = payload.agent;
      if (id === "synth") setSynth((s) => ({ ...s, status: "done", elapsed_s: payload.elapsed_s }));
      else setAgents((s) => ({ ...s, [id]: { ...(s[id] || {}), status: "done", elapsed_s: payload.elapsed_s } }));
      return;
    }
    if (event === "agent_error") {
      if (payload.agent === "synth")
        setSynth((s) => ({ ...s, status: "error", text: (s.text || "") + `\n\n_Error: ${payload.message}_` }));
      else if (payload.agent)
        setAgents((s) => ({ ...s, [payload.agent]: { ...(s[payload.agent] || {}), status: "error" } }));
      else setError(payload.message || "pipeline error");
      return;
    }
    if (event === "pipeline_complete") {
      setStats(payload);
    }
  };

  const agentArrayState = Object.entries(agents).map(([id, st]) => ({ id, ...st }));

  return (
    <div className="min-h-screen flex flex-col">
      <Header provider={config.provider} model={config.model} />
      <main className="flex-1 max-w-6xl mx-auto w-full px-6 py-6 space-y-6">
        <section className="grid lg:grid-cols-2 gap-6">
          <InputPanel
            onRun={runTriage}
            busy={busy}
            examples={examples}
            onLoadExample={loadExample}
            parsedCount={stats?.email_count || 0}
            text={text}
            setText={setText}
          />
          <PipelineHero stats={stats} busy={busy} agents={agentArrayState} />
        </section>

        {error && (
          <div className="bg-rose-500/10 border border-rose-500/30 text-rose-200 rounded-lg px-4 py-3 text-sm">
            <strong>Error:</strong> {error}
          </div>
        )}

        {agentList.length > 0 && (
          <section>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm uppercase tracking-wider text-paper/50">
                Phase 1 · Parallel reasoning
              </h2>
              {!busy && (
                <button
                  onClick={reset}
                  className="text-xs px-2 py-1 rounded bg-ink2 border border-line hover:border-paper/40 transition flex items-center gap-1"
                >
                  <RotateCcw className="w-3 h-3" />
                  Clear
                </button>
              )}
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {agentList.map((a) => (
                <AgentCard key={a.id} id={a.id} label={a.label} icon={a.icon} state={agents[a.id]} />
              ))}
            </div>
          </section>
        )}

        {(synth.status !== "idle" || synth.text) && (
          <section>
            <h2 className="text-sm uppercase tracking-wider text-paper/50 mb-3">
              Phase 2 · Long-chain synthesis
            </h2>
            <Digest text={synth.text} complete={synth.status === "done"} />
          </section>
        )}

        <footer className="text-center text-xs text-paper/40 pt-8 pb-4">
          Built for people who'd rather think than triage. ·{" "}
          <a
            href="https://github.com/Inah516/inbox-zero-ai"
            target="_blank"
            rel="noreferrer"
            className="hover:text-ember"
          >
            GitHub
          </a>
        </footer>
      </main>
    </div>
  );
}
