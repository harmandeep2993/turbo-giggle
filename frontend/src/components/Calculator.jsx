import { useEffect, useState } from "react";
import { useMsal } from "@azure/msal-react";

import { calculate, power } from "../api";

// Symbols are unicode escapes so the source file stays plain ASCII.
const SYMBOLS = {
  add: "+",
  subtract: "\u2212",
  multiply: "\u00d7",
  divide: "\u00f7",
  power: "^",
};

// Keyboard keys that map to an operation.
const KEY_TO_OPERATION = {
  "+": "add",
  "-": "subtract",
  "*": "multiply",
  x: "multiply",
  "/": "divide",
  "^": "power",
};

// Keypad layout, row by row, like a physical calculator.
const KEYS = [
  { label: "AC", action: "clear", kind: "function" },
  { label: "\u232b", action: "backspace", kind: "function", title: "Backspace" },
  { label: "\u00b1", action: "sign", kind: "function", title: "Change sign" },
  { label: SYMBOLS.divide, action: "op", value: "divide", kind: "operator" },
  { label: "7", action: "digit" },
  { label: "8", action: "digit" },
  { label: "9", action: "digit" },
  { label: SYMBOLS.multiply, action: "op", value: "multiply", kind: "operator" },
  { label: "4", action: "digit" },
  { label: "5", action: "digit" },
  { label: "6", action: "digit" },
  { label: SYMBOLS.subtract, action: "op", value: "subtract", kind: "operator" },
  { label: "1", action: "digit" },
  { label: "2", action: "digit" },
  { label: "3", action: "digit" },
  { label: SYMBOLS.add, action: "op", value: "add", kind: "operator" },
  { label: "x\u02b8", action: "op", value: "power", kind: "operator", title: "Power" },
  { label: "0", action: "digit" },
  { label: ".", action: "digit" },
  { label: "=", action: "equals", kind: "equals" },
];

// A physical calculator display has room for a limited number of digits.
const MAX_INPUT_LENGTH = 16;
// Results are rounded to this many significant digits so 0.1 + 0.2 shows 0.3.
const RESULT_PRECISION = 12;
const HISTORY_LIMIT = 5;
// With min replicas 0 the backend sleeps when idle; after this delay we tell the
// user the request is waking it up, so a slow answer does not look broken.
const SLOW_REQUEST_MS = 3000;

function formatResult(value) {
  return String(parseFloat(value.toPrecision(RESULT_PRECISION)));
}

function Calculator() {
  const { instance, accounts } = useMsal();
  const [display, setDisplay] = useState("0");
  const [stored, setStored] = useState(null);
  const [operation, setOperation] = useState(null);
  // True right after an operator: the next digit starts the second number.
  const [waitingForSecond, setWaitingForSecond] = useState(false);
  // True right after "=": the next digit starts a new calculation.
  const [showingResult, setShowingResult] = useState(false);
  const [expression, setExpression] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [slow, setSlow] = useState(false);
  const [history, setHistory] = useState([]);

  // Every calculation goes to the backend, which needs a valid login token.
  async function compute(a, op, b) {
    setLoading(true);
    const slowTimer = setTimeout(() => setSlow(true), SLOW_REQUEST_MS);
    try {
      const account = accounts[0];
      const value =
        op === "power"
          ? await power(instance, account, a, b)
          : await calculate(instance, account, a, b, op);
      setHistory((previous) =>
        [{ a, op, b, value }, ...previous].slice(0, HISTORY_LIMIT),
      );
      return value;
    } finally {
      clearTimeout(slowTimer);
      setSlow(false);
      setLoading(false);
    }
  }

  function showError(message) {
    setError(message);
    setDisplay("0");
    setStored(null);
    setOperation(null);
    setWaitingForSecond(false);
    setShowingResult(true);
  }

  function pressDigit(digit) {
    setError("");
    if (waitingForSecond || showingResult) {
      setDisplay(digit === "." ? "0." : digit);
      setWaitingForSecond(false);
      setShowingResult(false);
      if (showingResult) setExpression("");
      return;
    }
    if (digit === "." && display.includes(".")) return;
    if (display.replace("-", "").length >= MAX_INPUT_LENGTH) return;
    setDisplay(display === "0" && digit !== "." ? digit : display + digit);
  }

  async function pressOperator(nextOperation) {
    setError("");
    const current = Number(display);
    // Changing your mind about the operator before typing the second number.
    if (operation && waitingForSecond) {
      setOperation(nextOperation);
      setExpression(`${formatResult(stored)} ${SYMBOLS[nextOperation]}`);
      return;
    }
    let first = current;
    // Chaining like 2 + 3 x: calculate 2 + 3 first, then continue with x.
    if (operation) {
      try {
        first = await compute(stored, operation, current);
      } catch (err) {
        showError(err.message);
        return;
      }
    }
    setStored(first);
    setDisplay(formatResult(first));
    setOperation(nextOperation);
    setExpression(`${formatResult(first)} ${SYMBOLS[nextOperation]}`);
    setWaitingForSecond(true);
    setShowingResult(false);
  }

  async function pressEquals() {
    if (!operation || waitingForSecond) return;
    const current = Number(display);
    const finished = `${formatResult(stored)} ${SYMBOLS[operation]} ${display} =`;
    try {
      const value = await compute(stored, operation, current);
      setExpression(finished);
      setDisplay(formatResult(value));
      setStored(null);
      setOperation(null);
      setShowingResult(true);
    } catch (err) {
      setExpression(finished);
      showError(err.message);
    }
  }

  function pressClear() {
    setDisplay("0");
    setStored(null);
    setOperation(null);
    setWaitingForSecond(false);
    setShowingResult(false);
    setExpression("");
    setError("");
  }

  function pressBackspace() {
    if (waitingForSecond || showingResult) return;
    const shorter = display.slice(0, -1);
    setDisplay(shorter === "" || shorter === "-" ? "0" : shorter);
  }

  function pressSign() {
    if (display === "0" || waitingForSecond) return;
    setDisplay(display.startsWith("-") ? display.slice(1) : `-${display}`);
    setShowingResult(false);
  }

  function press(key) {
    if (loading) return;
    if (key.action === "digit") pressDigit(key.label);
    if (key.action === "op") pressOperator(key.value);
    if (key.action === "equals") pressEquals();
    if (key.action === "clear") pressClear();
    if (key.action === "backspace") pressBackspace();
    if (key.action === "sign") pressSign();
  }

  // Continue from a previous answer: it becomes the number on the display.
  function reuseResult(value) {
    if (loading) return;
    pressClear();
    setDisplay(formatResult(value));
    setShowingResult(true);
  }

  // Keyboard support, so it can be used like a desktop calculator app.
  // No dependency list: the handler is re-attached each render so it always
  // sees the current display and operation.
  useEffect(() => {
    function onKeyDown(event) {
      if (loading) return;
      const { key } = event;
      if (/^[0-9.]$/.test(key)) pressDigit(key);
      else if (KEY_TO_OPERATION[key]) pressOperator(KEY_TO_OPERATION[key]);
      else if (key === "Enter" || key === "=") {
        event.preventDefault();
        pressEquals();
      } else if (key === "Backspace") pressBackspace();
      else if (key === "Escape") pressClear();
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  });

  let mainText = display;
  if (loading) mainText = slow ? "Waking server..." : "...";
  else if (error) mainText = "Error";

  return (
    <div className="calculator">
      <section className="device">
        <div className="device-top">
          <span className="device-brand">CALC-API</span>
          <span className="device-model">Entra ID secured</span>
        </div>

        <div className="lcd" aria-live="polite">
          <div className="lcd-expression">{error || expression || "\u00a0"}</div>
          <div className={`lcd-value ${error ? "status--error" : ""}`}>{mainText}</div>
        </div>

        <div className="keypad">
          {KEYS.map((key) => (
            <button
              key={key.label}
              type="button"
              title={key.title}
              className={[
                "key",
                key.kind ? `key--${key.kind}` : "",
                key.action === "op" && operation === key.value && waitingForSecond
                  ? "key--active"
                  : "",
              ].join(" ")}
              onClick={() => press(key)}
              disabled={loading}
            >
              {key.label}
            </button>
          ))}
        </div>
      </section>

      {history.length > 0 && (
        <section className="tape">
          <h2 className="tape-title">Recent</h2>
          <ul className="history">
            {history.map((item, index) => (
              <li key={index}>
                <button
                  type="button"
                  className="history-item"
                  onClick={() => reuseResult(item.value)}
                  title="Use this result"
                >
                  <span className="muted">
                    {formatResult(item.a)} {SYMBOLS[item.op]} {formatResult(item.b)} =
                  </span>
                  <strong>{formatResult(item.value)}</strong>
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

    </div>
  );
}

export default Calculator;
