import { useState, useEffect } from "react";
import "./App.css";

// BACKEND URL
const API = "http://127.0.0.1:8000";

export default function App() {
  const [apiKey, setApiKey] = useState("");
  const [user, setUser] = useState(null);

  // Navigation
  const [tab, setTab] = useState("commands");

  // Commands
  const [command, setCommand] = useState("");

  // Rules
  const [rules, setRules] = useState([]);
  const [ruleForm, setRuleForm] = useState({ pattern: "", action: "" });

  // Users
  const [newUser, setNewUser] = useState({ name: "", role: "member" });
  const [allUsers, setAllUsers] = useState([]);

  // Logs
  const [logs, setLogs] = useState([]);
  const [logType, setLogType] = useState("system");
  const [selectedUserId, setSelectedUserId] = useState("");

  // ------------------------------------------------------------
  // Load Current User
  // ------------------------------------------------------------
  const loadUser = async () => {
    console.log("Verify clicked. API key:", apiKey);

    if (!apiKey) {
      alert("Enter an API key");
      return;
    }

    try {
      const res = await fetch(`${API}/users/me`, {
        headers: { "x-api-key": apiKey },
      });

      if (!res.ok) {
        alert("Invalid API Key");
        setUser(null);
        return;
      }

      const data = await res.json();
      setUser(data);

      // Load admin data
      if (data.role === "admin") {
        loadRules();
        loadAllUsers();
      }
    } catch (err) {
      alert("Backend not reachable");
    }
  };

  // ------------------------------------------------------------
  // Load All Users (Admin)
  // ------------------------------------------------------------
  const loadAllUsers = async () => {
    const res = await fetch(`${API}/users/`, {
      headers: { "x-api-key": apiKey },
    });

    if (res.ok) setAllUsers(await res.json());
  };

  // ------------------------------------------------------------
  // Load Rules
  // ------------------------------------------------------------
  const loadRules = async () => {
    const res = await fetch(`${API}/rules/`, {
      headers: { "x-api-key": apiKey },
    });

    if (res.ok) setRules(await res.json());
  };

  // ------------------------------------------------------------
  // Load Logs
  // ------------------------------------------------------------
  const loadLogs = async () => {
    let url = `${API}/logs/system`;

    if (logType === "me") url = `${API}/logs/me`;
    if (logType === "user" && selectedUserId)
      url = `${API}/logs/user/${selectedUserId}`;

    const res = await fetch(url, {
      headers: { "x-api-key": apiKey },
    });
    if (!res.ok) {
    console.log("Log fetch failed", res.status);
    return;
}

    if (res.ok) setLogs(await res.json());
  };

  // ------------------------------------------------------------
  // Run Command
  // ------------------------------------------------------------
  const runCommand = async () => {
    const res = await fetch(`${API}/commands/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
      },
      body: JSON.stringify({ command_text: command }),
    });

    const data = await res.json();

    if (!res.ok) {
      alert("Error: " + data.detail);
      return;
    }

    alert("Command: " + data.status);
    setCommand("");
    loadUser();
  };
  
  // ------------------------------------------------------------
  // Create New Rule (Admin)
  // ------------------------------------------------------------
  const createRule = async () => {
    const res = await fetch(`${API}/rules/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
      },
      body: JSON.stringify(ruleForm),
    });

    const data = await res.json();

    if (res.ok) {
      alert("Rule created");
      setRuleForm({ pattern: "", action: "" });
      loadRules();
    } else {
      alert(data.detail);
    }
  };

  // ------------------------------------------------------------
  // Create User (Admin)
  // ------------------------------------------------------------
  const createNewUser = async () => {
    const res = await fetch(`${API}/users/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
      },
      body: JSON.stringify(newUser),
    });

    const data = await res.json();

    if (res.ok) {
      alert(`User Created — API Key: ${data.api_key}`);
      setNewUser({ name: "", role: "member" });
      loadAllUsers();
    } else {
      alert(data.detail);
    }
  };

  // ------------------------------------------------------------
  // Logout
  // ------------------------------------------------------------
  const logout = () => {
    setUser(null);
    setApiKey("");
    setTab("commands");
  };

  // ------------------------------------------------------------
  // LOGIN SCREEN
  // ------------------------------------------------------------
  if (!user) {
    return (
      <div className="center-wrapper">
        <div className="login-card">
          <h1>Command Gateway</h1>

          <input
            placeholder="Enter API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />

          <button onClick={loadUser}>Verify</button>
        </div>
      </div>
    );
  }

  // ------------------------------------------------------------
  // DASHBOARD
  // ------------------------------------------------------------
  return (
    <div className="layout">

      {/* SIDEBAR */}
      <aside className="sidebar">
        <h2 className="logo">Gateway</h2>

        <div className="user-info">
          <strong>{user.name}</strong>
          <small>{user.role}</small>
          <p>Credits: {user.credits}</p>
        </div>

        <nav>
          <button onClick={() => setTab("commands")}>Commands</button>

          {user.role === "admin" && (
            <>
              <button onClick={() => setTab("rules")}>Rules</button>
              <button onClick={() => setTab("users")}>Users</button>
              <button onClick={() => setTab("logs")}>Logs</button>
            </>
          )}
        </nav>

        <button className="logout-btn" onClick={logout}>Logout</button>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main">

        {/* COMMANDS */}
        {tab === "commands" && (
          <div className="card">
            <h2>Execute Command</h2>

            <input
              value={command}
              placeholder="Enter command..."
              onChange={(e) => setCommand(e.target.value)}
            />

            <button onClick={runCommand}>Run</button>
          </div>
        )}

        {/* RULES */}
        {tab === "rules" && user.role === "admin" && (
          <div className="card">
            <h2>Create Rule</h2>

            <input
              placeholder="Pattern (regex)"
              value={ruleForm.pattern}
              onChange={(e) =>
                setRuleForm({ ...ruleForm, pattern: e.target.value })
              }
            />

            <select
              value={ruleForm.action}
              onChange={(e) =>
                setRuleForm({ ...ruleForm, action: e.target.value })
              }
            >
              <option value="">Action</option>
              <option value="AUTO_ACCEPT">AUTO_ACCEPT</option>
              <option value="AUTO_REJECT">AUTO_REJECT</option>
            </select>

            <button onClick={createRule}>Add Rule</button>

            <h3>Existing Rules</h3>
            <ul>
              {rules.map((r) => (
                <li key={r.id}>
                  {r.pattern} → {r.action}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* USERS */}
        {tab === "users" && user.role === "admin" && (
          <div className="card">
            <h2>Create User</h2>

            <input
              placeholder="Name"
              value={newUser.name}
              onChange={(e) =>
                setNewUser({ ...newUser, name: e.target.value })
              }
            />

            <select
              value={newUser.role}
              onChange={(e) =>
                setNewUser({ ...newUser, role: e.target.value })
              }
            >
              <option value="member">Member</option>
              <option value="admin">Admin</option>
            </select>

            <button onClick={createNewUser}>Create User</button>

            <h3>All Users</h3>
            <ul>
              {allUsers.map((u) => (
                <li key={u.id}>
                  {u.name} — ({u.role})
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* LOGS */}
        {tab === "logs" && user.role === "admin" && (
          <div className="card">
            <h2>Logs</h2>

            <select value={logType} onChange={(e) => setLogType(e.target.value)}>
              <option value="system">System Logs</option>
              <option value="me">My Logs</option>
              <option value="user">Logs by User</option>
            </select>

            {logType === "user" && (
              <select
                value={selectedUserId}
                onChange={(e) => setSelectedUserId(e.target.value)}
              >
                <option value="">Select user</option>
                {allUsers.map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.name}
                  </option>
                ))}
              </select>
            )}

            <button onClick={loadLogs}>Load Logs</button>

            <ul className="logs">
              {logs.map((l) => (
                <li key={l.id}>
                  <strong>{l.action}</strong>: {l.description}
                  <br />
                  <small>{l.timestamp}</small>
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}
