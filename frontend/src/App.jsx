import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [customer, setCustomer] = useState(null);

  const [loading, setLoading] = useState(false);

  // Modal + claim state
  const [showModal, setShowModal] = useState(false);
  const [selectedPolicy, setSelectedPolicy] = useState(null);

  const [claimData, setClaimData] = useState({
    amount: "",
    description: ""
  });

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/customers/2/")
      .then((res) => {
        setCustomer(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  function submitClaim() {
    axios
      .post("http://127.0.0.1:8000/api/claims/", {
        policy_id: selectedPolicy.id,
        amount: claimData.amount,
        description: claimData.description
      })
      .then((res) => {
        alert("Claim submitted!");

        console.log(res.data);

        setShowModal(false);
        setClaimData({ amount: "", description: "" });
      })
      .catch((err) => {
        console.log(err);
      });
  }
  function renewPolicy(policyId) {
  setLoading(true);

  axios
    .post("http://127.0.0.1:8000/api/renew-policy/", {
      policy_id: policyId
    })
    .then((res) => {
      alert("Policy renewed!");

      // refresh customer data
      return axios.get("http://127.0.0.1:8000/api/customers/2/");
    })
    .then((res) => {
      setCustomer(res.data);
    })
    .catch((err) => {
      console.log(err);
    })
    .finally(() => {
      setLoading(false);
    });
}

  if (!customer) return <h2>Loading...</h2>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Customer Dashboard</h1>

      {/* Customer Info */}
      <div>
        <h2>Name: {customer.name}</h2>
        <p>Wallet Balance: ${customer.wallet_balance}</p>
      </div>

      {/* Policies */}
      <h3>Policies</h3>

      {customer.policies.map((policy) => (
  <div
    key={policy.id}
    style={{
      padding: "10px",
      margin: "10px 0",
      border: "1px solid #ccc"
    }}
  >
    <p>Type: {policy.policy_type}</p>
    <p>Premium: ${policy.premium_amount}</p>

    {/* STATUS */}
    <span style={getStatusStyle(policy.status)}>
      {policy.status}
    </span>

    {/* RENEW BUTTON */}
    <button
      onClick={() => renewPolicy(policy.id)}
      disabled={loading}
      style={{ marginTop: "10px" }}
    >
      {loading ? "Processing..." : "Renew"}
    </button>

    {/* FILE CLAIM BUTTON */}
    {policy.status === "ACTIVE" && (
      <div>
        <button
          onClick={() => {
            setSelectedPolicy(policy);
            setShowModal(true);
          }}
        >
          File Claim
        </button>
      </div>
    )}
  </div>
))}

      {/* MODAL */}
      {showModal && (
        <div style={modalOverlay}>
          <div style={modalBox}>
            <h2>File Claim</h2>

            <input
              placeholder="Amount"
              value={claimData.amount}
              onChange={(e) =>
                setClaimData({ ...claimData, amount: e.target.value })
              }
            />

            <input
              placeholder="Description"
              value={claimData.description}
              onChange={(e) =>
                setClaimData({ ...claimData, description: e.target.value })
              }
            />

            <button onClick={submitClaim}>Submit</button>
            <button onClick={() => setShowModal(false)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

/* STATUS COLORS */
function getStatusStyle(status) {
  let color = "";

  switch (status) {
    case "ACTIVE":
      color = "green";
      break;
    case "PENDING":
      color = "yellow";
      break;
    case "LAPSED":
      color = "red";
      break;
    case "UNDER_REVIEW":
      color = "orange";
      break;
    default:
      color = "gray";
  }

  return {
    backgroundColor: color,
    color: "white",
    padding: "5px 10px",
    borderRadius: "5px"
  };
}

/* MODAL STYLES */
const modalOverlay = {
  position: "fixed",
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: "rgba(0,0,0,0.5)",
  display: "flex",
  justifyContent: "center",
  alignItems: "center"
};

const modalBox = {
  background: "white",
  padding: "20px",
  borderRadius: "10px",
  width: "300px",
  display: "flex",
  flexDirection: "column",
  gap: "10px"
};

export default App;