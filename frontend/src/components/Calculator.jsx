import { useState } from "react";
import { useMsal } from "@azure/msal-react";

import { calculate, power } from "../api";

const OPERATIONS = [
  { value: "add", label: "+" },
  { value: "subtract", label: "-" },
  { value: "multiply", label: "x" },
  { value: "divide", label: "/" },
  { value: "power", label: "^" },
];

function Calculator() {
  const { instance, accounts } = useMsal();
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [operation, setOperation] = useState("add");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const account = accounts[0];
      // Power is a separate endpoint in the backend, so it needs its own call.
      const value =
        operation === "power"
          ? await power(instance, account, Number(a), Number(b))
          : await calculate(instance, account, Number(a), Number(b), operation);
      setResult(value);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="calculator" onSubmit={handleSubmit}>
      <div className="row">
        <input
          type="number"
          step="any"
          value={a}
          onChange={(e) => setA(e.target.value)}
          placeholder="a"
          required
        />
        <select value={operation} onChange={(e) => setOperation(e.target.value)}>
          {OPERATIONS.map((op) => (
            <option key={op.value} value={op.value}>
              {op.label}
            </option>
          ))}
        </select>
        <input
          type="number"
          step="any"
          value={b}
          onChange={(e) => setB(e.target.value)}
          placeholder="b"
          required
        />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? "Calculating..." : "Calculate"}
      </button>
      {result !== null && <p className="result">Result: {result}</p>}
      {error && <p className="error">{error}</p>}
    </form>
  );
}

export default Calculator;
